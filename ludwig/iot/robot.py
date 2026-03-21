"""
Ludwig IoT - Robot abstraction for wheeled robots, arms, etc.
"""

from typing import Optional, Callable, Literal
from dataclasses import dataclass, field
from ludwig.iot.actuators import Motor, Servo
from ludwig.iot.sensor import Sensor
import time


@dataclass
class WheelConfig:
    """Configuration for a wheel motor."""
    forward: int
    backward: int = None
    enable: int = None


class Robot:
    """
    High-level robot abstraction.
    
    Example:
        # Simple 2-wheel robot car
        robot = Robot.car(
            left={"forward": 17, "backward": 18, "enable": 12},
            right={"forward": 22, "backward": 23, "enable": 13},
        )
        
        robot.forward(speed=50)
        robot.turn(90)  # Turn right 90 degrees
        robot.backward()
        robot.stop()
        
        # Add obstacle detection
        robot.add_sensor("front", Sensor.ultrasonic(trigger=24, echo=25))
        
        @robot.on_obstacle
        def avoid():
            robot.stop()
            robot.backward(duration=0.5)
            robot.turn(180)
    """
    
    def __init__(
        self,
        name: str = "robot",
        wheels: dict[str, Motor] = None,
        sensors: dict[str, Sensor] = None,
    ):
        self.name = name
        self.wheels = wheels or {}
        self.sensors = sensors or {}
        
        self._callbacks: dict[str, list[Callable]] = {}
        self._running = False
    
    # === Factory Methods ===
    
    @classmethod
    def car(
        cls,
        left: dict = None,
        right: dict = None,
        sensors: dict = None,
        name: str = "robot_car",
    ) -> "Robot":
        """
        Create a 2-wheel differential drive robot.
        
        Args:
            left: Left motor config {"forward": pin, "backward": pin, "enable": pin}
            right: Right motor config
            sensors: Optional sensors dict
        """
        wheels = {}
        
        if left:
            wheels["left"] = Motor(
                forward=left.get("forward"),
                backward=left.get("backward"),
                enable=left.get("enable"),
                name="left_wheel"
            )
        
        if right:
            wheels["right"] = Motor(
                forward=right.get("forward"),
                backward=right.get("backward"),
                enable=right.get("enable"),
                name="right_wheel"
            )
        
        robot = cls(name=name, wheels=wheels)
        
        # Add sensors
        if sensors:
            for sensor_name, sensor in sensors.items():
                robot.sensors[sensor_name] = sensor
        
        return robot
    
    @classmethod
    def arm(cls, joints: list[int], name: str = "robot_arm") -> "Robot":
        """
        Create a robot arm with servo joints.
        
        Args:
            joints: List of servo pins for each joint
        """
        robot = cls(name=name)
        robot.joints = [Servo(pin, name=f"joint_{i}") for i, pin in enumerate(joints)]
        return robot
    
    # === Movement ===
    
    def forward(self, speed: int = 100, duration: float = None):
        """Move forward."""
        for wheel in self.wheels.values():
            wheel.forward(speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def backward(self, speed: int = 100, duration: float = None):
        """Move backward."""
        for wheel in self.wheels.values():
            wheel.backward(speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def left(self, speed: int = 100, duration: float = None):
        """Turn left (tank turn)."""
        if "left" in self.wheels:
            self.wheels["left"].backward(speed)
        if "right" in self.wheels:
            self.wheels["right"].forward(speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def right(self, speed: int = 100, duration: float = None):
        """Turn right (tank turn)."""
        if "left" in self.wheels:
            self.wheels["left"].forward(speed)
        if "right" in self.wheels:
            self.wheels["right"].backward(speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn(self, angle: int, speed: int = 50):
        """
        Turn by a specific angle.
        
        Args:
            angle: Degrees to turn (positive = right, negative = left)
            speed: Turn speed
        """
        # Rough estimate: 1 second = 90 degrees at speed 50
        duration = abs(angle) / 90 * (50 / speed)
        
        if angle > 0:
            self.right(speed, duration)
        else:
            self.left(speed, duration)
    
    def stop(self):
        """Stop all motors."""
        for wheel in self.wheels.values():
            wheel.stop()
    
    def speed(self, percent: int):
        """Set speed for all wheels."""
        for wheel in self.wheels.values():
            wheel.speed(percent)
    
    # === Sensors ===
    
    def add_sensor(self, name: str, sensor: Sensor):
        """Add a sensor to the robot."""
        self.sensors[name] = sensor
    
    def distance(self, sensor_name: str = None) -> float:
        """
        Get distance from ultrasonic sensor.
        
        Args:
            sensor_name: Name of sensor (defaults to first ultrasonic)
        """
        if sensor_name:
            return self.sensors[sensor_name].read()
        
        # Find first ultrasonic sensor
        for sensor in self.sensors.values():
            if sensor.sensor_type == "ultrasonic":
                return sensor.read()
        
        return -1
    
    # === Events ===
    
    def on(self, event: str):
        """Register an event handler."""
        def decorator(func: Callable):
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(func)
            return func
        return decorator
    
    @property
    def on_obstacle(self):
        """Handler for obstacle detection."""
        return self.on("obstacle")
    
    def emit(self, event: str, *args, **kwargs):
        """Trigger event handlers."""
        for handler in self._callbacks.get(event, []):
            handler(*args, **kwargs)
    
    # === Run Loop ===
    
    def run(self, obstacle_distance: float = 20):
        """
        Start the robot's main loop.
        
        Args:
            obstacle_distance: Distance (cm) to trigger obstacle event
        """
        self._running = True
        print(f"🤖 {self.name} running... (Ctrl+C to stop)")
        
        try:
            while self._running:
                # Check for obstacles
                dist = self.distance()
                if dist > 0 and dist < obstacle_distance:
                    self.emit("obstacle", dist)
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
            print(f"\n🤖 {self.name} stopped")
    
    def shutdown(self):
        """Stop robot and cleanup."""
        self._running = False
        self.stop()
    
    # === Arm Methods (if applicable) ===
    
    def move_joint(self, joint_index: int, angle: float):
        """Move a specific joint to an angle."""
        if hasattr(self, 'joints') and joint_index < len(self.joints):
            self.joints[joint_index].angle(angle)
    
    def home(self):
        """Move all joints to home position (90 degrees)."""
        if hasattr(self, 'joints'):
            for joint in self.joints:
                joint.center()
    
    def __repr__(self):
        return f"Robot(name={self.name}, wheels={list(self.wheels.keys())}, sensors={list(self.sensors.keys())})"
