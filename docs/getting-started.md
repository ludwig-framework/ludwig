# Getting Started with Ludwig

Ludwig is a Python framework for building Web APIs, IoT systems, and AI applications with simple, readable code.

## Installation

### From PyPI (Recommended)

```bash
pip install ludwig
```

### From GitHub (Development)

```bash
git clone https://github.com/ludwig-framework/ludwig.git
cd ludwig
pip install -e .
```

### Optional Dependencies

```bash
# For AI features (voice assistant, chat)
pip install ludwig[ai]

# For computer vision
pip install ludwig[vision]

# For Raspberry Pi
pip install ludwig[pi]

# Everything
pip install ludwig[all]
```

## Your First Project

### Using Templates

The fastest way to start:

```bash
# Create a REST API
ludwig new my-api --template api

# Create a robot car
ludwig new my-robot --template robot

# Create a smart home
ludwig new my-home --template smart-home
```

### Manual Setup

Create `app.py`:

```python
from ludwig import App

app = App()

@app.get("/")
def home(req):
    return "Hello, Ludwig!"

@app.get("/api/hello/:name")
def hello(req):
    return {"message": f"Hello, {req.params['name']}!"}

app.run()
```

Run it:

```bash
python app.py
```

Visit `http://localhost:8000` in your browser.

## Project Templates

| Template | Use Case |
|----------|----------|
| `basic` | Simple web app |
| `api` | REST API with database |
| `web` | HTML web app |
| `robot` | Robot car with obstacle avoidance |
| `alarm` | Home security system |
| `smart-home` | Home automation |
| `garden` | Garden watering automation |
| `assistant` | Voice assistant with GPT-4 |
| `vision` | Object detection with YOLO |

## Next Steps

- [Web Development](web.md) - Build APIs and web apps
- [IoT Guide](iot.md) - Robots, alarms, smart homes
- [AI Integration](ai.md) - Voice assistants and vision
- [API Reference](api.md) - Full API documentation

## Requirements

- Python 3.10+
- No external dependencies for core features
- Platform-specific libraries for hardware (auto-detected)
