"""
Ludwig IoT - Actuators (motors, lights, servos, etc.)
"""

from typing import Optional
from ludwig.iot.pin import Pin, PWM
import time


class Light:
    """
    Simple light/LED control.
    
    Example:
        light = Light(pin=17, name="living_room")
        light.on()
        light.off()
        light.brightness(50)  # 50%
        light.blink(times=3)
    """
    
    def __init__(self, pin: int, name: str = None, dimmable: bool = False):
        self.pin_num = pin
        self.name = name or f"light_{pin}"
        self.dimmable = dimmable
        
        self._pin = Pin(pin, mode="output", name=self.name)
        self._pwm: Optional[PWM] = None
        self._state = False
        self._brightness = 100
        
        if dimmable:
            self._pwm = self._pin.pwm()
    
    def on(self, duration: int = None):
        """
        Turn light on.
        
        Args:
            duration: Auto-off after seconds (optional)
        """
        self._state = True
        if self._pwm:
            self._pwm.duty(self._brightness)
        else:
            self._pin.on()
        
        # TODO: Handle duration with scheduler
    
    def off(self):
        """Turn light off."""
        self._state = False
        if self._pwm:
            self._pwm.duty(0)
        else:
            self._pin.off()
    
    def toggle(self):
        """Toggle light state."""
        if self._state:
            self.off()
        else:
            self.on()
    
    def brightness(self, percent: float):
        """Set brightness (0-100%)."""
        self._brightness = max(0, min(100, percent))
        if self._pwm and self._state:
            self._pwm.duty(self._brightness)
    
    def blink(self, times: int = 3, interval: float = 0.5):
        """Blink the light."""
        for _ in range(times):
            self.on()
            time.sleep(interval)
            self.off()
            time.sleep(interval)
    
    @property
    def is_on(self) -> bool:
        return self._state
    
    def __repr__(self):
        return f"Light(pin={self.pin_num}, name={self.name}, on={self._state})"


class Motor:
    """
    DC Motor control with optional speed control.
    
    Example:
        # Simple motor
        motor = Motor(pin=18)
        motor.forward()
        motor.stop()
        
        # Motor with speed control
        motor = Motor(pin=18, enable=12)
        motor.forward(speed=50)  # 50% speed
        
        # H-bridge motor (forward/backward)
        motor = Motor(forward=17, backward=18, enable=12)
        motor.forward(speed=75)
        motor.backward(speed=50)
    """
    
    def __init__(
        self,
        pin: int = None,
        forward: int = None,
        backward: int = None,
        enable: int = None,
        name: str = None,
    ):
        self.name = name or "motor"
        
        # Simple single-direction motor
        if pin:
            self._forward_pin = Pin(pin, mode="output")
            self._backward_pin = None
        else:
            # H-bridge motor
            self._forward_pin = Pin(forward, mode="output") if forward else None
            self._backward_pin = Pin(backward, mode="output") if backward else None
        
        # Speed control
        self._enable_pin = Pin(enable, mode="output") if enable else None
        self._pwm = self._enable_pin.pwm() if self._enable_pin else None
        
        self._speed = 0
        self._direction = "stopped"
    
    def forward(self, speed: int = 100):
        """Run motor forward."""
        self._direction = "forward"
        self._speed = speed
        
        if self._backward_pin:
            self._backward_pin.off()
        if self._forward_pin:
            self._forward_pin.on()
        
        if self._pwm:
            self._pwm.duty(speed)
        elif self._enable_pin:
            self._enable_pin.on()
    
    def backward(self, speed: int = 100):
        """Run motor backward."""
        if not self._backward_pin:
            print(f"Warning: {self.name} doesn't support backward")
            return
        
        self._direction = "backward"
        self._speed = speed
        
        self._forward_pin.off()
        self._backward_pin.on()
        
        if self._pwm:
            self._pwm.duty(speed)
        elif self._enable_pin:
            self._enable_pin.on()
    
    def stop(self):
        """Stop the motor."""
        self._direction = "stopped"
        self._speed = 0
        
        if self._forward_pin:
            self._forward_pin.off()
        if self._backward_pin:
            self._backward_pin.off()
        if self._pwm:
            self._pwm.duty(0)
        elif self._enable_pin:
            self._enable_pin.off()
    
    def speed(self, percent: int):
        """Set motor speed (0-100%)."""
        self._speed = max(0, min(100, percent))
        if self._pwm:
            self._pwm.duty(self._speed)
    
    def __repr__(self):
        return f"Motor(name={self.name}, direction={self._direction}, speed={self._speed})"


class Servo:
    """
    Servo motor control (0-180 degrees).
    
    Example:
        servo = Servo(pin=18)
        servo.angle(90)   # Center
        servo.angle(0)    # Left
        servo.angle(180)  # Right
    """
    
    def __init__(self, pin: int, name: str = None, min_pulse: int = 500, max_pulse: int = 2500):
        self.pin_num = pin
        self.name = name or f"servo_{pin}"
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        
        self._pin = Pin(pin, mode="output")
        self._pwm = self._pin.pwm(frequency=50)  # 50Hz for servos
        self._angle = 90
    
    def angle(self, degrees: float):
        """Set servo angle (0-180 degrees)."""
        self._angle = max(0, min(180, degrees))
        
        # Convert angle to duty cycle
        # For 50Hz: period = 20ms, pulse range is ~0.5-2.5ms (2.5-12.5% duty)
        pulse_range = self.max_pulse - self.min_pulse
        pulse = self.min_pulse + (self._angle / 180) * pulse_range
        duty = (pulse / 20000) * 100  # Convert to percentage
        
        self._pwm.duty(duty)
    
    def center(self):
        """Move to center position (90 degrees)."""
        self.angle(90)
    
    def sweep(self, start: int = 0, end: int = 180, step: int = 5, delay: float = 0.05):
        """Sweep servo from start to end angle."""
        current = start
        direction = 1 if end > start else -1
        
        while (direction > 0 and current <= end) or (direction < 0 and current >= end):
            self.angle(current)
            time.sleep(delay)
            current += step * direction
    
    def __repr__(self):
        return f"Servo(pin={self.pin_num}, angle={self._angle})"


class Relay:
    """
    Relay control for high-power devices.
    
    Example:
        pump = Relay(pin=17, name="water_pump")
        pump.on()
        pump.off()
    """
    
    def __init__(self, pin: int, name: str = None, active_low: bool = False):
        self.pin_num = pin
        self.name = name or f"relay_{pin}"
        self.active_low = active_low
        
        self._pin = Pin(pin, mode="output")
        self._state = False
        
        # Start in off state
        self.off()
    
    def on(self):
        """Activate relay."""
        self._state = True
        if self.active_low:
            self._pin.off()
        else:
            self._pin.on()
    
    def off(self):
        """Deactivate relay."""
        self._state = False
        if self.active_low:
            self._pin.on()
        else:
            self._pin.off()
    
    def toggle(self):
        """Toggle relay state."""
        if self._state:
            self.off()
        else:
            self.on()
    
    @property
    def is_on(self) -> bool:
        return self._state
    
    def __repr__(self):
        return f"Relay(pin={self.pin_num}, name={self.name}, on={self._state})"


class Buzzer:
    """
    Buzzer/speaker control.
    
    Example:
        buzzer = Buzzer(pin=18)
        buzzer.beep()
        buzzer.tone(440, duration=0.5)  # A4 note
        buzzer.alarm()
    """
    
    def __init__(self, pin: int, name: str = None):
        self.pin_num = pin
        self.name = name or f"buzzer_{pin}"
        
        self._pin = Pin(pin, mode="output")
        self._pwm = self._pin.pwm()
    
    def on(self):
        """Turn buzzer on."""
        self._pwm.duty(50)
    
    def off(self):
        """Turn buzzer off."""
        self._pwm.duty(0)
    
    def beep(self, duration: float = 0.2, frequency: int = 1000):
        """Short beep."""
        self.tone(frequency, duration)
    
    def tone(self, frequency: int, duration: float = 0.5):
        """Play a tone at given frequency."""
        # Would need to change PWM frequency on real hardware
        self.on()
        time.sleep(duration)
        self.off()
    
    def alarm(self, cycles: int = 5):
        """Play alarm sound."""
        for _ in range(cycles):
            self.tone(1000, 0.2)
            time.sleep(0.1)
            self.tone(1500, 0.2)
            time.sleep(0.1)
    
    def melody(self, notes: list[tuple[int, float]]):
        """
        Play a melody.
        
        Args:
            notes: List of (frequency, duration) tuples
        """
        for freq, duration in notes:
            if freq > 0:
                self.tone(freq, duration)
            else:
                time.sleep(duration)  # Rest
    
    def __repr__(self):
        return f"Buzzer(pin={self.pin_num})"
