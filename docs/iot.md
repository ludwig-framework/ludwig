# IoT Development with Ludwig

Build robots, alarms, smart homes, and more with Ludwig's IoT modules.

## Platform Support

Ludwig works on multiple platforms with automatic fallback:

| Platform | Status |
|----------|--------|
| Raspberry Pi | ✅ Full support |
| ESP32 | ✅ Full support |
| Arduino | ✅ Basic support |
| Desktop | ✅ Simulation mode |

When hardware isn't available, Ludwig runs in simulation mode so you can develop and test anywhere.

## GPIO Basics

### Pin Control

```python
from ludwig.iot import Pin

# Output pin
led = Pin(17, mode="out")
led.on()
led.off()
led.toggle()

# Input pin
button = Pin(18, mode="in", pull="up")
if button.read():
    print("Button pressed!")

# PWM
pwm = Pin(12, mode="pwm")
pwm.duty(50)  # 50% duty cycle
```

## Sensors

### Motion Sensor

```python
from ludwig.iot import Sensor

motion = Sensor.motion(pin=4)

if motion.read():
    print("Motion detected!")

# Continuous monitoring
motion.on_trigger(lambda: print("Motion!"))
motion.run()
```

### Temperature Sensor

```python
temp = Sensor.temperature(pin=7)
print(f"Temperature: {temp.read()}°C")
```

### Ultrasonic Distance

```python
distance = Sensor.ultrasonic(trigger=24, echo=25)
print(f"Distance: {distance.read()} cm")
```

### Other Sensors

```python
# Door/window contact sensor
door = Sensor.door(pin=5)

# Window sensor
window = Sensor.window(pin=6)

# Soil moisture
moisture = Sensor.moisture(pin=0)  # Analog pin
```

## Actuators

### Motors

```python
from ludwig.iot import Motor

motor = Motor(forward=17, backward=18, enable=12)
motor.forward(speed=75)  # 75% speed
motor.backward(speed=50)
motor.stop()
```

### Lights

```python
from ludwig.iot import Light

# Simple on/off
light = Light(pin=17)
light.on()
light.off()

# Dimmable
light = Light(pin=17, dimmable=True)
light.brightness(70)  # 70%
```

### Servo Motors

```python
from ludwig.iot import Servo

servo = Servo(pin=18)
servo.angle(90)   # Move to 90°
servo.angle(0)    # Move to 0°
servo.angle(180)  # Move to 180°
```

### Relays

```python
from ludwig.iot import Relay

relay = Relay(pin=17)
relay.on()
relay.off()
```

### Buzzers

```python
from ludwig.iot import Buzzer

buzzer = Buzzer(pin=17)
buzzer.beep(duration=0.5)
buzzer.tone(frequency=1000, duration=1.0)
```

## Robot Cars

Build a robot car with obstacle avoidance:

```python
from ludwig.iot import Robot, Sensor

# Create robot with left and right motors
robot = Robot.car(
    left={"forward": 17, "backward": 18, "enable": 12},
    right={"forward": 22, "backward": 23, "enable": 13},
)

# Add front distance sensor
robot.add_sensor("front", Sensor.ultrasonic(trigger=24, echo=25))

# Movement commands
robot.forward(speed=50)
robot.backward(speed=50)
robot.turn(90)   # Turn right 90°
robot.turn(-90)  # Turn left 90°
robot.stop()

# Obstacle avoidance
@robot.on_obstacle
def avoid():
    robot.stop()
    robot.backward(duration=0.5)
    robot.turn(90)
    robot.forward()

# Start with obstacle detection
robot.run(obstacle_distance=20)  # Stop if obstacle within 20cm
```

## Robot Arms

```python
robot = Robot.arm(
    base=18,      # Base rotation servo
    shoulder=19,  # Shoulder servo
    elbow=20,     # Elbow servo
    gripper=21,   # Gripper servo
)

robot.move(base=90, shoulder=45, elbow=30)
robot.grip()
robot.release()
```

## Security Alarms

```python
from ludwig.iot import Alarm, Sensor

alarm = Alarm()

# Add sensors to zones
alarm.add(Sensor.motion(pin=4), zone="living_room")
alarm.add(Sensor.door(pin=5), zone="front_door")
alarm.add(Sensor.window(pin=6), zone="bedroom_window")

# Add siren output
alarm.siren(pin=17)

# Alert handler
@alarm.on_triggered
def alert(zone, sensor):
    print(f"🚨 ALERT: {zone}")
    
    # Send notifications
    alarm.send_sms("+1234567890", f"Alarm in {zone}!")
    alarm.send_email("you@example.com", "Alarm", f"Triggered in {zone}")

# Arm the system
alarm.arm()

# Or arm specific zones
alarm.arm(zones=["front_door", "living_room"])

# Disarm
alarm.disarm()

# Run monitoring loop
alarm.run()
```

## Smart Home

```python
from ludwig.iot import Home, Light, Sensor

home = Home()

# Create rooms
living = home.room("living_room")
living.add(Light(pin=17, name="ceiling", dimmable=True))
living.add(Light(pin=18, name="lamp"))
living.add(Sensor.motion(pin=4))
living.add(Sensor.temperature(pin=7))

bedroom = home.room("bedroom")
bedroom.add(Light(pin=19, name="main"))

# Automations

@home.at("sunset")
def evening_mode():
    living.light("ceiling").on()
    living.light("ceiling").brightness(70)

@home.at("23:00")
def bedtime():
    home.all_lights_off()

@home.at("07:00")
def morning():
    bedroom.light("main").on()

# Motion-triggered automation
@home.when(lambda: living.motion.read())
def motion_light():
    if not living.light("ceiling").is_on:
        living.light("ceiling").on()

# Temperature-based automation
@home.when(lambda: living.temperature.read() > 25)
def too_hot():
    # Turn on fan or AC
    pass

# Run home automation
home.run()
```

### Thermostat

```python
from ludwig.iot import Thermostat

thermo = Thermostat(
    temp_sensor=Sensor.temperature(pin=7),
    heater=Relay(pin=17),
    cooler=Relay(pin=18),
)

thermo.target = 22  # Target 22°C
thermo.run()
```

## Garden Automation

```python
from ludwig.iot import Garden

garden = Garden()

# Add plants with moisture sensors and pumps
garden.add_plant(
    "tomatoes",
    moisture_pin=0,    # Analog moisture sensor
    pump_pin=17,       # Water pump relay
    threshold=30,      # Water when below 30%
)

garden.add_plant("herbs", moisture_pin=1, pump_pin=18, threshold=40)
garden.add_plant("flowers", moisture_pin=2, pump_pin=19, threshold=35)

# Scheduled check
@garden.check_every(hours=1)
def water_check(plant):
    if plant.needs_water:
        plant.water(seconds=10)
        garden.log(f"Watered {plant.name}")

# Morning status report
@garden.at("06:00")
def morning_report():
    for plant in garden.plants:
        print(f"{plant.name}: {plant.moisture}%")

garden.run()
```

## Camera Integration

```python
from ludwig.iot import Camera

cam = Camera(0)  # Camera index or path

# Capture photo
cam.capture("photo.jpg")

# Record video
cam.record("video.mp4", duration=10)

# Motion detection
@cam.on_motion
def motion_detected(frame):
    cam.capture(f"motion_{time.time()}.jpg")

cam.run()
```

## Tips

### Pin Numbering

Ludwig uses BCM pin numbering on Raspberry Pi:

```python
# GPIO17 = BCM pin 17 = Physical pin 11
led = Pin(17, mode="out")
```

### Simulation Mode

On desktop, hardware calls are simulated:

```python
# This works on any machine
led = Pin(17, mode="out")
led.on()  # Prints: [SIM] Pin 17 -> HIGH
```

### Error Handling

```python
try:
    sensor = Sensor.temperature(pin=7)
    temp = sensor.read()
except Exception as e:
    print(f"Sensor error: {e}")
    temp = None
```

### Cleanup

```python
from ludwig.iot import cleanup

# Clean up all GPIO on exit
import atexit
atexit.register(cleanup)
```
