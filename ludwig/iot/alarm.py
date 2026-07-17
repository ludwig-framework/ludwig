"""
Ludwig IoT - Alarm system for home security
"""

from typing import Callable, Optional
from ludwig.iot.sensor import Sensor
from ludwig.iot.actuators import Buzzer, Light, Relay
import time


class Alarm:
    """
    Home security alarm system.
    
    Example:
        alarm = Alarm()
        
        # Add sensors
        alarm.add(Sensor.motion(pin=4), zone="living_room")
        alarm.add(Sensor.door(pin=5), zone="front_door")
        alarm.add(Sensor.window(pin=6), zone="bedroom")
        
        # Add siren
        alarm.siren(pin=17)
        
        # What happens when triggered
        @alarm.on_triggered
        def alert(zone, sensor):
            print(f"Intruder in {zone}!")
            alarm.send_sms("+233501234567", f"Alert: {zone}")
            alarm.notify_app()
        
        # Arm and run
        alarm.arm()
        alarm.run()
    """
    
    def __init__(self, name: str = "alarm"):
        self.name = name
        self._sensors: list[tuple[Sensor, str]] = []  # (sensor, zone)
        self._siren: Optional[Buzzer] = None
        self._strobe: Optional[Light] = None
        self._callbacks: dict[str, list[Callable]] = {}
        
        self._armed = False
        self._triggered = False
        self._running = False
        
        # Entry/exit delay
        self.entry_delay = 30  # seconds
        self.exit_delay = 30  # seconds
    
    def add(self, sensor: Sensor, zone: str = "default"):
        """Add a sensor to the alarm system."""
        self._sensors.append((sensor, zone))
    
    def siren(self, pin: int = None, buzzer: Buzzer = None):
        """Set up siren/buzzer."""
        if buzzer:
            self._siren = buzzer
        elif pin:
            self._siren = Buzzer(pin, name="siren")
    
    def strobe(self, pin: int = None, light: Light = None):
        """Set up strobe light."""
        if light:
            self._strobe = light
        elif pin:
            self._strobe = Light(pin, name="strobe")
    
    # === Arming ===
    
    def arm(self, mode: str = "away"):
        """
        Arm the alarm.
        
        Args:
            mode: "away" (all sensors), "home" (perimeter only), "night"
        """
        print(f"⚠️  Arming in {self.exit_delay} seconds...")
        
        # Exit delay countdown
        for i in range(self.exit_delay, 0, -1):
            if self._siren:
                self._siren.beep(duration=0.1)
            time.sleep(1)
        
        self._armed = True
        self._triggered = False
        print(f"🔒 Alarm armed ({mode} mode)")
        
        if self._siren:
            self._siren.beep(duration=0.5)
    
    def disarm(self, code: str = None):
        """Disarm the alarm."""
        # TODO: Verify code
        self._armed = False
        self._triggered = False
        
        if self._siren:
            self._siren.off()
        if self._strobe:
            self._strobe.off()
        
        print("🔓 Alarm disarmed")
    
    def trigger(self, zone: str, sensor: Sensor):
        """Trigger the alarm."""
        if not self._armed or self._triggered:
            return
        
        print(f"🚨 ALARM TRIGGERED: {zone}")
        self._triggered = True
        
        # Activate siren and strobe
        if self._siren:
            self._siren.alarm()
        if self._strobe:
            self._strobe.blink(times=10, interval=0.2)
        
        # Call handlers
        for handler in self._callbacks.get("triggered", []):
            handler(zone, sensor)
    
    # === Events ===
    
    def on(self, event: str):
        """Register event handler."""
        def decorator(func: Callable):
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(func)
            return func
        return decorator
    
    @property
    def on_triggered(self):
        """Handler for alarm trigger."""
        return self.on("triggered")
    
    @property
    def on_armed(self):
        """Handler for arming."""
        return self.on("armed")
    
    @property
    def on_disarmed(self):
        """Handler for disarming."""
        return self.on("disarmed")
    
    @property
    def is_armed(self) -> bool:
        """Check if alarm is armed."""
        return self._armed
    
    # === Notifications ===
    
    def send_sms(self, phone: str, message: str):
        """Send SMS notification."""
        # TODO: Integrate with Twilio/Vonage
        print(f"📱 SMS to {phone}: {message}")
    
    def send_email(self, email: str, subject: str, body: str):
        """Send email notification."""
        # TODO: Integrate with email service
        print(f"📧 Email to {email}: {subject}")
    
    def notify_app(self, message: str = "Alarm triggered!"):
        """Send push notification to app."""
        # TODO: Integrate with push service
        print(f"📲 Push: {message}")
    
    def call(self, phone: str, message: str = None):
        """Make phone call."""
        # TODO: Integrate with voice API
        print(f"📞 Calling {phone}")
    
    # === Run Loop ===
    
    def run(self):
        """Start monitoring sensors."""
        self._running = True
        print(f"👁️  Monitoring {len(self._sensors)} sensors...")
        
        try:
            while self._running:
                if self._armed:
                    for sensor, zone in self._sensors:
                        if sensor.read():  # Sensor triggered
                            self.trigger(zone, sensor)
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.disarm()
            print("\n👁️  Monitoring stopped")
    
    def stop(self):
        """Stop the alarm system."""
        self._running = False
        self.disarm()
    
    @property
    def status(self) -> dict:
        """Get current alarm status."""
        return {
            "armed": self._armed,
            "triggered": self._triggered,
            "sensors": len(self._sensors),
            "zones": list(set(zone for _, zone in self._sensors))
        }
    
    def __repr__(self):
        return f"Alarm(name={self.name}, armed={self._armed}, sensors={len(self._sensors)})"
