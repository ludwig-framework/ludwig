# Web Development with Ludwig

Build REST APIs and web applications with Ludwig's built-in HTTP server.

## Quick Start

```python
from ludwig import App

app = App()

@app.get("/")
def home(req):
    return "Hello, World!"

app.run()
```

## Routing

### HTTP Methods

```python
@app.get("/users")
def list_users(req):
    return {"users": []}

@app.post("/users")
def create_user(req):
    data = req.json
    return {"created": data}

@app.put("/users/:id")
def update_user(req):
    return {"updated": req.params["id"]}

@app.delete("/users/:id")
def delete_user(req):
    return {"deleted": req.params["id"]}
```

### URL Parameters

```python
@app.get("/users/:id")
def get_user(req):
    user_id = req.params["id"]
    return {"id": user_id}

@app.get("/posts/:category/:slug")
def get_post(req):
    category = req.params["category"]
    slug = req.params["slug"]
    return {"category": category, "slug": slug}
```

### Query Parameters

```python
@app.get("/search")
def search(req):
    query = req.query.get("q", "")
    page = int(req.query.get("page", 1))
    return {"query": query, "page": page}
```

## Request Object

```python
@app.post("/upload")
def upload(req):
    # JSON body
    data = req.json
    
    # Raw body
    body = req.body
    
    # Headers
    auth = req.headers.get("Authorization")
    
    # Method and path
    print(req.method)  # "POST"
    print(req.path)    # "/upload"
    
    return {"received": True}
```

## Responses

### JSON Response

```python
@app.get("/api/data")
def data(req):
    return {"status": "ok", "data": [1, 2, 3]}
```

### HTML Response

```python
@app.get("/page")
def page(req):
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Hello!</h1>
    </body>
    </html>
    """
```

### Status Codes

```python
@app.get("/item/:id")
def get_item(req):
    item = find_item(req.params["id"])
    if not item:
        return {"error": "Not found"}, 404
    return item
```

### Redirects

```python
from ludwig.web import redirect

@app.get("/old-page")
def old_page(req):
    return redirect("/new-page")
```

## Database Integration

### Setup

```python
from ludwig import App, Database, Model
from dataclasses import dataclass

app = App()
db = Database("app.db")  # SQLite
# db = Database("postgres://user:pass@localhost/db")  # PostgreSQL
```

### Models

```python
@dataclass
class User(Model):
    name: str
    email: str
    age: int = 0
```

### CRUD Operations

```python
@app.get("/users")
def list_users(req):
    users = User.all()
    return [u.to_dict() for u in users]

@app.post("/users")
def create_user(req):
    user = User.create(**req.json)
    return user.to_dict()

@app.get("/users/:id")
def get_user(req):
    user = User.find(int(req.params["id"]))
    if not user:
        return {"error": "Not found"}, 404
    return user.to_dict()

@app.put("/users/:id")
def update_user(req):
    user = User.find(int(req.params["id"]))
    if not user:
        return {"error": "Not found"}, 404
    
    for key, value in req.json.items():
        setattr(user, key, value)
    user.save()
    return user.to_dict()

@app.delete("/users/:id")
def delete_user(req):
    user = User.find(int(req.params["id"]))
    if not user:
        return {"error": "Not found"}, 404
    user.delete()
    return {"deleted": True}
```

### Query Builder

```python
# Find with conditions
adults = User.where("age", ">=", 18)

# Using query builder directly
results = db.table("users") \
    .where("age", ">", 21) \
    .order_by("name") \
    .limit(10) \
    .get()
```

## Static Files

```python
app = App(static_dir="public")
# Files in public/ are served at /static/
```

## Configuration

```python
app = App(
    name="My API",
    host="0.0.0.0",
    port=8000,
    debug=True,
    static_dir="public",
)
```

## Full Example

```python
from ludwig import App, Database, Model
from dataclasses import dataclass

app = App(name="Todo API")
db = Database("todos.db")

@dataclass
class Todo(Model):
    title: str
    completed: bool = False

@app.get("/")
def home(req):
    return {"name": "Todo API", "version": "1.0"}

@app.get("/todos")
def list_todos(req):
    todos = Todo.all()
    return [t.to_dict() for t in todos]

@app.post("/todos")
def create_todo(req):
    todo = Todo.create(**req.json)
    return todo.to_dict()

@app.put("/todos/:id/complete")
def complete_todo(req):
    todo = Todo.find(int(req.params["id"]))
    if todo:
        todo.completed = True
        todo.save()
        return todo.to_dict()
    return {"error": "Not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)
```
