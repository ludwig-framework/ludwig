"""
Ludwig IoT - Garden and irrigation automation
"""

from typing import Callable, Optional
from dataclasses import dataclass
from ludwig.iot.sensor import Sensor
from ludwig.iot.actuators import Relay
import time
from datetime import datetime


@dataclass
class Plant:
    """A plant being monitored."""
    name: str
    moisture_sensor: Sensor
    pump: Relay
    moisture_threshold: int = 30  # Water when below this
    last_watered: float = 0
    water_duration: int = 10  # seconds
    
    @property
    def moisture(self) -> int:
        """Current moisture level (0-100%)."""
        return self.moisture_sensor.read()
    
    @property
    def needs_water(self) -> bool:
        """Check if plant needs watering."""
        return self.moisture < self.moisture_threshold
    
    def water(self, seconds: int = None):
        """Water the plant."""
        duration = seconds or self.water_duration
        print(f"💧 Watering {self.name} for {duration}s...")
        self.pump.on()
        time.sleep(duration)
        self.pump.off()
        self.last_watered = time.time()


class Garden:
    """
    Automated garden/irrigation system.
    
    Example:
        garden = Garden()
        
        # Add plants with their sensors and pumps
        garden.add_plant("tomatoes", moisture_pin=0, pump_pin=17)
        garden.add_plant("herbs", moisture_pin=1, pump_pin=18)
        garden.add_plant("flowers", moisture_pin=2, pump_pin=19)
        
        # Check every hour
        @garden.check_every(hours=1)
        def water_if_dry(plant):
            if plant.needs_water:
                plant.water()
                garden.log(f"Watered {plant.name}")
        
        # Or water on schedule
        @garden.at("06:00")
        def morning_water():
            for plant in garden.plants:
                if plant.needs_water:
                    plant.water()
        
        garden.run()
    """
    
    def __init__(self, name: str = "garden"):
        self.name = name
        self._plants: dict[str, Plant] = {}
        self._schedules: list[tuple[str, Callable]] = []
        self._checks: list[tuple[int, Callable]] = []  # (interval_seconds, callback)
        self._running = False
        
        # Weather sensor (optional)
        self._rain_sensor: Optional[Sensor] = None
        self._light_sensor: Optional[Sensor] = None
        self._temp_sensor: Optional[Sensor] = None
    
    def add_plant(
        self,
        name: str,
        moisture_pin: int,
        pump_pin: int,
        threshold: int = 30,
        water_duration: int = 10,
    ):
        """
        Add a plant to monitor.
        
        Args:
            name: Plant name
            moisture_pin: Analog pin for moisture sensor
            pump_pin: GPIO pin for water pump relay
            threshold: Water when moisture below this (0-100)
            water_duration: How long to water (seconds)
        """
        plant = Plant(
            name=name,
            moisture_sensor=Sensor.moisture(moisture_pin, name=f"{name}_moisture"),
            pump=Relay(pump_pin, name=f"{name}_pump"),
            moisture_threshold=threshold,
            water_duration=water_duration,
        )
        self._plants[name] = plant
    
    def plant(self, name: str) -> Optional[Plant]:
        """Get plant by name."""
        return self._plants.get(name)
    
    @property
    def plants(self) -> list[Plant]:
        """All plants."""
        return list(self._plants.values())
    
    def add_rain_sensor(self, pin: int):
        """Add rain sensor."""
        self._rain_sensor = Sensor("rain", pin=pin)
    
    def add_light_sensor(self, pin: int):
        """Add light sensor."""
        self._light_sensor = Sensor.light(pin)
    
    def add_temp_sensor(self, pin: int, type: str = "dht22"):
        """Add temperature sensor."""
        self._temp_sensor = Sensor.temperature(pin, type=type)
    
    @property
    def is_raining(self) -> bool:
        """Check if it's raining."""
        if self._rain_sensor:
            return self._rain_sensor.read()
        return False
    
    @property
    def light_level(self) -> int:
        """Current light level (0-100)."""
        if self._light_sensor:
            return self._light_sensor.read()
        return 0
    
    @property
    def temperature(self) -> float:
        """Current temperature."""
        if self._temp_sensor:
            return self._temp_sensor.read()
        return 0
    
    # === Scheduling ===
    
    def check_every(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        """
        Schedule regular plant checks.
        
        Example:
            @garden.check_every(hours=1)
            def check(plant):
                if plant.needs_water:
                    plant.water()
        """
        interval = hours * 3600 + minutes * 60 + seconds
        
        def decorator(func: Callable):
            self._checks.append((interval, func))
            return func
        return decorator
    
    def at(self, time_spec: str):
        """
        Schedule action at specific time.
        
        Example:
            @garden.at("06:00")
            def morning_routine():
                garden.water_all()
        """
        def decorator(func: Callable):
            self._schedules.append((time_spec, func))
            return func
        return decorator
    
    # === Actions ===
    
    def water_all(self, skip_if_wet: bool = True):
        """Water all plants."""
        for plant in self._plants.values():
            if skip_if_wet and not plant.needs_water:
                continue
            plant.water()
    
    def status(self) -> dict:
        """Get garden status."""
        return {
            "plants": {
                name: {
                    "moisture": plant.moisture,
                    "needs_water": plant.needs_water,
                    "last_watered": plant.last_watered,
                }
                for name, plant in self._plants.items()
            },
            "is_raining": self.is_raining,
            "light_level": self.light_level,
            "temperature": self.temperature,
        }
    
    def log(self, message: str):
        """Log a garden event."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 🌱 {message}")
        
        # Could also write to file or database
    
    # === Run Loop ===
    
    def run(self):
        """Start garden automation."""
        self._running = True
        print(f"🌱 {self.name} automation running...")
        print(f"   Monitoring {len(self._plants)} plants")
        
        last_check = {}
        last_schedule = {}
        
        try:
            while self._running:
                now = time.time()
                
                # Skip watering if raining
                if self.is_raining:
                    time.sleep(60)
                    continue
                
                # Run scheduled checks
                for interval, func in self._checks:
                    last = last_check.get(id(func), 0)
                    if now - last >= interval:
                        for plant in self._plants.values():
                            func(plant)
                        last_check[id(func)] = now
                
                # Run time-based schedules
                current_time = datetime.now().strftime("%H:%M")
                for time_spec, func in self._schedules:
                    if time_spec == current_time:
                        last = last_schedule.get(id(func), 0)
                        if now - last > 60:  # Prevent duplicate runs
                            func()
                            last_schedule[id(func)] = now
                
                time.sleep(10)  # Check every 10 seconds
                
        except KeyboardInterrupt:
            print(f"\n🌱 {self.name} stopping...")
    
    def stop(self):
        """Stop automation."""
        self._running = False
    
    def __repr__(self):
        return f"Garden(name={self.name}, plants={len(self._plants)})"
