"""
Ludwig Core - Application foundation
"""

from typing import Any, Callable, Optional
from dataclasses import dataclass, field
import json
import os


@dataclass
class Config:
    """Application configuration."""
    
    name: str = "Ludwig App"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: Optional[str] = None
    
    # IoT
    board: str = "auto"  # auto, raspberry_pi, esp32, arduino
    
    # AI
    openai_key: Optional[str] = None
    model: str = "gpt-4o"
    
    @classmethod
    def from_file(cls, path: str = "ludwig.json") -> "Config":
        """Load config from JSON file."""
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            return cls(**data)
        return cls()
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment variables."""
        return cls(
            name=os.getenv("LUDWIG_APP_NAME", "Ludwig App"),
            debug=os.getenv("LUDWIG_DEBUG", "false").lower() == "true",
            host=os.getenv("LUDWIG_HOST", "0.0.0.0"),
            port=int(os.getenv("LUDWIG_PORT", "8000")),
            database_url=os.getenv("DATABASE_URL"),
            openai_key=os.getenv("OPENAI_API_KEY"),
        )


class App:
    """
    Base Ludwig application.
    
    Unifies Web, IoT, and AI capabilities.
    
    Example:
        app = App(name="My Project")
        
        @app.route("/")
        def home():
            return "Hello!"
        
        @app.on_sensor("motion")
        def motion_detected():
            app.light.on()
        
        app.run()
    """
    
    def __init__(
        self,
        name: str = "Ludwig App",
        config: Optional[Config] = None,
        **kwargs
    ):
        self.name = name
        self.config = config or Config(name=name, **kwargs)
        
        self._routes: dict[str, Callable] = {}
        self._events: dict[str, list[Callable]] = {}
        self._tasks: list[Callable] = []
        
        # Components (lazy loaded)
        self._web = None
        self._iot = None
        self._ai = None
    
    # === Web Methods ===
    
    def route(self, path: str, methods: list[str] = None):
        """Register a web route."""
        methods = methods or ["GET"]
        
        def decorator(func: Callable):
            for method in methods:
                key = f"{method}:{path}"
                self._routes[key] = func
            return func
        return decorator
    
    def get(self, path: str):
        """Register a GET route."""
        return self.route(path, ["GET"])
    
    def post(self, path: str):
        """Register a POST route."""
        return self.route(path, ["POST"])
    
    def api(self, path: str):
        """Register a REST API endpoint."""
        return self.route(path, ["GET", "POST", "PUT", "DELETE"])
    
    # === Event Methods ===
    
    def on(self, event: str):
        """Register an event handler."""
        def decorator(func: Callable):
            if event not in self._events:
                self._events[event] = []
            self._events[event].append(func)
            return func
        return decorator
    
    def emit(self, event: str, *args, **kwargs):
        """Emit an event to all handlers."""
        handlers = self._events.get(event, [])
        for handler in handlers:
            handler(*args, **kwargs)
    
    # === Task Methods ===
    
    def every(self, interval: str):
        """
        Schedule a recurring task.
        
        Example:
            @app.every("1 hour")
            def check_sensors():
                pass
        """
        def decorator(func: Callable):
            self._tasks.append((interval, func))
            return func
        return decorator
    
    def at(self, time: str):
        """
        Schedule a task at a specific time.
        
        Example:
            @app.at("sunset")
            def evening_mode():
                pass
        """
        def decorator(func: Callable):
            self._tasks.append((f"at:{time}", func))
            return func
        return decorator
    
    # === Run ===
    
    def run(self, host: str = None, port: int = None, debug: bool = None, reload: bool = False):
        """Start the application.
        
        Args:
            host: Server host (default: 0.0.0.0)
            port: Server port (default: 8000)
            debug: Enable debug mode
            reload: Auto-reload on file changes (for development)
        """
        import os
        
        # Check if we're in a reload subprocess
        if os.environ.get('LUDWIG_NO_RELOAD'):
            reload = False
        
        # Check if dev server requested reload
        if os.environ.get('LUDWIG_DEV_RELOAD'):
            reload = True
        
        host = host or self.config.host
        port = port or self.config.port
        debug = debug if debug is not None else self.config.debug
        
        print(f"🚀 Ludwig {self.name} starting...")
        print(f"   Host: {host}:{port}")
        print(f"   Debug: {debug}")
        if reload:
            print(f"   Reload: enabled")
        
        if self._routes:
            self._start_web_server(host, port, debug, reload)
        elif self._events or self._tasks:
            self._start_event_loop()
        else:
            print("   No routes or events registered.")
    
    def _start_web_server(self, host: str, port: int, debug: bool, reload: bool = False):
        """Start the web server."""
        from ludwig.web import Web
        self._web = Web(routes=self._routes)
        self._web.run(host=host, port=port, debug=debug, reload=reload)
    
    def _start_event_loop(self):
        """Start the event loop for IoT/scheduled tasks."""
        import asyncio
        print("   Running event loop (Ctrl+C to stop)")
        try:
            asyncio.run(self._event_loop())
        except KeyboardInterrupt:
            print("\n   Shutting down...")
    
    async def _event_loop(self):
        """Main event loop."""
        import asyncio
        while True:
            await asyncio.sleep(0.1)
