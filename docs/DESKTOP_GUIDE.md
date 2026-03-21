# Desktop Development Guide

Ludwig provides a cross-platform desktop framework inspired by C#/.NET.

## Creating a Desktop App

```bash
python artisan.py make:desktop MyApp
python myapp_app.ludwig
```

## Application Structure

```python
class MyApp(Application):
    def __init__(self):
        self.title = "My Application"
        self.width = 800
        self.height = 600
    
    def on_start(self):
        self.main_window = MainWindow()
        self.main_window.show()
```

## Windows

```python
class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.title = "Main Window"
        
        # Add controls
        self.add(Label("Hello, World!"))
        self.add(Button("Click Me", on_click=self.handle_click))
    
    def handle_click(self, event):
        MessageBox.show("Button clicked!")
```

## Controls

Available controls:
- `Label` - Text display
- `Button` - Clickable button
- `TextBox` - Text input
- `CheckBox` - Boolean toggle
- `ComboBox` - Dropdown selection
- `ListView` - List display
- `TreeView` - Hierarchical display
- `ProgressBar` - Progress indicator

## Layouts

```python
# Stack layout (vertical)
layout = StackLayout(orientation="vertical")
layout.add(Label("Name:"))
layout.add(TextBox())

# Grid layout
layout = GridLayout(rows=2, cols=2)
layout.add(Label("First:"), row=0, col=0)
layout.add(TextBox(), row=0, col=1)

# Border layout
layout = BorderLayout()
layout.add(Menu(), position="top")
layout.add(Sidebar(), position="left")
layout.add(Content(), position="center")
```

## Events

```python
button = Button("Submit")
button.on_click = self.handle_submit

textbox = TextBox()
textbox.on_change = self.handle_text_change
textbox.on_key_press = self.handle_key
```

## Menus

```python
menu = Menu()
file_menu = menu.add_submenu("File")
file_menu.add_item("New", self.new_file, shortcut="Ctrl+N")
file_menu.add_item("Open", self.open_file, shortcut="Ctrl+O")
file_menu.add_separator()
file_menu.add_item("Exit", self.exit_app)
```

## Services

Built-in services:

```python
# File service
from ludwig.services import FileService

content = FileService.read("document.txt")
FileService.write("output.txt", content)
path = FileService.open_dialog(filters=["*.txt", "*.md"])

# HTTP service
from ludwig.services import HttpService

response = HttpService.get("https://api.example.com/data")
data = response.json()

# Database service
from ludwig.services import DatabaseService

db = DatabaseService.connect("sqlite:///app.db")
users = db.query("SELECT * FROM users")

# Notification service
from ludwig.services import NotificationService

NotificationService.show("Title", "Message body")
```

## System Tray

```python
tray = SystemTray(icon="icon.png")
tray.add_item("Show", self.show_window)
tray.add_item("Exit", self.exit_app)
tray.show()
```
