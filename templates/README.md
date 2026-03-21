# Ludwig Templates

Project templates demonstrating Ludwig's capabilities.

## Web Templates

### Simple API
```bash
python api_example.py
# Visit http://localhost:8000
```

### REST API with Database
```bash
python todo_api.py
```

### Dashboard
```bash
python dashboard_example.py
# Web dashboard with stats cards
```

## IoT Templates

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

### Weather Station
```bash
python weather_station.py
# Temperature, humidity, pressure, light monitoring
```

### Smart Door Lock
```bash
python door_lock.py
# PIN, RFID, and remote access control
```

### LED Controller
```bash
python led_controller.py
# RGB LED strip with scenes and effects
```

## AI Templates

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
