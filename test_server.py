"""
Ludwig Test Server - For verification and screenshots
"""
import sys
sys.path.insert(0, '/Users/user/Desktop/NBStuff/dev/ludwig')

from ludwig import App

app = App(name="Ludwig Test")

@app.route("/")
def home(req):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ludwig Framework - Test</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: system-ui, -apple-system, sans-serif; 
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                min-height: 100vh;
                color: white;
            }
            .container { max-width: 900px; margin: 0 auto; padding: 60px 20px; }
            h1 { 
                font-size: 48px; 
                margin-bottom: 16px;
                background: linear-gradient(90deg, #00d4ff, #7b2ff7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtitle { color: #888; font-size: 20px; margin-bottom: 48px; }
            .status { 
                display: inline-block;
                background: #2ecc71; 
                color: white; 
                padding: 8px 16px; 
                border-radius: 20px; 
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 32px;
            }
            .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 48px; }
            .card { 
                background: rgba(255,255,255,0.05); 
                padding: 24px; 
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);
                transition: transform 0.2s, border-color 0.2s;
            }
            .card:hover { 
                transform: translateY(-4px);
                border-color: #00d4ff;
            }
            .card h3 { margin-bottom: 12px; color: #00d4ff; }
            .card p { color: #999; font-size: 14px; line-height: 1.6; }
            .endpoints { background: rgba(0,0,0,0.3); border-radius: 12px; padding: 24px; }
            .endpoints h2 { margin-bottom: 16px; font-size: 20px; }
            .endpoint { 
                display: flex; 
                align-items: center; 
                padding: 12px 0; 
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .endpoint:last-child { border-bottom: none; }
            .method { 
                background: #00d4ff; 
                color: #000; 
                padding: 4px 12px; 
                border-radius: 4px; 
                font-size: 12px; 
                font-weight: 600;
                margin-right: 16px;
                min-width: 50px;
                text-align: center;
            }
            .method.post { background: #7b2ff7; color: white; }
            .path { font-family: monospace; color: #00d4ff; }
            .desc { color: #666; margin-left: auto; font-size: 14px; }
            footer { text-align: center; margin-top: 48px; color: #666; }
            footer a { color: #00d4ff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="status">SERVER RUNNING</span>
            <h1>Ludwig Framework</h1>
            <p class="subtitle">Simple Python for Web, IoT, and AI</p>
            
            <div class="grid">
                <div class="card">
                    <h3>Web</h3>
                    <p>Build REST APIs and web apps with simple decorators. No boilerplate.</p>
                </div>
                <div class="card">
                    <h3>IoT</h3>
                    <p>Control robots, sensors, alarms, and smart home devices.</p>
                </div>
                <div class="card">
                    <h3>AI</h3>
                    <p>Voice assistants, computer vision, and automation with GPT-4.</p>
                </div>
            </div>
            
            <div class="endpoints">
                <h2>Test Endpoints</h2>
                <div class="endpoint">
                    <span class="method">GET</span>
                    <span class="path">/</span>
                    <span class="desc">This page</span>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span>
                    <span class="path">/api/status</span>
                    <span class="desc">Server status JSON</span>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span>
                    <span class="path">/api/modules</span>
                    <span class="desc">Available modules</span>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <span class="path">/api/echo</span>
                    <span class="desc">Echo POST data</span>
                </div>
            </div>
            
            <footer>
                <p>Ludwig v2.0.0 | <a href="https://github.com/ludwig-framework/ludwig">GitHub</a></p>
            </footer>
        </div>
    </body>
    </html>
    """

@app.route("/api/status")
def status(req):
    return {
        "status": "running",
        "version": "2.0.0",
        "framework": "Ludwig",
        "modules": ["core", "web", "iot", "ai", "db"]
    }

@app.route("/api/modules")
def modules(req):
    return {
        "iot": ["Robot", "Alarm", "Sensor", "Light", "Camera", "Home", "Garden"],
        "ai": ["Assistant", "Vision", "Automator"],
        "web": ["App", "route"],
        "db": ["Database", "Model"]
    }

@app.route("/api/echo", methods=["POST"])
def echo(req):
    return {"received": req.json, "echo": True}

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Ludwig Test Server")
    print("="*50)
    print("\nOpen http://localhost:8000 in your browser")
    print("\nPress Ctrl+C to stop\n")
    app.run(port=8000)
