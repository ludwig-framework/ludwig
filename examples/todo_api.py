"""
Todo API Example - REST API with SQLite database
"""

from dataclasses import dataclass
from ludwig import App, Database, Model

app = App(name="Todo API")
db = Database("todos.db")


@dataclass
class Todo(Model):
    title: str
    completed: bool = False


@app.get("/")
def home(req):
    return {
        "name": "Todo API",
        "endpoints": {
            "GET /todos": "List all todos",
            "POST /todos": "Create a todo",
            "GET /todos/:id": "Get a todo",
            "PUT /todos/:id": "Update a todo",
            "DELETE /todos/:id": "Delete a todo",
        }
    }


@app.get("/todos")
def list_todos(req):
    todos = Todo.all()
    return [t.to_dict() for t in todos]


@app.post("/todos")
def create_todo(req):
    todo = Todo.create(**req.json)
    return todo.to_dict()


@app.get("/todos/:id")
def get_todo(req):
    todo = Todo.find(int(req.params["id"]))
    if not todo:
        return {"error": "Todo not found"}, 404
    return todo.to_dict()


@app.put("/todos/:id")
def update_todo(req):
    todo = Todo.find(int(req.params["id"]))
    if not todo:
        return {"error": "Todo not found"}, 404
    
    for key, value in req.json.items():
        if hasattr(todo, key):
            setattr(todo, key, value)
    todo.save()
    return todo.to_dict()


@app.delete("/todos/:id")
def delete_todo(req):
    todo = Todo.find(int(req.params["id"]))
    if not todo:
        return {"error": "Todo not found"}, 404
    todo.delete()
    return {"deleted": True}


if __name__ == "__main__":
    print("Todo API at http://localhost:8000")
    print("Try: curl http://localhost:8000/todos")
    app.run(debug=True)
