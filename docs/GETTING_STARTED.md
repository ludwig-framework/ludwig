# Getting Started

This guide covers installation and creating your first Ludwig project.

## Prerequisites

- Python 3.9 or higher
- Git

## Installation

```bash
git clone https://github.com/NanaBright/ludwig.git
cd ludwig
pip install -r requirements.txt
```

Verify installation:

```bash
python artisan.py help
```

## Create a Web Project

```bash
python artisan.py new my_blog web
cd my_blog
python artisan.py dev
```

This creates a complete web application with:
- User authentication
- Database with ORM
- REST API endpoints
- Modern UI with TailwindCSS

## Create a Desktop App

```bash
python artisan.py make:desktop Calculator
python calculator_app.ludwig
```

## Create an Embedded Project

```bash
python artisan.py make:embedded TempSensor
```

## CLI Commands

```bash
# Project creation
python artisan.py new <name> <type>    # Create new project (web, desktop, cli)

# Code generation
python artisan.py make:api <name>      # Generate API with controller
python artisan.py make:auth            # Add authentication
python artisan.py make:desktop <name>  # Generate desktop app
python artisan.py make:embedded <name> # Generate embedded template

# Development
python artisan.py dev                  # Start dev server
python artisan.py serve                # Start interactive REPL
```

## Project Structure

A typical web project:

```
my_blog/
├── main.ludwig          # Entry point
├── config.json          # Configuration
├── controllers/
│   └── HomeController.py
├── models/
│   └── User.py
├── views/
│   └── index.html
└── static/
    └── css/
```

## Next Steps

- [Web Development Guide](WEB_GUIDE.md)
- [Desktop Development Guide](DESKTOP_GUIDE.md)
- [Embedded Systems Guide](EMBEDDED_GUIDE.md)
cd my_app

# Run the application
python artisan.py run main.ludwig
```

### 🔌 Embedded Project

```bash
# Create an IoT device
python artisan.py make:embedded MyDevice

# Run the embedded application
python mydevice_embedded.ludwig
```

---

## Web Development

Ludwig provides Laravel-inspired features for modern web development.

### Creating a Blog Application

```bash
# 1. Create project
python ludwig_setup.py blog web
cd blog

# 2. Generate components
python artisan.py make:controller PostController
python artisan.py make:component BlogCard
python artisan.py make:page Dashboard

# 3. Set up authentication
python artisan.py make:auth

# 4. Start development server
python artisan.py dev
```

### Available Web Commands

| Command | Description |
|---------|-------------|
| `make:controller <name>` | Create a web controller |
| `make:component <name>` | Create a UI component |
| `make:page <name>` | Create a complete page |
| `make:api <name>` | Generate REST API |
| `make:middleware <name>` | Create middleware |

### Features Included

- ✅ **TailwindCSS** for styling
- ✅ **shadcn/ui** components
- ✅ **JWT Authentication**
- ✅ **Form validation**
- ✅ **Database ORM**
- ✅ **REST API generation**

---

## Desktop Applications

Build cross-platform desktop applications with Ludwig's C#-inspired framework.

### Creating a Text Editor

```bash
# 1. Create desktop app
python artisan.py make:desktop TextEditor

# 2. Add forms and services
python artisan.py make:form MainWindow
python artisan.py make:service FileService

# 3. Run the application
python texteditor_app.ludwig
```

### Desktop Features

- 🪟 **Cross-platform GUI**
- 📝 **Forms and controls**
- 🗃️ **File and database services**
- 🔔 **System notifications**
- 🎨 **Layout managers**

### Example Controls

```ludwig
# Create a text editor window
let main_window = create window do
    let title = "Ludwig Text Editor"
    let width = 800
    let height = 600

# Add controls
let text_area = Desktop.textbox({
    "multiline": true,
    "scrollbars": true
})

let menu_bar = Desktop.menubar({
    "File": ["New", "Open", "Save", "Exit"],
    "Edit": ["Cut", "Copy", "Paste"],
    "Help": ["About"]
})
```

---

## Embedded/IoT Systems

Ludwig makes embedded development accessible with hardware abstraction and pre-built templates.

### Quick Start Examples

#### IoT Sensor Device
```bash
python artisan.py make:embedded WeatherStation
```

#### Point of Sale System
```bash
python artisan.py make:pos RetailPOS
```

#### Smart Home Controller
```bash
python artisan.py make:smarthome HomeController
```

#### Robotics System
```bash
python artisan.py make:robotics CleaningBot
```

### Supported Hardware

| Category | Examples |
|----------|----------|
| **Microcontrollers** | Arduino, ESP32, Raspberry Pi |
| **Sensors** | Temperature, Motion, Ultrasonic |
| **Displays** | LCD, OLED, TouchScreen |
| **Communication** | WiFi, Bluetooth, Serial |
| **Actuators** | Motors, Servos, LEDs |

### Example IoT Code

```ludwig
import embedded_framework as Embedded

# Create device
device = Embedded.EmbeddedDevice("WeatherStation", "1.0.0")

# Add sensors
device.add_sensor("temp", Embedded.TemperatureSensor(pin=A0))
device.add_sensor("humidity", Embedded.HumiditySensor(pin=A1))

# Add connectivity
device.add_service("wifi", Embedded.WiFiService())
device.add_service("cloud", Embedded.CloudService())

function main():
    device.initialize()
    
    while device.is_running():
        temp = device.get_sensor("temp").read()
        humidity = device.get_sensor("humidity").read()
        
        device.get_service("cloud").send_data({
            "temperature": temp,
            "humidity": humidity,
            "timestamp": get_timestamp()
        })
        
        device.sleep(60000)  # Send every minute
end
```

---

## CLI Commands Reference

Ludwig's Artisan CLI provides powerful code generation and project management.

### Project Management
```bash
python artisan.py new <name> [template]    # Create new project
python artisan.py templates                # List available templates
python artisan.py version                  # Show version
python artisan.py help                     # Show all commands
```

### Web Development
```bash
python artisan.py make:controller <name>   # Web controller
python artisan.py make:component <name>    # UI component
python artisan.py make:page <name>         # Complete page
python artisan.py make:api <name>          # REST API
python artisan.py make:middleware <name>   # Middleware
python artisan.py dev                      # Start dev server
```

### Desktop Development
```bash
python artisan.py make:desktop <name>      # Desktop app
python artisan.py make:form <name>         # UI form
python artisan.py make:service <name>      # App service
```

### Embedded Development
```bash
python artisan.py make:embedded <name>     # IoT device
python artisan.py make:pos <name>          # POS system
python artisan.py make:kiosk <name>        # QR kiosk
python artisan.py make:scanner <name>      # Barcode scanner
python artisan.py make:smarthome <name>    # Smart home
python artisan.py make:robotics <name>     # Robot controller
```

### Utility Commands
```bash
python artisan.py make:class <name>        # Class file
python artisan.py make:function <name>     # Function file
python artisan.py make:test <name>         # Test file
python artisan.py serve                    # Start REPL
python artisan.py run <file>               # Execute file
```

---

## Next Steps

### 📚 Learn More

- **[Complete Guide](COMPLETE_GUIDE.md)** - Comprehensive feature documentation
- **[Embedded Guide](EMBEDDED_GUIDE.md)** - IoT and embedded development
- **[Desktop Quickstart](DESKTOP_QUICKSTART.md)** - Desktop application development
- **[Examples](../examples/)** - Real-world project examples

### 🛠️ Development

- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute to Ludwig
- **[Architecture Overview](DEVELOPMENT_SUMMARY.md)** - Technical deep-dive
- **[API Reference](PROJECT_STRUCTURE.md)** - Code structure and APIs

### 💬 Community

- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - Community help and questions
- **Contributors** - See our amazing [contributors](../CONTRIBUTORS.md)

### 🎯 Project Ideas

#### Beginner Projects
- **Personal Blog** - Web development with auth and content management
- **Todo App** - Desktop application with local storage
- **Temperature Monitor** - IoT sensor with data logging

#### Intermediate Projects
- **E-commerce Site** - Full-stack web app with payments
- **Media Player** - Desktop app with file management
- **Smart Garden** - IoT system with automated watering

#### Advanced Projects
- **Social Platform** - Scalable web application
- **IDE/Editor** - Complex desktop application
- **Home Automation** - Complete IoT ecosystem

---

## 🆘 Getting Help

### Common Issues

#### Import Errors
```bash
# If you see import errors, check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt
```

#### CLI Not Working
```bash
# Verify Ludwig installation
python artisan.py version

# Check file permissions
ls -la artisan.py
```

#### Embedded Development
```bash
# Install additional dependencies for embedded
pip install pyserial
pip install requests  # For cloud services
```

### Support Channels

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/NanaBright/ludwig/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/NanaBright/ludwig/discussions)
- 📖 **Documentation**: [Ludwig Docs](README.md)
- 🤝 **Contributing**: [Contribution Guide](../CONTRIBUTING.md)

---

## 🎉 Welcome to Ludwig!

You're now ready to build amazing applications with Ludwig! Whether you're creating web applications, desktop software, or IoT devices, Ludwig provides the tools and frameworks you need.

**Happy coding!** 🚀

---

<p align="center">
  <strong>Ludwig: Write less. Build more. Deploy anywhere.</strong>
</p>

<p align="center">
  <a href="../README.md">← Back to Main README</a> |
  <a href="COMPLETE_GUIDE.md">Complete Guide →</a>
</p>
