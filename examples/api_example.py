"""
Simple API Example
"""

from ludwig import App

app = App(name="Hello API")


@app.get("/")
def home(req):
    return {"message": "Welcome to Ludwig!", "version": "2.0.0"}


@app.get("/hello/:name")
def hello(req):
    name = req.params["name"]
    return {"message": f"Hello, {name}!"}


@app.get("/status")
def status(req):
    return {"status": "ok", "uptime": "running"}


if __name__ == "__main__":
    print("Starting API at http://localhost:8000")
    app.run(debug=True)
