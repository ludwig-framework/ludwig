# AI Integration with Ludwig

Build voice assistants, computer vision systems, and intelligent automation with Ludwig's AI modules.

## Requirements

```bash
# Voice assistant
pip install ludwig[ai]

# Computer vision
pip install ludwig[vision]
```

## Voice Assistant

Build a voice-controlled assistant powered by GPT-4:

```python
from ludwig.ai import Assistant

assistant = Assistant(
    name="Ludwig",
    model="gpt-4o",
    voice="alloy",  # OpenAI voice: alloy, echo, fable, onyx, nova, shimmer
)

# Wake word activation
@assistant.on_wake("Hey Ludwig")
def handle():
    command = assistant.listen()      # Speech to text
    response = assistant.think(command)  # GPT-4 response
    assistant.speak(response)         # Text to speech

assistant.run()
```

### Chat Without Voice

```python
assistant = Assistant(model="gpt-4o")

response = assistant.chat("What's the weather like?")
print(response)

# With context
response = assistant.chat(
    "Summarize this document",
    context="Ludwig is a Python framework..."
)
```

### Custom Commands

```python
@assistant.on_command("turn on lights")
def lights_on():
    home.all_lights_on()
    assistant.speak("Lights are on")

@assistant.on_command("turn off lights")
def lights_off():
    home.all_lights_off()
    assistant.speak("Lights are off")

@assistant.on_command("what's the temperature")
def get_temp():
    temp = sensor.read()
    assistant.speak(f"It's {temp} degrees")
```

### Configuration

```python
assistant = Assistant(
    name="Jarvis",
    model="gpt-4o",           # OpenAI model
    voice="onyx",             # TTS voice
    system_prompt="You are a helpful home assistant",
    api_key="sk-...",         # Or set OPENAI_API_KEY env var
)
```

## Computer Vision

Object detection powered by YOLO:

```python
from ludwig.ai import Vision

vision = Vision(camera=0, model="yolo")  # or "yolov8n", "yolov8s", etc.

# Detect specific objects
@vision.on_detect("person")
def person_detected(detection):
    print(f"Person at {detection.center}")
    print(f"Confidence: {detection.confidence:.2f}")
    print(f"Bounding box: {detection.bbox}")

@vision.on_detect("car")
def car_detected(detection):
    print(f"Car detected!")

@vision.on_detect("cat")
def cat_spotted(detection):
    # Take action when cat detected
    pass

# Run with display window
vision.run(display=True)

# Or run headless
vision.run(display=False)
```

### Detection Object

```python
@vision.on_detect("person")
def handle(detection):
    detection.label       # "person"
    detection.confidence  # 0.95
    detection.bbox        # (x1, y1, x2, y2)
    detection.center      # (cx, cy)
    detection.width       # width in pixels
    detection.height      # height in pixels
```

### Multiple Objects

```python
@vision.on_detect(["person", "car", "dog"])
def detect_any(detection):
    print(f"Detected: {detection.label}")
```

### Single Frame Analysis

```python
vision = Vision(camera=0)

# Capture and analyze single frame
detections = vision.detect()
for d in detections:
    print(f"{d.label}: {d.confidence:.2f}")
```

### With IoT Integration

```python
from ludwig.ai import Vision
from ludwig.iot import Alarm, Camera

vision = Vision(camera=0)
alarm = Alarm()

@vision.on_detect("person")
def intruder_alert(detection):
    if alarm.is_armed:
        alarm.trigger()
        cam = Camera(0)
        cam.capture(f"intruder_{time.time()}.jpg")
```

## Natural Language Automation

Create automation rules using plain English:

```python
from ludwig.ai import Automator

auto = Automator()

# Time-based rules
auto.add_rule("every morning at 7am turn on the coffee maker")
auto.add_rule("every day at sunset turn on the porch lights")
auto.add_rule("every weekday at 8am remind me to check emails")

# Condition-based rules
auto.add_rule("when temperature is above 80 turn on the AC")
auto.add_rule("when motion is detected in backyard send me an alert")
auto.add_rule("when door opens after 10pm turn on security mode")

# Event-based rules
auto.add_rule("when I say goodnight turn off all lights")
auto.add_rule("when battery is low notify me")

# Run the automation engine
auto.run()
```

### With Context

```python
auto = Automator()

# Provide devices/sensors the automator can control
auto.set_context({
    "devices": {
        "coffee_maker": coffee_relay,
        "porch_lights": porch_light,
        "ac": ac_relay,
    },
    "sensors": {
        "temperature": temp_sensor,
        "motion_backyard": motion_sensor,
    }
})

auto.add_rule("when temperature exceeds 75 turn on ac")
auto.run()
```

### Custom Actions

```python
@auto.action("send_alert")
def send_alert(message):
    send_sms("+1234567890", message)

@auto.action("play_music")
def play_music(playlist):
    spotify.play(playlist)

auto.add_rule("when I get home play my welcome playlist")
```

## Combining AI + IoT

### Smart Security Camera

```python
from ludwig.ai import Vision, Assistant
from ludwig.iot import Camera, Alarm

vision = Vision(camera=0)
assistant = Assistant(model="gpt-4o")
alarm = Alarm()

@vision.on_detect("person")
def security_check(detection):
    if alarm.is_armed:
        # Ask AI to assess threat
        response = assistant.chat(
            "A person was detected at the front door. "
            "The time is 2am. Should I trigger the alarm?",
            context="Security mode is active. No family expected."
        )
        
        if "yes" in response.lower():
            alarm.trigger()
            alarm.send_sms("+1234567890", "Intruder detected!")
```

### Voice-Controlled Robot

```python
from ludwig.ai import Assistant
from ludwig.iot import Robot

assistant = Assistant(name="Robo")
robot = Robot.car(...)

@assistant.on_command("go forward")
def forward():
    robot.forward(duration=2)
    assistant.speak("Moving forward")

@assistant.on_command("turn around")
def turn():
    robot.turn(180)
    assistant.speak("Turning around")

@assistant.on_command("stop")
def stop():
    robot.stop()
    assistant.speak("Stopped")

assistant.run()
```

### AI Garden Monitor

```python
from ludwig.ai import Vision, Assistant
from ludwig.iot import Garden

vision = Vision(camera=0)
assistant = Assistant(model="gpt-4o")
garden = Garden()

@vision.on_detect("bird")
def bird_spotted(detection):
    assistant.speak("Bird detected in garden!")

@garden.check_every(hours=4)
def health_check(plant):
    # Capture image for AI analysis
    img = vision.capture()
    
    response = assistant.chat(
        f"Analyze this image of my {plant.name}. "
        "Does it look healthy? Any signs of disease or pests?",
        image=img
    )
    
    garden.log(f"{plant.name}: {response}")
```

## Environment Variables

Set these environment variables for API access:

```bash
# OpenAI API key (required for chat, TTS)
export OPENAI_API_KEY=sk-...

# Optional: specific models
export LUDWIG_CHAT_MODEL=gpt-4o
export LUDWIG_TTS_MODEL=tts-1
export LUDWIG_STT_MODEL=whisper-1
```

## Tips

### Performance

```python
# Use smaller YOLO model for speed
vision = Vision(camera=0, model="yolov8n")  # nano = fastest

# Or larger for accuracy
vision = Vision(camera=0, model="yolov8x")  # xlarge = most accurate
```

### Memory

```python
# Clear assistant conversation history
assistant.clear_history()
```

### Error Handling

```python
try:
    response = assistant.chat("Hello")
except Exception as e:
    print(f"AI error: {e}")
    response = "Sorry, I'm having trouble connecting."
```
