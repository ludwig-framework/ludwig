<p align="center">
  <img src="https://raw.githubusercontent.com/ludwig-framework/ludwig/main/assets/logo.png" alt="Ludwig Logo" width="160"/>
</p>

<h1 align="center">Ludwig</h1>
<p align="center"><strong>Simple Python for Web, IoT, and AI</strong></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://github.com/ludwig-framework/ludwig/stargazers"><img src="https://img.shields.io/github/stars/ludwig-framework/ludwig?style=flat&logo=github&color=yellow" alt="Stars"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.10+-blue" alt="Python 3.10+"></a>
</p>

---

## What is Ludwig?

Ludwig is a Python framework that makes building **anything** simple. One framework for Web APIs, IoT robots, smart home systems, AI assistants, and more — all in pure Python.

```python
# Build an API in 10 lines
from ludwig import App

app = App()

@app.get("/hello/:name")
def hello(req):
    return {"message": f"Hello, {req.params['name']}!"}

app.run()
```

---

## Why Ludwig?

- **Pure Python** — No custom syntax. No DSLs. Just Python.
- **Templates for Everything** — Start a robot, API, or smart home in seconds
- **Hardware Agnostic** — Works on Raspberry Pi, ESP32, Arduino, or simulation
- **AI Built-In** — Voice assistants, computer vision, automation
- **Minimal Dependencies** — Core framework has zero external dependencies

---

## Quick Start

```bash
pip install ludwig
ludwig new my-project --template api
cd my-project
python app.py
```

### Available Templates

| Template | Description |
|----------|-------------|
| `basic` | Simple web app |
| `api` | REST API with database |
| `web` | Web app with HTML |
| `robot` | Robot car with obstacle avoidance |
| `alarm` | Home security system |
| `smart-home` | Home automation |
| `garden` | Garden watering system |
| `assistant` | Voice assistant |
| `vision` | Computer vision |

---

## Examples

### Build a Robot Car

```python
from ludwig.iot import Robot, Sensor

robot = Robot.car(
    left={"forward": 17, "backward": 18},
    right={"forward": 22, "backward": 23},
)

robot.add_sensor("front", Sensor.ultrasonic(trigger=24, echo=25))

@robot.on_obstacle
def avoid():
    robot.stop()
    robot.backward(duration=0.5)
    robot.turn(90)
    robot.forward()

robot.forward()
robot.run()
```

### Build a Security Alarm

```python
from ludwig.iot import Alarm, Sensor

alarm = Alarm()
alarm.add(Sensor.motion(pin=4), zone="living_room")
alarm.add(Sensor.door(pin=5), zone="front_door")
alarm.siren(pin=17)

@alarm.on_triggered
def alert(zone, sensor):
    alarm.send_sms("+1234567890", f"Alert in {zone}!")

alarm.arm()
alarm.run()
```

### Build a Voice Assistant

```python
from ludwig.ai import Assistant

assistant = Assistant(name="Ludwig", model="gpt-4o")

@assistant.on_wake("Hey Ludwig")
def handle():
    command = assistant.listen()
    response = assistant.think(command)
    assistant.speak(response)

assistant.run()
```

### Build a Computer Vision System

```python
from ludwig.ai import Vision

vision = Vision(camera=0, model="yolo")

@vision.on_detect("person")
def person_alert(detection):
    print(f"Person detected at {detection.center}")

@vision.on_detect("cat")
def cat_spotted(detection):
    print("Cat spotted!")

vision.run(display=True)
```

### Build a Smart Garden

```python
from ludwig.iot import Garden

garden = Garden()
garden.add_plant("tomatoes", moisture_pin=0, pump_pin=17, threshold=30)
garden.add_plant("herbs", moisture_pin=1, pump_pin=18, threshold=40)

@garden.check_every(hours=1)
def water_check(plant):
    if plant.needs_water:
        plant.water(seconds=10)

garden.run()
```

### Build a REST API

```python
from ludwig import App, Database, Model
from dataclasses import dataclass

app = App()
db = Database("app.db")

@dataclass
class Item(Model):
    name: str
    price: float

@app.get("/items")
def list_items(req):
    return [item.to_dict() for item in Item.all()]

@app.post("/items")
def create_item(req):
    item = Item.create(**req.json)
    return item.to_dict()

app.run()
```

---

## IoT Hardware Support

Ludwig works on multiple platforms with automatic fallback to simulation:

| Platform | GPIO | I2C | SPI | PWM |
|----------|------|-----|-----|-----|
| Raspberry Pi | ✅ | ✅ | ✅ | ✅ |
| ESP32 | ✅ | ✅ | ✅ | ✅ |
| Arduino | ✅ | 🔜 | 🔜 | ✅ |
| Desktop (Simulation) | ✅ | ✅ | ✅ | ✅ |

---

## AI Features

- **Chat**: GPT-4o powered conversation
- **Voice**: Text-to-speech and speech recognition
- **Vision**: YOLO object detection
- **Automation**: Natural language rules ("every morning at 7am turn on lights")

---

## Project Structure

```
ludwig/
├── ludwig/
│   ├── __init__.py      # Main exports
│   ├── core.py          # App, Config
│   ├── web.py           # HTTP server
│   ├── db.py            # Database, Model
│   ├── cli.py           # CLI commands
│   ├── iot/             # IoT modules
│   │   ├── pin.py       # GPIO abstraction
│   │   ├── sensor.py    # Sensors
│   │   ├── actuators.py # Motors, lights, relays
│   │   ├── robot.py     # Robot cars, arms
│   │   ├── alarm.py     # Security systems
│   │   ├── camera.py    # Camera integration
│   │   ├── home.py      # Smart home
│   │   └── garden.py    # Garden automation
│   └── ai/              # AI modules
│       ├── assistant.py # Voice assistant
│       ├── vision.py    # Computer vision
│       └── automator.py # NL automation
└── examples/            # Example projects
```

---

## Documentation

- [Getting Started](docs/getting-started.md)
- [Web Development](docs/web.md)
- [IoT Guide](docs/iot.md)
- [AI Integration](docs/ai.md)
- [API Reference](docs/api.md)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](LICENSE)
