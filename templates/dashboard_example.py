"""
Ludwig Dashboard Template
Simple web dashboard with live stats and charts.
"""
from ludwig import App, route

app = App()

# Sample data
stats = {
    "users": 1234,
    "orders": 567,
    "revenue": 45678.90,
    "growth": 12.5
}

@route("/")
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body { font-family: system-ui; margin: 40px; background: #f5f5f5; }
            .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
            .card { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stat { font-size: 32px; font-weight: bold; color: #333; }
            .label { color: #666; margin-top: 8px; }
            h1 { margin-bottom: 24px; }
        </style>
    </head>
    <body>
        <h1>Dashboard</h1>
        <div class="grid">
            <div class="card">
                <div class="stat">1,234</div>
                <div class="label">Total Users</div>
            </div>
            <div class="card">
                <div class="stat">567</div>
                <div class="label">Orders</div>
            </div>
            <div class="card">
                <div class="stat">$45,678</div>
                <div class="label">Revenue</div>
            </div>
            <div class="card">
                <div class="stat">+12.5%</div>
                <div class="label">Growth</div>
            </div>
        </div>
    </body>
    </html>
    """

@route("/api/stats")
def api_stats():
    return stats

if __name__ == "__main__":
    app.run(port=8000)
