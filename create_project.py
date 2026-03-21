#!/usr/bin/env python3
"""
Simple Ludwig Project Creator
Creates new Ludwig projects with basic structure.
"""

import os
import sys
import json
from datetime import datetime


def create_web_project(project_name):
    """Create a new web project with the given name."""
    if os.path.exists(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        return False
    
    print(f"Creating web project: {project_name}")
    
    # Create project structure
    directories = [
        project_name,
        f"{project_name}/components",
        f"{project_name}/controllers",
        f"{project_name}/models",
        f"{project_name}/views",
        f"{project_name}/public",
        f"{project_name}/config",
        f"{project_name}/lib",
        f"{project_name}/tests"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create main project file
    main_content = f'''# {project_name.title()} - Ludwig Web Application

# Import Ludwig's native web framework (no external dependencies!)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_framework import Web

# Application configuration
app = Web.create_application({{
    "name": "{project_name}",
    "version": "1.0.0",
    "debug": True
}})

# Route definitions
@app.route("/")
def home(request):
    return Web.render("home.html", {{
        "title": "Welcome to Ludwig",
        "message": "Your Ludwig web application is ready!",
        "timestamp": get_timestamp(),
        "project_name": "{project_name.title()}"
    }})

@app.route("/about")
def about(request):
    return Web.render("about.html", {{
        "title": "About",
        "description": "Built with Ludwig - Write less. Build more. Deploy anywhere.",
        "project_name": "{project_name.title()}"
    }})

@app.route("/api/status")
def api_status(request):
    return Web.json_response({{
        "status": "running",
        "project": "{project_name}",
        "framework": "Ludwig Native Web Framework",
        "dependencies": "None - Pure Python!",
        "timestamp": get_timestamp()
    }})

# Static file serving
app.static("/css", "public/css")
app.static("/js", "public/js")
app.static("/images", "public/images")

def get_timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    print("Starting {project_name.title()} application...")
    print("Using Ludwig Native Web Framework (no external dependencies)")
    print("Application running at http://localhost:8000")
    print("API endpoint: http://localhost:8000/api/status")
    app.run(host="localhost", port=8000, debug=True)

if __name__ == "__main__":
    main()
'''
    
    with open(f"{project_name}/main.ludwig", "w") as f:
        f.write(main_content)
    print(f"✓ Created main application file: {project_name}/main.ludwig")
    
    # Create controller
    controller_content = f'''# Home Controller for Ludwig Web Application

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from web_framework import Web

class HomeController:
    """
    Home Controller - Ludwig Web Application
    Handles main application routes and logic
    """
    
    @staticmethod
    def index(request):
        return Web.render("home.html", {{
            "title": "Welcome to Ludwig",
            "message": "Your Ludwig web application is ready!",
            "timestamp": HomeController.get_timestamp(),
            "project_name": "{project_name.title()}"
        }})
    
    @staticmethod
    def about(request):
        return Web.render("about.html", {{
            "title": "About",
            "description": "Built with Ludwig - Write less. Build more. Deploy anywhere.",
            "project_name": "{project_name.title()}"
        }})
    
    @staticmethod
    def api_info(request):
        return Web.json_response({{
            "project": "{project_name}",
            "controller": "HomeController", 
            "framework": "Ludwig Native",
            "timestamp": HomeController.get_timestamp()
        }})
    
    @staticmethod
    def get_timestamp():
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Example usage:
# This controller can be imported and used in your main.ludwig file
# 
# from controllers.home_controller import HomeController
# app.route("/", HomeController.index)
# app.route("/about", HomeController.about)
'''
    
    with open(f"{project_name}/controllers/home_controller.ludwig", "w") as f:
        f.write(controller_content)
    print(f"✓ Created controller: {project_name}/controllers/home_controller.ludwig")
    
    # Create views
    home_view = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title }}}} - {project_name.title()}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
    <div class="container mx-auto px-4 py-16">
        <div class="max-w-4xl mx-auto text-center">
            <div class="mb-8">
                <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full mb-6">
                    <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                </div>
                <h1 class="text-5xl font-bold text-gray-900 mb-4">{{{{ title }}}}</h1>
                <p class="text-xl text-gray-600 mb-8">{{{{ message }}}}</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8 mb-12">
                <div class="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                    <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Web Framework</h3>
                    <p class="text-gray-600">Laravel-inspired features with modern tooling</p>
                </div>
                
                <div class="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                    <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Components</h3>
                    <p class="text-gray-600">Reusable UI components with TailwindCSS</p>
                </div>
                
                <div class="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                    <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Configuration</h3>
                    <p class="text-gray-600">Easy setup and deployment options</p>
                </div>
            </div>
            
            <div class="bg-white rounded-xl p-8 shadow-lg">
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Quick Start</h2>
                <div class="bg-gray-50 rounded-lg p-4 text-left">
                    <code class="text-sm text-gray-700">
                        # Start development server<br>
                        python artisan.py dev<br><br>
                        # Generate new components<br>
                        python artisan.py make:component MyComponent<br>
                        python artisan.py make:controller ApiController
                    </code>
                </div>
            </div>
            
            <footer class="mt-12 text-center">
                <p class="text-gray-500">Generated at {{{{ timestamp }}}}</p>
                <p class="text-gray-400 mt-2">
                    <a href="/about" class="text-blue-600 hover:underline">About</a> • 
                    <a href="https://github.com/NanaBright/ludwig" class="text-blue-600 hover:underline">GitHub</a>
                </p>
            </footer>
        </div>
    </div>
</body>
</html>'''
    
    with open(f"{project_name}/views/home.html", "w") as f:
        f.write(home_view)
    print(f"✓ Created view: {project_name}/views/home.html")
    
    # Create about view
    about_view = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title }}}} - {project_name.title()}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="bg-gradient-to-br from-purple-50 to-pink-100 min-h-screen">
    <div class="container mx-auto px-4 py-16">
        <div class="max-w-3xl mx-auto">
            <div class="text-center mb-12">
                <h1 class="text-4xl font-bold text-gray-900 mb-4">{{{{ title }}}}</h1>
                <p class="text-xl text-gray-600">{{{{ description }}}}</p>
            </div>
            
            <div class="bg-white rounded-xl p-8 shadow-lg mb-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">About Ludwig</h2>
                <div class="prose prose-lg text-gray-600">
                    <p>Ludwig is a modern, multi-platform development framework that simplifies building applications across Web, Desktop, and Embedded/IoT systems.</p>
                    
                    <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">Key Features:</h3>
                    <ul class="space-y-2">
                        <li><strong>Web Development</strong> - Laravel-inspired framework with TailwindCSS</li>
                        <li><strong>Desktop Applications</strong> - Cross-platform GUI development</li>
                        <li><strong>Embedded/IoT</strong> - Hardware abstraction for sensors and devices</li>
                        <li><strong>Powerful CLI</strong> - Artisan-style code generation tools</li>
                    </ul>
                    
                    <h3 class="text-lg font-semibold text-gray-900 mt-6 mb-3">This Project:</h3>
                    <p>You've created <strong>{project_name.title()}</strong>, a Ludwig web application with a modern, responsive design using TailwindCSS and best practices.</p>
                </div>
            </div>
            
            <div class="text-center">
                <a href="/" class="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                    </svg>
                    Back to Home
                </a>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(f"{project_name}/views/about.html", "w") as f:
        f.write(about_view)
    print(f"✓ Created view: {project_name}/views/about.html")
    
    # Create package.json for web dependencies (optional)
    package_json = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"Ludwig web application: {project_name}",
        "scripts": {
            "dev": "python main.ludwig",
            "build": "echo 'Building for production...'",
            "test": "echo 'Running tests...'"
        },
        "dependencies": {},
        "devDependencies": {
            "tailwindcss": "^3.0.0"
        }
    }
    
    with open(f"{project_name}/package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    print(f"✓ Created package.json: {project_name}/package.json")
    
    # Create ludwig.json project config
    ludwig_config = {
        "name": project_name,
        "version": "1.0.0",
        "type": "web",
        "main": "main.ludwig",
        "framework": {
            "web": {
                "port": 8000,
                "host": "localhost",
                "static_dir": "public",
                "template_dir": "views"
            }
        },
        "dependencies": {
            "web_framework": "^0.1.0"
        }
    }
    
    with open(f"{project_name}/ludwig.json", "w") as f:
        json.dump(ludwig_config, f, indent=2)
    print(f"✓ Created project config: {project_name}/ludwig.json")
    
    # Create README
    readme_content = f'''# {project_name.title()}

A Ludwig web application with modern design and TailwindCSS styling.

## Quick Start

```bash
# Navigate to project directory
cd {project_name}

# Start development server
python main.ludwig

# Or use Ludwig CLI
python ../artisan.py dev
```

Your application will be available at: http://localhost:8000

## Project Structure

```
{project_name}/
├── main.ludwig              # Main application file
├── ludwig.json              # Project configuration
├── package.json             # Dependencies (optional)
├── controllers/             # Application controllers
│   └── home_controller.ludwig
├── views/                   # HTML templates
│   ├── home.html
│   └── about.html
├── components/              # Reusable UI components
├── models/                  # Data models
├── public/                  # Static assets (CSS, JS, images)
├── config/                  # Configuration files
├── lib/                     # Custom libraries
└── tests/                   # Test files
```

## Available Commands

```bash
# Generate new components
python ../artisan.py make:component ComponentName
python ../artisan.py make:controller ControllerName
python ../artisan.py make:page PageName

# Development tools
python ../artisan.py dev        # Start dev server
python ../artisan.py build      # Build for production
```

## Features

- **Modern Design** - TailwindCSS styling with responsive layout
- **Component Architecture** - Modular and reusable components
- **MVC Pattern** - Clean separation of concerns
- **Static Assets** - CSS, JS, and image handling
- **Hot Reload** - Development server with live updates

## Learn More

- [Ludwig Documentation](../docs/README.md)
- [Web Development Guide](../docs/COMPLETE_GUIDE.md)
- [Component Examples](../examples/web/)

---

*Generated with Ludwig v0.1.0 - Write less. Build more. Deploy anywhere.* ✨
'''
    
    with open(f"{project_name}/README.md", "w") as f:
        f.write(readme_content)
    print(f"✓ Created documentation: {project_name}/README.md")
    
    # Success message
    print(f"""
Successfully created Ludwig web project: {project_name.title()}

Project created in: ./{project_name}/
Type: Web Application
Styling: TailwindCSS + Modern Design

Next Steps:
   1. cd {project_name}
   2. python main.ludwig
   3. Open http://localhost:8000 in your browser

""")
    
    return True


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Ludwig Project Creator")
        print("Usage: python create_project.py <project_name> <type>")
        print("Types: web, desktop, embedded")
        print()
        print("Example: python create_project.py dashboard-demo web")
        return
    
    project_name = sys.argv[1]
    project_type = sys.argv[2].lower()
    
    if project_type == "web":
        create_web_project(project_name)
    else:
        print(f"Project type '{project_type}' not implemented yet.")
        print("Available types: web")
        print("Coming soon: desktop, embedded")


if __name__ == "__main__":
    main()
