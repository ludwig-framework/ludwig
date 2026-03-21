"""
Ludwig IoT - Smart home automation
"""

from typing import Any, Callable, Optional
from ludwig.iot.actuators import Light, Relay
from ludwig.iot.sensor import Sensor
import time
from datetime import datetime


class Room:
    """
    A room in the smart home.
    
    Example:
        living = Room("living_room")
        living.add(Light(pin=17, name="ceiling"))
        living.add(Light(pin=18, name="lamp"))
        living.add(Sensor.motion(pin=4))
        
        living.light("ceiling").on()
        living.all_lights_off()
    """
    
    def __init__(self, name: str):
        self.name = name
        self._lights: dict[str, Light] = {}
        self._sensors: dict[str, Sensor] = {}
        self._devices: dict[str, Relay] = {}
    
    def add(self, device):
        """Add a device to the room."""
        if isinstance(device, Light):
            self._lights[device.name] = device
        elif isinstance(device, Sensor):
            self._sensors[device.name] = device
        elif isinstance(device, Relay):
            self._devices[device.name] = device
    
    def light(self, name: str) -> Optional[Light]:
        """Get a light by name."""
        return self._lights.get(name)
    
    def sensor(self, name: str) -> Optional[Sensor]:
        """Get a sensor by name."""
        return self._sensors.get(name)
    
    def device(self, name: str) -> Optional[Relay]:
        """Get a device by name."""
        return self._devices.get(name)
    
    @property
    def lights(self) -> list[Light]:
        """All lights in room."""
        return list(self._lights.values())
    
    @property
    def motion(self) -> Optional[Sensor]:
        """Motion sensor shortcut."""
        for sensor in self._sensors.values():
            if sensor.sensor_type == "motion":
                return sensor
        return None
    
    @property
    def temperature(self) -> Optional[float]:
        """Temperature sensor shortcut."""
        for sensor in self._sensors.values():
            if sensor.sensor_type == "temperature":
                return sensor.read()
        return None
    
    @property
    def thermostat(self):
        """Thermostat device shortcut."""
        return self._devices.get("thermostat")
    
    def all_lights_on(self):
        """Turn on all lights."""
        for light in self._lights.values():
            light.on()
    
    def all_lights_off(self):
        """Turn off all lights."""
        for light in self._lights.values():
            light.off()
    
    def __repr__(self):
        return f"Room({self.name}, lights={len(self._lights)}, sensors={len(self._sensors)})"


class Thermostat:
    """Smart thermostat."""
    
    def __init__(self, pin: int, sensor_pin: int = None, name: str = "thermostat"):
        self.name = name
        self._relay = Relay(pin, name=name)
        self._sensor = Sensor.temperature(sensor_pin) if sensor_pin else None
        self._target = 22  # Default target temperature
        self._mode = "auto"  # auto, heat, cool, off
    
    def set(self, temperature: float):
        """Set target temperature."""
        self._target = temperature
    
    @property
    def current(self) -> float:
        """Current temperature."""
        if self._sensor:
            return self._sensor.read()
        return 0
    
    @property
    def target(self) -> float:
        """Target temperature."""
        return self._target
    
    def mode(self, mode: str):
        """Set mode: auto, heat, cool, off"""
        self._mode = mode


class Home:
    """
    Smart home controller.
    
    Example:
        home = Home()
        
        # Define rooms
        living = home.room("living_room")
        living.add(Light(pin=17, name="ceiling"))
        living.add(Sensor.motion(pin=4))
        
        bedroom = home.room("bedroom")
        bedroom.add(Light(pin=18, dimmable=True))
        
        # Automations
        @home.at("sunset")
        def evening_mode():
            living.light("ceiling").on()
            bedroom.light("main").brightness(30)
        
        @home.at("23:00")
        def bedtime():
            home.all_lights_off()
        
        @home.when(living.motion.detected)
        def motion_light():
            living.light("ceiling").on(duration=300)
        
        home.run()
    """
    
    def __init__(self, name: str = "home"):
        self.name = name
        self._rooms: dict[str, Room] = {}
        self._schedules: list[tuple[str, Callable]] = []
        self._automations: list[tuple[str, Callable, Callable]] = []
        self._running = False
    
    def room(self, name: str) -> Room:
        """Get or create a room."""
        if name not in self._rooms:
            self._rooms[name] = Room(name)
        return self._rooms[name]
    
    @property
    def rooms(self) -> list[Room]:
        """All rooms."""
        return list(self._rooms.values())
    
    def all_lights_on(self):
        """Turn on all lights in all rooms."""
        for room in self._rooms.values():
            room.all_lights_on()
    
    def all_lights_off(self):
        """Turn off all lights in all rooms."""
        for room in self._rooms.values():
            room.all_lights_off()
    
    # === Scheduling ===
    
    def at(self, time_spec: str):
        """
        Schedule an action.
        
        Args:
            time_spec: Time like "sunset", "sunrise", "23:00", "08:30"
        """
        def decorator(func: Callable):
            self._schedules.append((time_spec, func))
            return func
        return decorator
    
    def every(self, interval: str):
        """
        Repeat an action.
        
        Args:
            interval: Like "1 hour", "30 minutes", "1 day"
        """
        def decorator(func: Callable):
            self._schedules.append((f"every:{interval}", func))
            return func
        return decorator
    
    def when(self, condition: Callable):
        """
        Trigger action when condition is true.
        
        Example:
            @home.when(lambda: living.motion.read())
            def motion_detected():
                living.light("ceiling").on()
        """
        def decorator(func: Callable):
            self._automations.append(("when", condition, func))
            return func
        return decorator
    
    def _check_time(self, time_spec: str) -> bool:
        """Check if it's time to trigger a schedule."""
        now = datetime.now()
        
        if time_spec == "sunset":
            # Approximate sunset (could use astronomy library)
            return now.hour == 18 and now.minute == 0
        elif time_spec == "sunrise":
            return now.hour == 6 and now.minute == 0
        elif ":" in time_spec:
            hour, minute = map(int, time_spec.split(":"))
            return now.hour == hour and now.minute == minute
        
        return False
    
    def _parse_interval(self, interval: str) -> int:
        """Parse interval string to seconds."""
        parts = interval.lower().split()
        value = int(parts[0])
        unit = parts[1] if len(parts) > 1 else "seconds"
        
        multipliers = {
            "second": 1, "seconds": 1,
            "minute": 60, "minutes": 60,
            "hour": 3600, "hours": 3600,
            "day": 86400, "days": 86400,
        }
        
        return value * multipliers.get(unit, 1)
    
    # === Run Loop ===
    
    def run(self):
        """Start home automation loop."""
        self._running = True
        print(f"🏠 {self.name} automation running...")
        
        last_check = {}  # Track last trigger time for schedules
        
        try:
            while self._running:
                now = time.time()
                
                # Check schedules
                for time_spec, func in self._schedules:
                    if time_spec.startswith("every:"):
                        interval = self._parse_interval(time_spec[6:])
                        last = last_check.get(id(func), 0)
                        if now - last >= interval:
                            func()
                            last_check[id(func)] = now
                    elif self._check_time(time_spec):
                        if id(func) not in last_check or now - last_check[id(func)] > 60:
                            func()
                            last_check[id(func)] = now
                
                # Check automations
                for auto_type, condition, func in self._automations:
                    if auto_type == "when" and condition():
                        func()
                
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n🏠 {self.name} stopping...")
    
    def stop(self):
        """Stop automation."""
        self._running = False
    
    def __repr__(self):
        return f"Home(name={self.name}, rooms={len(self._rooms)})"
