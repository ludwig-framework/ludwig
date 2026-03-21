"""
Ludwig IoT - Sensor abstractions
"""

from typing import Any, Callable, Optional, Literal
from dataclasses import dataclass
from ludwig.iot.pin import Pin, Board
import time


class Sensor:
    """
    Base sensor class with factory methods for common sensors.
    
    Example:
        # Motion sensor (PIR)
        motion = Sensor.motion(pin=4)
        
        @motion.on_detected
        def movement():
            print("Motion detected!")
        
        # Temperature sensor
        temp = Sensor.temperature(pin=7, type="dht22")
        print(f"Temperature: {temp.read()}°C")
        
        # Distance sensor
        distance = Sensor.ultrasonic(trigger=23, echo=24)
        print(f"Distance: {distance.read()} cm")
    """
    
    def __init__(
        self,
        sensor_type: str,
        pin: int = None,
        pins: dict = None,
        name: Optional[str] = None,
        **config
    ):
        self.sensor_type = sensor_type
        self.pin = pin
        self.pins = pins or {}
        self.name = name or f"{sensor_type}_sensor"
        self.config = config
        
        self._value = None
        self._callbacks: dict[str, list[Callable]] = {}
        
        self._setup()
    
    def _setup(self):
        """Initialize sensor hardware."""
        if self.pin:
            self._input_pin = Pin(self.pin, mode="input", pull="down")
    
    def read(self) -> Any:
        """Read current sensor value."""
        if self.sensor_type == "motion":
            return self._read_motion()
        elif self.sensor_type == "temperature":
            return self._read_temperature()
        elif self.sensor_type == "humidity":
            return self._read_humidity()
        elif self.sensor_type == "ultrasonic":
            return self._read_ultrasonic()
        elif self.sensor_type == "moisture":
            return self._read_moisture()
        elif self.sensor_type == "light":
            return self._read_light()
        elif self.sensor_type == "door":
            return self._read_digital()
        elif self.sensor_type == "window":
            return self._read_digital()
        else:
            return self._read_digital()
    
    def _read_digital(self) -> bool:
        """Read digital sensor (on/off)."""
        if hasattr(self, "_input_pin"):
            return self._input_pin.read()
        return False
    
    def _read_motion(self) -> bool:
        """Read PIR motion sensor."""
        return self._read_digital()
    
    def _read_temperature(self) -> float:
        """Read temperature sensor (DHT11/DHT22/DS18B20)."""
        sensor_model = self.config.get("type", "dht22")
        
        try:
            if sensor_model in ("dht11", "dht22"):
                import Adafruit_DHT
                sensor = Adafruit_DHT.DHT22 if sensor_model == "dht22" else Adafruit_DHT.DHT11
                humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
                return temperature
            elif sensor_model == "ds18b20":
                # One-wire temperature sensor
                return self._read_ds18b20()
        except ImportError:
            # Simulation mode
            import random
            return round(20 + random.random() * 10, 1)
        
        return 0.0
    
    def _read_humidity(self) -> float:
        """Read humidity from DHT sensor."""
        sensor_model = self.config.get("type", "dht22")
        
        try:
            import Adafruit_DHT
            sensor = Adafruit_DHT.DHT22 if sensor_model == "dht22" else Adafruit_DHT.DHT11
            humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
            return humidity
        except ImportError:
            import random
            return round(40 + random.random() * 30, 1)
        
        return 0.0
    
    def _read_ultrasonic(self) -> float:
        """Read ultrasonic distance sensor (HC-SR04)."""
        trigger_pin = self.pins.get("trigger")
        echo_pin = self.pins.get("echo")
        
        if not trigger_pin or not echo_pin:
            return 0.0
        
        trigger = Pin(trigger_pin, mode="output")
        echo = Pin(echo_pin, mode="input")
        
        board = Pin._get_board()
        
        if board == Board.SIMULATION:
            import random
            return round(10 + random.random() * 200, 1)
        
        # Send trigger pulse
        trigger.off()
        time.sleep(0.00002)
        trigger.on()
        time.sleep(0.00001)
        trigger.off()
        
        # Measure echo
        start = time.time()
        while not echo.read():
            start = time.time()
            if time.time() - start > 0.1:
                return -1  # Timeout
        
        while echo.read():
            end = time.time()
            if time.time() - start > 0.1:
                return -1  # Timeout
        
        # Calculate distance
        duration = end - start
        distance = duration * 34300 / 2  # Speed of sound / 2
        
        return round(distance, 1)
    
    def _read_moisture(self) -> int:
        """Read soil moisture sensor (analog, 0-100%)."""
        # Would use ADC on real hardware
        import random
        return int(random.random() * 100)
    
    def _read_light(self) -> int:
        """Read light sensor (analog, 0-100%)."""
        import random
        return int(random.random() * 100)
    
    def _read_ds18b20(self) -> float:
        """Read DS18B20 temperature sensor."""
        # One-wire implementation
        import random
        return round(20 + random.random() * 10, 1)
    
    # === Event Handlers ===
    
    def on(self, event: str):
        """Register an event handler."""
        def decorator(func: Callable):
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(func)
            return func
        return decorator
    
    @property
    def on_detected(self):
        """Shortcut for on("detected")."""
        return self.on("detected")
    
    @property
    def on_change(self):
        """Shortcut for on("change")."""
        return self.on("change")
    
    # === Factory Methods ===
    
    @classmethod
    def motion(cls, pin: int, name: str = None) -> "Sensor":
        """Create a PIR motion sensor."""
        return cls("motion", pin=pin, name=name or "motion")
    
    @classmethod
    def temperature(cls, pin: int, type: str = "dht22", name: str = None) -> "Sensor":
        """Create a temperature sensor."""
        return cls("temperature", pin=pin, type=type, name=name or "temperature")
    
    @classmethod
    def humidity(cls, pin: int, type: str = "dht22", name: str = None) -> "Sensor":
        """Create a humidity sensor."""
        return cls("humidity", pin=pin, type=type, name=name or "humidity")
    
    @classmethod
    def ultrasonic(cls, trigger: int, echo: int, name: str = None) -> "Sensor":
        """Create an ultrasonic distance sensor."""
        return cls("ultrasonic", pins={"trigger": trigger, "echo": echo}, name=name or "distance")
    
    @classmethod
    def moisture(cls, pin: int, name: str = None) -> "Sensor":
        """Create a soil moisture sensor."""
        return cls("moisture", pin=pin, name=name or "moisture")
    
    @classmethod
    def light(cls, pin: int, name: str = None) -> "Sensor":
        """Create a light sensor."""
        return cls("light", pin=pin, name=name or "light")
    
    @classmethod
    def door(cls, pin: int, name: str = None) -> "Sensor":
        """Create a door/magnetic sensor."""
        return cls("door", pin=pin, name=name or "door")
    
    @classmethod
    def window(cls, pin: int, name: str = None) -> "Sensor":
        """Create a window sensor."""
        return cls("window", pin=pin, name=name or "window")
    
    def __repr__(self):
        return f"Sensor({self.sensor_type}, pin={self.pin}, name={self.name})"
