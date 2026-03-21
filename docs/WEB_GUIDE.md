# Web Development Guide

Ludwig provides a pure Python web framework inspired by Laravel.

## Creating a Web Project

```bash
python artisan.py new my_app web
cd my_app
python artisan.py dev
```

## Routing

Define routes in your application:

```python
routes = [
    Route("GET", "/", "HomeController.index"),
    Route("GET", "/posts", "PostController.index"),
    Route("POST", "/posts", "PostController.store"),
    Route("GET", "/posts/{id}", "PostController.show"),
]
```

## Controllers

```python
class PostController:
    def index(self, request):
        posts = Post.query().all()
        return Response.json(posts)
    
    def store(self, request):
        post = Post.create(request.body)
        return Response.json(post, status=201)
    
    def show(self, request, id):
        post = Post.find(id)
        return Response.json(post)
```

## Models (ORM)

Ludwig uses an Eloquent-style ORM:

```python
class Post(Model):
    table_name = "posts"
    fillable = ["title", "content", "author_id"]
    
# Query examples
posts = Post.query().where("published", True).get()
post = Post.find(1)
post = Post.create({"title": "Hello", "content": "World"})
```

## Authentication

Add authentication with one command:

```bash
python artisan.py make:auth
```

This generates:
- User model
- AuthController with register/login
- JWT middleware
- Protected routes

```python
# Login
result = AuthController.login({
    "email": "user@example.com",
    "password": "secret"
})
# Returns: {"token": "jwt...", "user": {...}}

# Protected route
@middleware("auth")
def dashboard(request):
    user = request.user
    return Response.json({"message": f"Hello {user.name}"})
```

## API Generation

Generate complete CRUD APIs:

```bash
python artisan.py make:api posts --model
```

Creates:
- PostsController with index, store, show, update, destroy
- Post model
- Database migration

## Response Types

```python
# JSON response
return Response.json({"data": posts})

# HTML template
return Response.view("posts/index.html", {"posts": posts})

# Redirect
return Response.redirect("/login")

# File download
return Response.download("report.pdf")
```

## Middleware

```python
def auth_middleware(request, next):
    token = request.headers.get("Authorization")
    if not verify_token(token):
        return Response.json({"error": "Unauthorized"}, status=401)
    return next(request)
```

## Validation

```python
from ludwig.validation import Validator

rules = {
    "title": "required|string|max:255",
    "content": "required|string",
    "email": "required|email"
}

errors = Validator.validate(request.body, rules)
if errors:
    return Response.json({"errors": errors}, status=422)
```

## Static Files

Static files are served from the `static/` directory:

```
my_app/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
```

## Configuration

```json
{
    "app": {
        "name": "My App",
        "port": 3000,
        "debug": true
    },
    "database": {
        "driver": "sqlite",
        "database": "db.sqlite"
    }
}
```
