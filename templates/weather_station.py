"""
Ludwig Weather Station Template
IoT weather monitoring with sensors.
"""
from ludwig import App, route
from ludwig.iot import Sensor

app = App()

# Initialize sensors
temperature = Sensor("dht22", pin=4)
humidity = Sensor("dht22", pin=4, reading="humidity")
pressure = Sensor("bmp280", pin=5)
light = Sensor("ldr", pin=6)

# Store readings history
readings = []

@route("/")
def weather_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Station</title>
        <style>
            body { font-family: system-ui; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: white; margin-bottom: 24px; }
            .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
            .card { background: white; padding: 24px; border-radius: 12px; text-align: center; }
            .value { font-size: 48px; font-weight: bold; color: #333; }
            .unit { font-size: 20px; color: #666; }
            .label { color: #999; margin-top: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Weather Station</h1>
            <div class="grid">
                <div class="card">
                    <div class="value" id="temp">--</div>
                    <div class="unit">C</div>
                    <div class="label">Temperature</div>
                </div>
                <div class="card">
                    <div class="value" id="humidity">--</div>
                    <div class="unit">%</div>
                    <div class="label">Humidity</div>
                </div>
                <div class="card">
                    <div class="value" id="pressure">--</div>
                    <div class="unit">hPa</div>
                    <div class="label">Pressure</div>
                </div>
                <div class="card">
                    <div class="value" id="light">--</div>
                    <div class="unit">lux</div>
                    <div class="label">Light</div>
                </div>
            </div>
        </div>
        <script>
            async function update() {
                const res = await fetch('/readings');
                const data = await res.json();
                document.getElementById('temp').textContent = data.temperature.toFixed(1);
                document.getElementById('humidity').textContent = data.humidity.toFixed(0);
                document.getElementById('pressure').textContent = data.pressure.toFixed(0);
                document.getElementById('light').textContent = data.light.toFixed(0);
            }
            update();
            setInterval(update, 5000);
        </script>
    </body>
    </html>
    """

@route("/readings")
def get_readings():
    data = {
        "temperature": temperature.read(),
        "humidity": humidity.read(),
        "pressure": pressure.read(),
        "light": light.read()
    }
    readings.append(data)
    return data

@route("/history")
def get_history():
    return {"readings": readings[-100:]}

if __name__ == "__main__":
    app.run(port=8000)
