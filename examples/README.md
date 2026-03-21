# Ludwig Examples

Example projects demonstrating Ludwig's capabilities.

## Web Examples

### Simple API
```bash
python api_example.py
# Visit http://localhost:8000
```

### REST API with Database
```bash
python todo_api.py
```

## IoT Examples

### Robot Car
```bash
python robot_car.py
# Runs in simulation mode on desktop
```

### Security Alarm
```bash
python alarm_example.py
```

### Smart Home
```bash
python smart_home.py
```

### Garden Automation
```bash
python garden_example.py
```

## AI Examples

### Voice Assistant
```bash
export OPENAI_API_KEY=sk-...
python assistant_example.py
```

### Computer Vision
```bash
pip install ludwig[vision]
python vision_example.py
```

## Running on Hardware

These examples run in simulation mode on desktop. On Raspberry Pi or ESP32, they control real hardware automatically.

```bash
# On Raspberry Pi
pip install ludwig[pi]
python robot_car.py  # Now controls real motors!
```
