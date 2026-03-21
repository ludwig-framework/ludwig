# Embedded Systems Guide

Ludwig provides templates and abstractions for IoT and embedded development.

## Creating an Embedded Project

```bash
# Basic IoT device
python artisan.py make:embedded TempMonitor

# Point of Sale system
python artisan.py make:pos RetailSystem

# QR Kiosk
python artisan.py make:kiosk InfoStation

# Smart home
python artisan.py make:smarthome MyHome

# Robotics
python artisan.py make:robotics RobotController
```

## Supported Platforms

- Arduino
- Raspberry Pi
- ESP32
- ESP8266

## Basic Device

```python
class TempMonitor(EmbeddedDevice):
    def __init__(self):
        self.sensor = TemperatureSensor(pin=4)
        self.display = LCD(pins=[2, 3, 4, 5])
    
    def setup(self):
        self.sensor.initialize()
        self.display.initialize()
    
    def loop(self):
        temp = self.sensor.read()
        self.display.print(f"Temp: {temp}C")
        self.sleep(1000)
```

## Sensors

Available sensor abstractions:

```python
# Temperature
sensor = TemperatureSensor(pin=4, model="DS18B20")
temp = sensor.read()  # Returns celsius

# Motion
sensor = MotionSensor(pin=7)
if sensor.detected():
    trigger_alert()

# Light
sensor = LightSensor(pin=A0)
lux = sensor.read()

# Ultrasonic distance
sensor = UltrasonicSensor(trigger=9, echo=10)
distance = sensor.read()  # Returns cm

# Barcode/QR
scanner = BarcodeScanner(port="/dev/ttyUSB0")
code = scanner.scan()
```

## Actuators

```python
# LED
led = LED(pin=13)
led.on()
led.off()
led.blink(interval=500)

# Servo
servo = Servo(pin=9)
servo.move(90)  # Move to 90 degrees

# Motor
motor = Motor(pin_a=5, pin_b=6)
motor.forward(speed=255)
motor.stop()

# Relay
relay = Relay(pin=8)
relay.on()
```

## Connectivity

```python
# WiFi
from ludwig.connectivity import WiFi

wifi = WiFi()
wifi.connect("SSID", "password")

# HTTP requests
response = wifi.get("https://api.example.com/data")
wifi.post("https://api.example.com/sensor", {"temp": 22.5})

# MQTT
from ludwig.connectivity import MQTT

mqtt = MQTT(broker="mqtt.example.com")
mqtt.subscribe("home/sensors/#", callback=handle_message)
mqtt.publish("home/sensors/temp", "22.5")
```

## POS System

```python
class RetailPOS(POSSystem):
    def __init__(self):
        self.scanner = BarcodeScanner()
        self.display = LCD()
        self.printer = ReceiptPrinter()
    
    def scan_item(self):
        barcode = self.scanner.scan()
        item = self.lookup_product(barcode)
        self.cart.add(item)
        self.display.show(f"{item.name}: ${item.price}")
    
    def checkout(self):
        total = self.cart.total()
        self.printer.print_receipt(self.cart)
        self.cart.clear()
```

## Smart Home

```python
class SmartHome(SmartHomeSystem):
    def __init__(self):
        self.lights = [Light(pin=i) for i in [2, 3, 4]]
        self.thermostat = Thermostat()
        self.motion = MotionSensor(pin=7)
    
    def on_motion_detected(self):
        self.lights[0].on()
        self.schedule(self.lights[0].off, delay=300)
    
    def set_temperature(self, target):
        self.thermostat.set(target)
```

## Cloud Sync

```python
from ludwig.cloud import CloudSync

cloud = CloudSync(api_key="...")

# Upload sensor data
cloud.log("temperature", 22.5)
cloud.log("humidity", 45)

# Get remote config
config = cloud.get_config()
```
