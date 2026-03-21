# Ludwig API Reference

Complete API documentation for Ludwig v2.0.

## Core

### App

The main application class.

```python
from ludwig import App

app = App(
    name="My App",     # Application name
    host="0.0.0.0",    # Server host
    port=8000,         # Server port
    debug=False,       # Debug mode
    static_dir=None,   # Static files directory
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `app.get(path)` | Register GET route |
| `app.post(path)` | Register POST route |
| `app.put(path)` | Register PUT route |
| `app.delete(path)` | Register DELETE route |
| `app.api(path)` | Register JSON API route |
| `app.on(event)` | Register event handler |
| `app.every(interval)` | Register scheduled task |
| `app.at(time)` | Register time-based task |
| `app.run()` | Start the server |

---

## Web

### Request

```python
@app.post("/example")
def handler(req):
    req.method      # "POST"
    req.path        # "/example"
    req.params      # URL parameters {"id": "123"}
    req.query       # Query params {"page": "1"}
    req.headers     # Request headers
    req.body        # Raw body string
    req.json        # Parsed JSON body
```

### Response

Routes can return:

```python
# Dict → JSON response
return {"status": "ok"}

# String → HTML/text response
return "<h1>Hello</h1>"

# Tuple → Response with status code
return {"error": "Not found"}, 404

# Response object
from ludwig.web import Response
return Response(body="Hello", status=200, headers={})
```

---

## Database

### Database

```python
from ludwig import Database

db = Database("app.db")              # SQLite
db = Database("postgres://...")      # PostgreSQL
```

#### Methods

| Method | Description |
|--------|-------------|
| `db.table(name)` | Start query builder |
| `db.query(sql, params)` | Execute raw SQL |
| `db.create_table(name, schema)` | Create table |
| `db.close()` | Close connection |

### QueryBuilder

```python
db.table("users")
    .select("id", "name")
    .where("age", ">", 18)
    .order_by("name", "ASC")
    .limit(10)
    .offset(5)
    .get()      # Returns list[dict]
    .first()    # Returns dict or None
    .count()    # Returns int
    .insert(data)   # Returns id
    .update(data)   # Returns affected rows
    .delete()       # Returns affected rows
```

### Model

```python
from ludwig import Model
from dataclasses import dataclass

@dataclass
class User(Model):
    name: str
    email: str
    age: int = 0
```

#### Class Methods

| Method | Description |
|--------|-------------|
| `User.all()` | Get all records |
| `User.find(id)` | Find by ID |
| `User.where(col, op, val)` | Query with condition |
| `User.create(**data)` | Create and save |

#### Instance Methods

| Method | Description |
|--------|-------------|
| `user.save()` | Insert or update |
| `user.delete()` | Delete record |
| `user.to_dict()` | Convert to dict |
| `user.to_json()` | Convert to JSON |

---

## IoT

### Pin

```python
from ludwig.iot import Pin

pin = Pin(17, mode="out")    # Output
pin = Pin(18, mode="in")     # Input
pin = Pin(12, mode="pwm")    # PWM

pin.on()           # Set HIGH
pin.off()          # Set LOW
pin.toggle()       # Toggle state
pin.read()         # Read value
pin.duty(50)       # Set PWM duty cycle (0-100)
```

### Sensor

Factory methods for common sensors:

```python
from ludwig.iot import Sensor

Sensor.motion(pin)              # PIR motion sensor
Sensor.temperature(pin)         # Temperature sensor
Sensor.ultrasonic(trigger, echo) # Distance sensor
Sensor.moisture(pin)            # Soil moisture (analog)
Sensor.door(pin)                # Door contact sensor
Sensor.window(pin)              # Window sensor
```

### Motor

```python
from ludwig.iot import Motor

motor = Motor(forward=17, backward=18, enable=12)
motor.forward(speed=100)
motor.backward(speed=50)
motor.stop()
```

### Light

```python
from ludwig.iot import Light

light = Light(pin=17)
light = Light(pin=17, dimmable=True)

light.on()
light.off()
light.toggle()
light.brightness(70)  # 0-100
light.is_on           # Property
```

### Servo

```python
from ludwig.iot import Servo

servo = Servo(pin=18)
servo.angle(90)  # 0-180 degrees
```

### Relay

```python
from ludwig.iot import Relay

relay = Relay(pin=17)
relay.on()
relay.off()
```

### Buzzer

```python
from ludwig.iot import Buzzer

buzzer = Buzzer(pin=17)
buzzer.beep(duration=0.5)
buzzer.tone(frequency=1000, duration=1.0)
```

### Robot

```python
from ludwig.iot import Robot

# Robot car
robot = Robot.car(
    left={"forward": 17, "backward": 18, "enable": 12},
    right={"forward": 22, "backward": 23, "enable": 13},
)

# Robot arm
robot = Robot.arm(base=18, shoulder=19, elbow=20, gripper=21)
```

#### Car Methods

| Method | Description |
|--------|-------------|
| `robot.forward(speed, duration)` | Move forward |
| `robot.backward(speed, duration)` | Move backward |
| `robot.turn(degrees)` | Turn right (positive) or left (negative) |
| `robot.stop()` | Stop all motors |
| `robot.add_sensor(name, sensor)` | Add distance sensor |
| `robot.run(obstacle_distance)` | Run with obstacle avoidance |

### Alarm

```python
from ludwig.iot import Alarm

alarm = Alarm()
alarm.add(sensor, zone="name")
alarm.siren(pin)

alarm.arm()
alarm.arm(zones=["front_door"])
alarm.disarm()
alarm.is_armed        # Property

@alarm.on_triggered
def handler(zone, sensor):
    pass

alarm.send_sms(phone, message)
alarm.send_email(to, subject, body)
alarm.run()
```

### Camera

```python
from ludwig.iot import Camera

cam = Camera(0)  # Index or path
cam.capture(filename)
cam.record(filename, duration)

@cam.on_motion
def handler(frame):
    pass

cam.run()
```

### Home

```python
from ludwig.iot import Home

home = Home()
room = home.room("name")
room.add(device)

home.all_lights_on()
home.all_lights_off()

@home.at("sunset")
@home.at("07:00")
@home.every(minutes=30)
@home.when(condition_fn)
def automation():
    pass

home.run()
```

### Garden

```python
from ludwig.iot import Garden

garden = Garden()
garden.add_plant(name, moisture_pin, pump_pin, threshold)

@garden.check_every(hours=1)
def check(plant):
    plant.name
    plant.moisture      # Current moisture %
    plant.needs_water   # Boolean
    plant.water(seconds)

@garden.at("06:00")
def morning():
    pass

garden.run()
```

---

## AI

### Assistant

```python
from ludwig.ai import Assistant

assistant = Assistant(
    name="Assistant",
    model="gpt-4o",
    voice="alloy",
    system_prompt="You are helpful",
    api_key=None,  # Uses OPENAI_API_KEY env var
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `assistant.chat(message, context)` | Send chat message |
| `assistant.listen()` | Speech to text |
| `assistant.speak(text)` | Text to speech |
| `assistant.clear_history()` | Clear conversation |
| `assistant.run()` | Start listening loop |

#### Decorators

```python
@assistant.on_wake("Hey Ludwig")
def handler():
    pass

@assistant.on_command("command text")
def handler():
    pass
```

### Vision

```python
from ludwig.ai import Vision

vision = Vision(
    camera=0,           # Camera index
    model="yolo",       # YOLO model
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `vision.detect()` | Detect objects in frame |
| `vision.capture()` | Capture current frame |
| `vision.run(display)` | Start detection loop |

#### Decorators

```python
@vision.on_detect("person")
@vision.on_detect(["person", "car"])
def handler(detection):
    detection.label
    detection.confidence
    detection.bbox
    detection.center
```

### Automator

```python
from ludwig.ai import Automator

auto = Automator()
auto.add_rule("natural language rule")
auto.set_context({"devices": {...}})

@auto.action("action_name")
def handler(*args):
    pass

auto.run()
```

---

## CLI

```bash
# Create new project
ludwig new <name> --template <template>

# Run development server
ludwig dev --port 8000 --host 0.0.0.0

# Run a file
ludwig run app.py

# Show version
ludwig version
```

### Templates

- `basic` - Simple web app
- `api` - REST API with database
- `web` - HTML web app
- `robot` - Robot car
- `alarm` - Security alarm
- `smart-home` - Home automation
- `garden` - Garden automation
- `assistant` - Voice assistant
- `vision` - Computer vision
