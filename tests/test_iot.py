"""
Tests for Ludwig IoT modules
"""

import pytest
from ludwig.iot import Pin, Sensor, Motor, Light, Robot, Alarm


class TestPin:
    """Test Pin class (simulation mode)."""
    
    def test_pin_creation(self):
        """Test creating output pin."""
        pin = Pin(17, mode="out")
        assert pin is not None
    
    def test_pin_output(self):
        """Test pin output operations."""
        pin = Pin(17, mode="out")
        pin.on()
        pin.off()
        pin.toggle()
    
    def test_pin_input(self):
        """Test pin input operations."""
        pin = Pin(18, mode="in")
        value = pin.read()
        assert value in (0, 1, True, False)


class TestSensor:
    """Test Sensor class."""
    
    def test_motion_sensor(self):
        """Test motion sensor factory."""
        sensor = Sensor.motion(pin=4)
        assert sensor is not None
        assert sensor.type == "motion"
    
    def test_temperature_sensor(self):
        """Test temperature sensor factory."""
        sensor = Sensor.temperature(pin=7)
        assert sensor is not None
        value = sensor.read()
        assert isinstance(value, (int, float))
    
    def test_ultrasonic_sensor(self):
        """Test ultrasonic distance sensor."""
        sensor = Sensor.ultrasonic(trigger=24, echo=25)
        assert sensor is not None
        distance = sensor.read()
        assert isinstance(distance, (int, float))


class TestActuators:
    """Test actuator classes."""
    
    def test_motor(self):
        """Test Motor class."""
        motor = Motor(forward=17, backward=18, enable=12)
        motor.forward(speed=50)
        motor.backward(speed=75)
        motor.stop()
    
    def test_light(self):
        """Test Light class."""
        light = Light(pin=17)
        light.on()
        assert light.is_on
        light.off()
        assert not light.is_on
    
    def test_dimmable_light(self):
        """Test dimmable Light."""
        light = Light(pin=17, dimmable=True)
        light.brightness(50)
        light.brightness(100)


class TestRobot:
    """Test Robot class."""
    
    def test_robot_car_creation(self):
        """Test creating robot car."""
        robot = Robot.car(
            left={"forward": 17, "backward": 18, "enable": 12},
            right={"forward": 22, "backward": 23, "enable": 13},
        )
        assert robot is not None
    
    def test_robot_movement(self):
        """Test robot movement."""
        robot = Robot.car(
            left={"forward": 17, "backward": 18},
            right={"forward": 22, "backward": 23},
        )
        robot.forward(speed=50)
        robot.backward(speed=50)
        robot.turn(90)
        robot.stop()


class TestAlarm:
    """Test Alarm class."""
    
    def test_alarm_creation(self):
        """Test creating alarm system."""
        alarm = Alarm()
        assert alarm is not None
    
    def test_add_sensors(self):
        """Test adding sensors to zones."""
        alarm = Alarm()
        alarm.add(Sensor.motion(pin=4), zone="living_room")
        alarm.add(Sensor.door(pin=5), zone="front_door")
    
    def test_arm_disarm(self):
        """Test arming and disarming."""
        alarm = Alarm()
        alarm.arm()
        assert alarm.is_armed
        alarm.disarm()
        assert not alarm.is_armed
