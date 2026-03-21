"""
Ludwig IoT - Pin abstraction for different hardware boards
"""

from typing import Any, Callable, Optional, Literal
from dataclasses import dataclass
from enum import Enum
import platform
import sys


class Board(Enum):
    """Supported hardware boards."""
    RASPBERRY_PI = "raspberry_pi"
    ESP32 = "esp32"
    ARDUINO = "arduino"  # Via serial
    SIMULATION = "simulation"  # For testing


def detect_board() -> Board:
    """Auto-detect the current hardware board."""
    try:
        # Check for Raspberry Pi
        with open("/proc/cpuinfo") as f:
            if "Raspberry Pi" in f.read():
                return Board.RASPBERRY_PI
    except:
        pass
    
    # Check for MicroPython (ESP32)
    if sys.implementation.name == "micropython":
        return Board.ESP32
    
    # Default to simulation for development
    return Board.SIMULATION


class Pin:
    """
    Hardware-agnostic GPIO pin.
    
    Works on Raspberry Pi, ESP32, Arduino, or simulation mode.
    
    Example:
        led = Pin(17, mode="output")
        led.on()
        led.off()
        led.toggle()
        
        button = Pin(4, mode="input", pull="up")
        if button.read():
            print("Button pressed!")
        
        @button.on_change
        def button_changed(value):
            print(f"Button: {value}")
    """
    
    # Class-level board detection (lazy)
    _board: Optional[Board] = None
    _gpio = None
    
    def __init__(
        self,
        number: int,
        mode: Literal["input", "output"] = "output",
        pull: Literal["up", "down", "none"] = "none",
        name: Optional[str] = None,
    ):
        self.number = number
        self.mode = mode
        self.pull = pull
        self.name = name or f"pin_{number}"
        
        self._value = False
        self._callbacks: list[Callable] = []
        
        self._setup()
    
    @classmethod
    def _get_board(cls) -> Board:
        if cls._board is None:
            cls._board = detect_board()
        return cls._board
    
    @classmethod
    def _get_gpio(cls):
        if cls._gpio is not None:
            return cls._gpio
        
        board = cls._get_board()
        
        if board == Board.RASPBERRY_PI:
            try:
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                cls._gpio = GPIO
            except ImportError:
                print("Warning: RPi.GPIO not found, using simulation")
                cls._gpio = None
        elif board == Board.ESP32:
            try:
                from machine import Pin as MachinePin
                cls._gpio = MachinePin
            except ImportError:
                cls._gpio = None
        else:
            cls._gpio = None
        
        return cls._gpio
    
    def _setup(self):
        """Initialize the pin on hardware."""
        gpio = self._get_gpio()
        board = self._get_board()
        
        if gpio is None:
            # Simulation mode
            return
        
        if board == Board.RASPBERRY_PI:
            if self.mode == "output":
                gpio.setup(self.number, gpio.OUT)
            else:
                pull_mode = gpio.PUD_OFF
                if self.pull == "up":
                    pull_mode = gpio.PUD_UP
                elif self.pull == "down":
                    pull_mode = gpio.PUD_DOWN
                gpio.setup(self.number, gpio.IN, pull_up_down=pull_mode)
        
        elif board == Board.ESP32:
            # MicroPython style
            if self.mode == "output":
                self._pin = gpio(self.number, gpio.OUT)
            else:
                pull_mode = None
                if self.pull == "up":
                    pull_mode = gpio.PULL_UP
                elif self.pull == "down":
                    pull_mode = gpio.PULL_DOWN
                self._pin = gpio(self.number, gpio.IN, pull_mode)
    
    def on(self):
        """Set pin HIGH."""
        self.write(True)
    
    def off(self):
        """Set pin LOW."""
        self.write(False)
    
    def toggle(self):
        """Toggle pin state."""
        self.write(not self._value)
    
    def write(self, value: bool):
        """Write a value to the pin."""
        self._value = value
        gpio = self._get_gpio()
        board = self._get_board()
        
        if gpio is None:
            # Simulation
            print(f"[SIM] {self.name}: {'HIGH' if value else 'LOW'}")
            return
        
        if board == Board.RASPBERRY_PI:
            gpio.output(self.number, value)
        elif board == Board.ESP32:
            self._pin.value(1 if value else 0)
    
    def read(self) -> bool:
        """Read the pin value."""
        gpio = self._get_gpio()
        board = self._get_board()
        
        if gpio is None:
            return self._value
        
        if board == Board.RASPBERRY_PI:
            return bool(gpio.input(self.number))
        elif board == Board.ESP32:
            return bool(self._pin.value())
        
        return self._value
    
    def on_change(self, callback: Callable):
        """
        Register a callback for pin state changes.
        
        Example:
            @button.on_change
            def handle(value):
                print(f"Button: {value}")
        """
        self._callbacks.append(callback)
        
        gpio = self._get_gpio()
        board = self._get_board()
        
        if gpio and board == Board.RASPBERRY_PI:
            def wrapped(channel):
                value = self.read()
                for cb in self._callbacks:
                    cb(value)
            gpio.add_event_detect(
                self.number, 
                gpio.BOTH, 
                callback=wrapped, 
                bouncetime=200
            )
        
        return callback
    
    def pwm(self, frequency: int = 1000) -> "PWM":
        """Create a PWM instance for this pin."""
        return PWM(self, frequency)
    
    def __repr__(self):
        return f"Pin({self.number}, mode={self.mode}, name={self.name})"


class PWM:
    """Pulse Width Modulation for analog-like output."""
    
    def __init__(self, pin: Pin, frequency: int = 1000):
        self.pin = pin
        self.frequency = frequency
        self._duty = 0
        self._pwm = None
        
        self._setup()
    
    def _setup(self):
        gpio = Pin._get_gpio()
        board = Pin._get_board()
        
        if gpio is None:
            return
        
        if board == Board.RASPBERRY_PI:
            self._pwm = gpio.PWM(self.pin.number, self.frequency)
            self._pwm.start(0)
        elif board == Board.ESP32:
            from machine import PWM as MachinePWM
            self._pwm = MachinePWM(self.pin._pin, freq=self.frequency)
    
    def duty(self, percent: float):
        """
        Set duty cycle (0-100%).
        
        Example:
            led_pwm.duty(50)  # 50% brightness
        """
        self._duty = max(0, min(100, percent))
        
        if self._pwm is None:
            print(f"[SIM] {self.pin.name} PWM: {self._duty}%")
            return
        
        board = Pin._get_board()
        
        if board == Board.RASPBERRY_PI:
            self._pwm.ChangeDutyCycle(self._duty)
        elif board == Board.ESP32:
            # ESP32 uses 0-1023
            self._pwm.duty(int(self._duty * 10.23))
    
    def stop(self):
        """Stop PWM."""
        if self._pwm:
            self._pwm.stop() if hasattr(self._pwm, 'stop') else self._pwm.deinit()
