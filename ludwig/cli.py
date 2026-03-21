"""
Ludwig CLI - Command line interface with project templates
"""

import argparse
import os
import sys


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="ludwig",
        description="Ludwig - Simple Python for Web, IoT, and AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ludwig new my-api --template api
  ludwig new my-robot --template robot
  ludwig new my-home --template smart-home
  ludwig dev
  ludwig run app.py
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # new command
    new_parser = subparsers.add_parser("new", help="Create a new project")
    new_parser.add_argument("name", help="Project name")
    new_parser.add_argument("--template", "-t", default="basic",
                           choices=["basic", "api", "web", "robot", "alarm", 
                                   "smart-home", "garden", "assistant", "vision"],
                           help="Project template")
    
    # dev command
    dev_parser = subparsers.add_parser("dev", help="Start development server")
    dev_parser.add_argument("--port", "-p", type=int, default=8000, help="Port")
    dev_parser.add_argument("--host", default="0.0.0.0", help="Host")
    
    # run command
    run_parser = subparsers.add_parser("run", help="Run a Ludwig file")
    run_parser.add_argument("file", help="File to run")
    
    # version command
    subparsers.add_parser("version", help="Show version")
    
    args = parser.parse_args()
    
    if args.command == "new":
        create_project(args.name, args.template)
    elif args.command == "dev":
        run_dev_server(args.host, args.port)
    elif args.command == "run":
        run_file(args.file)
    elif args.command == "version":
        from ludwig import __version__
        print(f"Ludwig v{__version__}")
    else:
        parser.print_help()


def create_project(name: str, template: str):
    """Create a new Ludwig project."""
    os.makedirs(name, exist_ok=True)
    
    templates = {
        "basic": TEMPLATE_BASIC,
        "api": TEMPLATE_API,
        "web": TEMPLATE_WEB,
        "robot": TEMPLATE_ROBOT,
        "alarm": TEMPLATE_ALARM,
        "smart-home": TEMPLATE_SMART_HOME,
        "garden": TEMPLATE_GARDEN,
        "assistant": TEMPLATE_ASSISTANT,
        "vision": TEMPLATE_VISION,
    }
    
    code = templates.get(template, TEMPLATE_BASIC)
    
    # Write main file
    with open(os.path.join(name, "app.py"), "w") as f:
        f.write(code)
    
    # Write requirements.txt
    with open(os.path.join(name, "requirements.txt"), "w") as f:
        f.write("ludwig\n")
        
        # Add template-specific requirements
        if template in ("assistant", "vision"):
            f.write("openai\n")
        if template == "vision":
            f.write("opencv-python\n")
            f.write("ultralytics\n")
        if template == "assistant":
            f.write("SpeechRecognition\n")
    
    # Write README
    with open(os.path.join(name, "README.md"), "w") as f:
        f.write(f"# {name}\n\n")
        f.write(f"A Ludwig `{template}` project.\n\n")
        f.write("## Getting Started\n\n")
        f.write("```bash\n")
        f.write("pip install -r requirements.txt\n")
        f.write("python app.py\n")
        f.write("```\n")
    
    print(f"✓ Created project: {name}")
    print(f"  Template: {template}")
    print()
    print("Next steps:")
    print(f"  cd {name}")
    print("  pip install -r requirements.txt")
    print("  python app.py")


def run_dev_server(host: str, port: int):
    """Start development server."""
    if os.path.exists("app.py"):
        print(f"Starting dev server at http://{host}:{port}")
        os.system(f"{sys.executable} app.py")
    else:
        print("No app.py found. Create one or use 'ludwig new <name>'")


def run_file(file: str):
    """Run a Ludwig file."""
    os.system(f"{sys.executable} {file}")


# === Templates ===

TEMPLATE_BASIC = '''"""
Ludwig Basic Project
"""

from ludwig import App

app = App(name="My App")

@app.get("/")
def home(req):
    return "Hello from Ludwig!"

@app.get("/api/status")
def status(req):
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
'''

TEMPLATE_API = '''"""
Ludwig REST API
"""

from ludwig import App, Database, Model
from dataclasses import dataclass

app = App(name="API")
db = Database("app.db")

@dataclass
class Item(Model):
    name: str
    price: float
    
@app.get("/api/items")
def list_items(req):
    return [item.to_dict() for item in Item.all()]

@app.post("/api/items")
def create_item(req):
    item = Item.create(**req.json)
    return item.to_dict()

@app.get("/api/items/:id")
def get_item(req):
    item = Item.find(int(req.params["id"]))
    if not item:
        return {"error": "Not found"}, 404
    return item.to_dict()

if __name__ == "__main__":
    app.run(debug=True)
'''

TEMPLATE_WEB = '''"""
Ludwig Web App
"""

from ludwig import App

app = App(name="Web App")

@app.get("/")
def home(req):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ludwig Web App</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 min-h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-lg">
            <h1 class="text-3xl font-bold text-gray-800">Hello Ludwig!</h1>
            <p class="text-gray-600 mt-2">Your web app is running.</p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
'''

TEMPLATE_ROBOT = '''"""
Ludwig Robot Car
"""

from ludwig.iot import Robot, Sensor

# Create robot with 2 motors
robot = Robot.car(
    left={"forward": 17, "backward": 18, "enable": 12},
    right={"forward": 22, "backward": 23, "enable": 13},
)

# Add distance sensor
robot.add_sensor("front", Sensor.ultrasonic(trigger=24, echo=25))

# Avoid obstacles
@robot.on_obstacle
def avoid():
    print("Obstacle detected!")
    robot.stop()
    robot.backward(duration=0.5)
    robot.turn(90)
    robot.forward()

if __name__ == "__main__":
    print("Robot starting...")
    robot.forward(speed=50)
    robot.run(obstacle_distance=20)
'''

TEMPLATE_ALARM = '''"""
Ludwig Security Alarm
"""

from ludwig.iot import Alarm, Sensor

alarm = Alarm()

# Add sensors
alarm.add(Sensor.motion(pin=4), zone="living_room")
alarm.add(Sensor.door(pin=5), zone="front_door")
alarm.add(Sensor.window(pin=6), zone="bedroom")

# Add siren
alarm.siren(pin=17)

# Alert handler
@alarm.on_triggered
def alert(zone, sensor):
    print(f"🚨 ALERT: {zone}")
    alarm.send_sms("+1234567890", f"Alarm triggered in {zone}")

if __name__ == "__main__":
    alarm.arm()
    alarm.run()
'''

TEMPLATE_SMART_HOME = '''"""
Ludwig Smart Home
"""

from ludwig.iot import Home, Light, Sensor

home = Home()

# Living room
living = home.room("living_room")
living.add(Light(pin=17, name="ceiling", dimmable=True))
living.add(Sensor.motion(pin=4))
living.add(Sensor.temperature(pin=7))

# Bedroom
bedroom = home.room("bedroom")
bedroom.add(Light(pin=18, name="main"))

# Automations
@home.at("sunset")
def evening_mode():
    living.light("ceiling").on()
    living.light("ceiling").brightness(70)

@home.at("23:00")
def bedtime():
    home.all_lights_off()

@home.when(lambda: living.motion.read())
def motion_light():
    if not living.light("ceiling").is_on:
        living.light("ceiling").on()

if __name__ == "__main__":
    home.run()
'''

TEMPLATE_GARDEN = '''"""
Ludwig Garden Automation
"""

from ludwig.iot import Garden

garden = Garden()

# Add plants
garden.add_plant("tomatoes", moisture_pin=0, pump_pin=17, threshold=30)
garden.add_plant("herbs", moisture_pin=1, pump_pin=18, threshold=40)
garden.add_plant("flowers", moisture_pin=2, pump_pin=19, threshold=35)

# Check every hour
@garden.check_every(hours=1)
def water_if_needed(plant):
    if plant.needs_water:
        plant.water(seconds=10)
        garden.log(f"Watered {plant.name} (moisture was {plant.moisture}%)")

# Morning routine
@garden.at("06:00")
def morning_check():
    print("Morning status:")
    for plant in garden.plants:
        print(f"  {plant.name}: {plant.moisture}%")

if __name__ == "__main__":
    garden.run()
'''

TEMPLATE_ASSISTANT = '''"""
Ludwig Voice Assistant
"""

from ludwig.ai import Assistant

assistant = Assistant(
    name="Ludwig",
    model="gpt-4o",
    voice="alloy",
)

@assistant.on_wake("Hey Ludwig")
def handle():
    command = assistant.listen()
    response = assistant.think(command)
    assistant.speak(response)

@assistant.on_command("turn on lights")
def lights_on():
    print("Turning on lights...")
    # home.all_lights_on()

@assistant.on_command("turn off lights")
def lights_off():
    print("Turning off lights...")
    # home.all_lights_off()

if __name__ == "__main__":
    print("Say 'Hey Ludwig' to wake me up...")
    assistant.run()
'''

TEMPLATE_VISION = '''"""
Ludwig Computer Vision
"""

from ludwig.ai import Vision

vision = Vision(camera=0, model="yolo")

@vision.on_detect("person")
def person_detected(detection):
    print(f"Person at {detection.center} (confidence: {detection.confidence:.2f})")

@vision.on_detect("cat")
def cat_detected(detection):
    print(f"Cat spotted!")

@vision.on_detect("dog")
def dog_detected(detection):
    print(f"Dog spotted!")

if __name__ == "__main__":
    vision.run(display=True)
'''


if __name__ == "__main__":
    main()
