<p align="center">
  <img src="https://raw.githubusercontent.com/NanaBright/ludwig/main/assets/logo.png" alt="Ludwig Logo" width="160"/>
</p>

<h1 align="center">Ludwig</h1>
<p align="center">A Python web framework with Laravel-style elegance</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://github.com/NanaBright/ludwig/stargazers"><img src="https://img.shields.io/github/stars/NanaBright/ludwig?style=flat&logo=github&color=yellow" alt="Stars"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.9+-blue" alt="Python 3.9+"></a>
</p>

---

## What is Ludwig?

Ludwig is a Python framework that brings Laravel's developer experience to Python. Build web applications, desktop apps, and embedded systems with a clean, expressive syntax and zero external framework dependencies.

```python
# Create a web app in seconds
python artisan.py new my_blog web
cd my_blog
python main.ludwig
```

---

## Features

**Web Development**
- Pure Python HTTP server - no Flask or Django required
- Laravel-style routing and controllers
- Built-in ORM with Eloquent-style syntax
- JWT authentication out of the box
- TailwindCSS + modern UI components

**Desktop Development**
- Cross-platform GUI framework
- C#/.NET-inspired API
- Forms, layouts, and system integration

**Embedded/IoT**
- Templates for Arduino, Raspberry Pi, ESP32
- Hardware abstraction for sensors and actuators
- POS, kiosk, and smart home generators

**Developer Tools**
- Artisan CLI for code generation
- Interactive REPL
- Project templates for all platforms

---

## Quick Start

```bash
git clone https://github.com/NanaBright/ludwig.git
cd ludwig
pip install -r requirements.txt
```

### Create a Web App

```bash
python artisan.py new my_blog web
cd my_blog
python artisan.py dev
```

### Generate Components

```bash
# Create API with model
python artisan.py make:api posts --model

# Add authentication
python artisan.py make:auth

# Create desktop app
python artisan.py make:desktop Calculator
```

---

## Web Framework Example

```python
# Define a model
class Post(Model):
    table_name = "posts"
    fillable = ["title", "content", "author_id"]

# Query with Eloquent-style syntax    
posts = Post.query() \
    .where("published", True) \
    .order_by("created_at", "desc") \
    .paginate(1, 10)

# Authentication
auth_result = AuthController.login({
    "email": "user@example.com",
    "password": "secret"
})
# Returns JWT token
```

---

## Project Structure

```
ludwig/
├── artisan.py           # CLI tool
├── web_framework.py     # Web framework core
├── auth.py              # Authentication system
├── src/
│   ├── frameworks/      # Framework implementations
│   └── templates/       # Project templates
├── examples/            # Example projects
└── docs/                # Documentation
```

---

## Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [Web Development Guide](docs/WEB_GUIDE.md)
- [Desktop Development](docs/DESKTOP_GUIDE.md)
- [Embedded Systems](docs/EMBEDDED_GUIDE.md)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE)
