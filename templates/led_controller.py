"""
Ludwig LED Controller Template
RGB LED strip controller with effects and scenes.
"""
from ludwig import App, route
from ludwig.iot import Light

app = App()

# LED strip configuration
led_strip = Light(pin=18, type="ws2812b", count=60)

# Predefined scenes
scenes = {
    "off": {"r": 0, "g": 0, "b": 0},
    "warm": {"r": 255, "g": 180, "b": 100},
    "cool": {"r": 200, "g": 220, "b": 255},
    "red": {"r": 255, "g": 0, "b": 0},
    "green": {"r": 0, "g": 255, "b": 0},
    "blue": {"r": 0, "g": 0, "b": 255},
    "purple": {"r": 150, "g": 0, "b": 255},
    "party": {"effect": "rainbow"},
    "relax": {"r": 255, "g": 100, "b": 50, "brightness": 30}
}

current_state = {"r": 0, "g": 0, "b": 0, "brightness": 100}

@route("/")
def led_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LED Controller</title>
        <style>
            body { font-family: system-ui; margin: 0; background: #111; min-height: 100vh; color: white; }
            .container { max-width: 500px; margin: 0 auto; padding: 40px 20px; }
            h1 { text-align: center; margin-bottom: 32px; }
            .preview { height: 80px; border-radius: 12px; margin-bottom: 24px; transition: background 0.3s; }
            .slider-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; }
            input[type="range"] { width: 100%; }
            .scenes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }
            .scene { padding: 16px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; }
            .effects { display: flex; gap: 12px; }
            .effect { flex: 1; padding: 16px; border: 2px solid #333; border-radius: 8px; background: transparent; color: white; cursor: pointer; }
            .effect:hover { border-color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>LED Controller</h1>
            <div class="preview" id="preview"></div>
            
            <div class="slider-group">
                <label>Red: <span id="rVal">0</span></label>
                <input type="range" id="r" min="0" max="255" value="0" oninput="update()">
            </div>
            <div class="slider-group">
                <label>Green: <span id="gVal">0</span></label>
                <input type="range" id="g" min="0" max="255" value="0" oninput="update()">
            </div>
            <div class="slider-group">
                <label>Blue: <span id="bVal">0</span></label>
                <input type="range" id="b" min="0" max="255" value="0" oninput="update()">
            </div>
            <div class="slider-group">
                <label>Brightness: <span id="brVal">100</span>%</label>
                <input type="range" id="brightness" min="0" max="100" value="100" oninput="update()">
            </div>
            
            <h3>Scenes</h3>
            <div class="scenes">
                <button class="scene" style="background:#333" onclick="setScene('off')">Off</button>
                <button class="scene" style="background:#ffb464" onclick="setScene('warm')">Warm</button>
                <button class="scene" style="background:#c8dcff" onclick="setScene('cool')">Cool</button>
                <button class="scene" style="background:#f00" onclick="setScene('red')">Red</button>
                <button class="scene" style="background:#0f0" onclick="setScene('green')">Green</button>
                <button class="scene" style="background:#00f" onclick="setScene('blue')">Blue</button>
                <button class="scene" style="background:#9600ff" onclick="setScene('purple')">Purple</button>
                <button class="scene" style="background:linear-gradient(90deg,red,orange,yellow,green,blue,purple)" onclick="setScene('party')">Party</button>
                <button class="scene" style="background:#ff6432" onclick="setScene('relax')">Relax</button>
            </div>
            
            <h3>Effects</h3>
            <div class="effects">
                <button class="effect" onclick="setEffect('rainbow')">Rainbow</button>
                <button class="effect" onclick="setEffect('breathe')">Breathe</button>
                <button class="effect" onclick="setEffect('chase')">Chase</button>
            </div>
        </div>
        <script>
            function update() {
                const r = document.getElementById('r').value;
                const g = document.getElementById('g').value;
                const b = document.getElementById('b').value;
                const br = document.getElementById('brightness').value;
                
                document.getElementById('rVal').textContent = r;
                document.getElementById('gVal').textContent = g;
                document.getElementById('bVal').textContent = b;
                document.getElementById('brVal').textContent = br;
                
                document.getElementById('preview').style.background = `rgba(${r},${g},${b},${br/100})`;
                
                fetch('/set', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({r: +r, g: +g, b: +b, brightness: +br})
                });
            }
            
            async function setScene(name) {
                await fetch('/scene/' + name, {method: 'POST'});
                const res = await fetch('/state');
                const state = await res.json();
                document.getElementById('r').value = state.r;
                document.getElementById('g').value = state.g;
                document.getElementById('b').value = state.b;
                document.getElementById('brightness').value = state.brightness;
                update();
            }
            
            function setEffect(name) {
                fetch('/effect/' + name, {method: 'POST'});
            }
            
            update();
        </script>
    </body>
    </html>
    """

@route("/state")
def get_state():
    return current_state

@route("/set", methods=["POST"])
def set_color(r: int, g: int, b: int, brightness: int = 100):
    global current_state
    current_state = {"r": r, "g": g, "b": b, "brightness": brightness}
    led_strip.set_color(r, g, b)
    led_strip.set_brightness(brightness)
    return {"success": True}

@route("/scene/<name>", methods=["POST"])
def set_scene(name: str):
    global current_state
    if name in scenes:
        scene = scenes[name]
        if "effect" not in scene:
            current_state = {
                "r": scene.get("r", 0),
                "g": scene.get("g", 0),
                "b": scene.get("b", 0),
                "brightness": scene.get("brightness", 100)
            }
            led_strip.set_color(current_state["r"], current_state["g"], current_state["b"])
            led_strip.set_brightness(current_state["brightness"])
        else:
            led_strip.effect(scene["effect"])
        return {"success": True, "scene": name}
    return {"success": False, "error": "Unknown scene"}

@route("/effect/<name>", methods=["POST"])
def set_effect(name: str):
    led_strip.effect(name)
    return {"success": True, "effect": name}

if __name__ == "__main__":
    app.run(port=8000)
