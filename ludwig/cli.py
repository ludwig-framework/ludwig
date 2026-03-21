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
                                   "smart-home", "garden", "assistant", "vision",
                                   "dashboard", "chatbot", "weather-station", 
                                   "door-lock", "led"],
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
        "dashboard": TEMPLATE_DASHBOARD,
        "chatbot": TEMPLATE_CHATBOT,
        "weather-station": TEMPLATE_WEATHER_STATION,
        "door-lock": TEMPLATE_DOOR_LOCK,
        "led": TEMPLATE_LED,
    }
    
    code = templates.get(template, TEMPLATE_BASIC)
    
    # Write main file
    with open(os.path.join(name, "app.py"), "w") as f:
        f.write(code)
    
    # Write requirements.txt
    with open(os.path.join(name, "requirements.txt"), "w") as f:
        f.write("ludwig\n")
        
        # Add template-specific requirements
        if template in ("assistant", "vision", "chatbot"):
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

TEMPLATE_DASHBOARD = '''"""
Ludwig Dashboard
"""

from ludwig import App

app = App()

@app.route("/")
def dashboard(req):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body { font-family: system-ui; margin: 40px; background: #f5f5f5; }
            .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
            .card { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stat { font-size: 32px; font-weight: bold; color: #333; }
            .label { color: #666; margin-top: 8px; }
        </style>
    </head>
    <body>
        <h1>Dashboard</h1>
        <div class="grid">
            <div class="card"><div class="stat">1,234</div><div class="label">Users</div></div>
            <div class="card"><div class="stat">567</div><div class="label">Orders</div></div>
            <div class="card"><div class="stat">$45,678</div><div class="label">Revenue</div></div>
            <div class="card"><div class="stat">+12.5%</div><div class="label">Growth</div></div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(port=8000)
'''

TEMPLATE_CHATBOT = '''"""
Ludwig Chatbot
"""

from ludwig import App
from ludwig.ai import Assistant

app = App()
assistant = Assistant(name="Bot", model="gpt-4o-mini")

@app.route("/")
def chat_ui(req):
    return """
    <!DOCTYPE html>
    <html><head><title>Chatbot</title>
    <style>
        body { font-family: system-ui; margin: 0; height: 100vh; display: flex; flex-direction: column; }
        #messages { flex: 1; padding: 20px; overflow-y: auto; background: #f5f5f5; }
        .message { padding: 12px 16px; border-radius: 8px; margin: 8px 0; max-width: 70%; }
        .user { background: #007bff; color: white; margin-left: auto; }
        .bot { background: white; }
        #input-area { display: flex; padding: 16px; background: white; }
        input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }
        button { margin-left: 8px; padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 8px; }
    </style></head>
    <body>
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="msg" placeholder="Type..." onkeypress="if(event.key==='Enter')send()">
            <button onclick="send()">Send</button>
        </div>
        <script>
            async function send() {
                const input = document.getElementById('msg');
                const msg = input.value.trim(); if (!msg) return;
                addMsg(msg, 'user'); input.value = '';
                const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:msg})});
                const data = await res.json();
                addMsg(data.reply, 'bot');
            }
            function addMsg(text, type) {
                const div = document.createElement('div');
                div.className = 'message ' + type;
                div.textContent = text;
                document.getElementById('messages').appendChild(div);
            }
        </script>
    </body></html>
    """

@app.route("/chat", methods=["POST"])
def chat(req):
    return {"reply": assistant.ask(req.json.get("message", ""))}

if __name__ == "__main__":
    app.run(port=8000)
'''

TEMPLATE_WEATHER_STATION = '''"""
Ludwig Weather Station
"""

from ludwig import App
from ludwig.iot import Sensor

app = App()

temperature = Sensor("dht22", pin=4)
humidity = Sensor("dht22", pin=4, reading="humidity")

@app.route("/")
def dashboard(req):
    return """
    <!DOCTYPE html>
    <html><head><title>Weather Station</title>
    <style>
        body { font-family: system-ui; margin: 40px; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 600px; margin: 0 auto; }
        .card { background: white; padding: 24px; border-radius: 12px; text-align: center; }
        .value { font-size: 48px; font-weight: bold; }
        .label { color: #666; margin-top: 8px; }
        h1 { color: white; text-align: center; }
    </style></head>
    <body>
        <h1>Weather Station</h1>
        <div class="grid">
            <div class="card"><div class="value" id="temp">--</div><div class="label">Temperature (C)</div></div>
            <div class="card"><div class="value" id="hum">--</div><div class="label">Humidity (%)</div></div>
        </div>
        <script>
            async function update() {
                const res = await fetch('/readings');
                const data = await res.json();
                document.getElementById('temp').textContent = data.temperature.toFixed(1);
                document.getElementById('hum').textContent = data.humidity.toFixed(0);
            }
            update(); setInterval(update, 5000);
        </script>
    </body></html>
    """

@app.route("/readings")
def readings(req):
    return {"temperature": temperature.read(), "humidity": humidity.read()}

if __name__ == "__main__":
    app.run(port=8000)
'''

TEMPLATE_DOOR_LOCK = '''"""
Ludwig Smart Door Lock
"""

from ludwig import App
from ludwig.iot import Relay

app = App()
lock = Relay(pin=11)
PIN = "1234"

@app.route("/")
def ui(req):
    return """
    <!DOCTYPE html>
    <html><head><title>Smart Lock</title>
    <style>
        body { font-family: system-ui; margin: 40px; background: #1a1a2e; color: white; }
        .container { max-width: 300px; margin: 0 auto; text-align: center; }
        .status { font-size: 24px; padding: 24px; border-radius: 12px; margin-bottom: 24px; }
        .locked { background: #e74c3c; }
        .unlocked { background: #2ecc71; }
        input { padding: 16px; font-size: 20px; width: 100%; margin-bottom: 16px; border-radius: 8px; border: none; }
        button { padding: 16px 32px; font-size: 18px; border: none; border-radius: 8px; cursor: pointer; margin: 8px; }
        .unlock { background: #2ecc71; color: white; }
        .lock { background: #e74c3c; color: white; }
    </style></head>
    <body>
        <div class="container">
            <h1>Smart Lock</h1>
            <div class="status" id="status">Checking...</div>
            <input type="password" id="pin" placeholder="Enter PIN" maxlength="4">
            <button class="unlock" onclick="unlock()">Unlock</button>
            <button class="lock" onclick="doLock()">Lock</button>
        </div>
        <script>
            async function unlock() {
                const pin = document.getElementById('pin').value;
                const res = await fetch('/unlock', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({pin})});
                const data = await res.json();
                alert(data.message);
                updateStatus();
            }
            async function doLock() { await fetch('/lock', {method:'POST'}); updateStatus(); }
            async function updateStatus() {
                const res = await fetch('/status');
                const data = await res.json();
                const el = document.getElementById('status');
                el.textContent = data.locked ? 'LOCKED' : 'UNLOCKED';
                el.className = 'status ' + (data.locked ? 'locked' : 'unlocked');
            }
            updateStatus();
        </script>
    </body></html>
    """

@app.route("/status")
def status(req):
    return {"locked": not lock.is_on()}

@app.route("/unlock", methods=["POST"])
def unlock(req):
    pin = req.json.get("pin", "")
    if pin == PIN:
        lock.on()
        return {"success": True, "message": "Unlocked"}
    return {"success": False, "message": "Invalid PIN"}

@app.route("/lock", methods=["POST"])
def do_lock(req):
    lock.off()
    return {"success": True}

if __name__ == "__main__":
    app.run(port=8000)
'''

TEMPLATE_LED = '''"""
Ludwig LED Controller
"""

from ludwig import App
from ludwig.iot import Light

app = App()
led = Light(pin=18, type="ws2812b", count=60)
state = {"r": 0, "g": 0, "b": 0, "brightness": 100}

@app.route("/")
def ui(req):
    return """
    <!DOCTYPE html>
    <html><head><title>LED Controller</title>
    <style>
        body { font-family: system-ui; margin: 40px; background: #111; color: white; }
        .container { max-width: 400px; margin: 0 auto; }
        .preview { height: 60px; border-radius: 8px; margin-bottom: 24px; }
        input[type="range"] { width: 100%; margin: 8px 0; }
        .scenes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .scene { padding: 12px; border: none; border-radius: 8px; cursor: pointer; }
    </style></head>
    <body>
        <div class="container">
            <h1>LED Controller</h1>
            <div class="preview" id="preview"></div>
            <label>R: <input type="range" id="r" max="255" value="0" oninput="update()"></label>
            <label>G: <input type="range" id="g" max="255" value="0" oninput="update()"></label>
            <label>B: <input type="range" id="b" max="255" value="0" oninput="update()"></label>
            <h3>Scenes</h3>
            <div class="scenes">
                <button class="scene" style="background:#333" onclick="set(0,0,0)">Off</button>
                <button class="scene" style="background:#ffb464" onclick="set(255,180,100)">Warm</button>
                <button class="scene" style="background:#f00" onclick="set(255,0,0)">Red</button>
                <button class="scene" style="background:#0f0" onclick="set(0,255,0)">Green</button>
                <button class="scene" style="background:#00f" onclick="set(0,0,255)">Blue</button>
                <button class="scene" style="background:#9600ff" onclick="set(150,0,255)">Purple</button>
            </div>
        </div>
        <script>
            function update() {
                const r=document.getElementById('r').value, g=document.getElementById('g').value, b=document.getElementById('b').value;
                document.getElementById('preview').style.background = `rgb(${r},${g},${b})`;
                fetch('/set', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({r:+r,g:+g,b:+b})});
            }
            function set(r,g,b) {
                document.getElementById('r').value=r; document.getElementById('g').value=g; document.getElementById('b').value=b;
                update();
            }
        </script>
    </body></html>
    """

@app.route("/set", methods=["POST"])
def set_color(req):
    global state
    data = req.json
    r, g, b = data.get("r", 0), data.get("g", 0), data.get("b", 0)
    state = {"r": r, "g": g, "b": b, "brightness": 100}
    led.set_color(r, g, b)
    return {"success": True}

if __name__ == "__main__":
    app.run(port=8000)
'''


if __name__ == "__main__":
    main()
