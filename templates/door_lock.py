"""
Ludwig Smart Door Lock Template
Secure door lock with PIN, RFID, and remote access.
"""
from ludwig import App, route
from ludwig.iot import Sensor, Relay

app = App()

# Hardware
keypad = Sensor("keypad", pins=[2, 3, 4, 5, 6, 7, 8, 9])
rfid = Sensor("rfid", pin=10)
lock = Relay(pin=11)
door_sensor = Sensor("magnetic", pin=12)

# Security config
PIN = "1234"
authorized_cards = ["A1B2C3D4", "E5F6G7H8"]
access_log = []

def log_access(method: str, success: bool, detail: str = ""):
    from datetime import datetime
    access_log.append({
        "time": datetime.now().isoformat(),
        "method": method,
        "success": success,
        "detail": detail
    })

@route("/")
def lock_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Lock</title>
        <style>
            body { font-family: system-ui; margin: 40px; background: #1a1a2e; color: white; }
            .container { max-width: 400px; margin: 0 auto; text-align: center; }
            h1 { margin-bottom: 32px; }
            .status { font-size: 24px; padding: 24px; border-radius: 12px; margin-bottom: 24px; }
            .locked { background: #e74c3c; }
            .unlocked { background: #2ecc71; }
            .keypad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }
            .key { padding: 20px; font-size: 24px; border: none; border-radius: 8px; background: #16213e; color: white; cursor: pointer; }
            .key:hover { background: #0f3460; }
            .display { background: #16213e; padding: 16px; border-radius: 8px; margin-bottom: 24px; font-size: 24px; letter-spacing: 8px; }
            button { padding: 16px 32px; font-size: 18px; border: none; border-radius: 8px; cursor: pointer; margin: 8px; }
            .unlock { background: #2ecc71; color: white; }
            .lock { background: #e74c3c; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Smart Lock</h1>
            <div class="status" id="status">Checking...</div>
            <div class="display" id="display">____</div>
            <div class="keypad">
                <button class="key" onclick="press('1')">1</button>
                <button class="key" onclick="press('2')">2</button>
                <button class="key" onclick="press('3')">3</button>
                <button class="key" onclick="press('4')">4</button>
                <button class="key" onclick="press('5')">5</button>
                <button class="key" onclick="press('6')">6</button>
                <button class="key" onclick="press('7')">7</button>
                <button class="key" onclick="press('8')">8</button>
                <button class="key" onclick="press('9')">9</button>
                <button class="key" onclick="clear()">C</button>
                <button class="key" onclick="press('0')">0</button>
                <button class="key" onclick="submit()">OK</button>
            </div>
            <button class="unlock" onclick="remoteUnlock()">Remote Unlock</button>
            <button class="lock" onclick="remoteLock()">Lock</button>
        </div>
        <script>
            let pin = '';
            
            function press(n) {
                if (pin.length < 4) {
                    pin += n;
                    document.getElementById('display').textContent = '*'.repeat(pin.length) + '_'.repeat(4-pin.length);
                }
            }
            
            function clear() {
                pin = '';
                document.getElementById('display').textContent = '____';
            }
            
            async function submit() {
                const res = await fetch('/unlock/pin', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({pin: pin})
                });
                const data = await res.json();
                alert(data.message);
                clear();
                updateStatus();
            }
            
            async function remoteUnlock() {
                await fetch('/unlock/remote', {method: 'POST'});
                updateStatus();
            }
            
            async function remoteLock() {
                await fetch('/lock', {method: 'POST'});
                updateStatus();
            }
            
            async function updateStatus() {
                const res = await fetch('/status');
                const data = await res.json();
                const el = document.getElementById('status');
                el.textContent = data.locked ? 'LOCKED' : 'UNLOCKED';
                el.className = 'status ' + (data.locked ? 'locked' : 'unlocked');
            }
            
            updateStatus();
            setInterval(updateStatus, 2000);
        </script>
    </body>
    </html>
    """

@route("/status")
def get_status():
    return {
        "locked": not lock.is_on(),
        "door_closed": door_sensor.read() == 1
    }

@route("/unlock/pin", methods=["POST"])
def unlock_pin(pin: str):
    if pin == PIN:
        lock.on()
        log_access("pin", True)
        return {"success": True, "message": "Unlocked"}
    else:
        log_access("pin", False, f"Invalid PIN attempt")
        return {"success": False, "message": "Invalid PIN"}

@route("/unlock/remote", methods=["POST"])
def unlock_remote():
    lock.on()
    log_access("remote", True)
    return {"success": True}

@route("/lock", methods=["POST"])
def lock_door():
    lock.off()
    return {"success": True}

@route("/log")
def get_log():
    return {"log": access_log[-50:]}

if __name__ == "__main__":
    app.run(port=8000)
