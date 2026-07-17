"""
Ludwig Web - Simple HTTP server and routing
"""

from typing import Any, Callable, Optional, Union
from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import re
import os


@dataclass
class Request:
    """HTTP Request object."""
    method: str
    path: str
    query: dict
    headers: dict
    body: Any = None
    params: dict = None  # URL parameters like /users/:id
    
    @property
    def json(self) -> dict:
        """Parse body as JSON."""
        if isinstance(self.body, dict):
            return self.body
        if isinstance(self.body, str):
            return json.loads(self.body)
        return {}


@dataclass  
class Response:
    """HTTP Response object."""
    body: Any
    status: int = 200
    headers: dict = None
    content_type: str = "text/html"
    
    def __post_init__(self):
        self.headers = self.headers or {}


def json_response(data: Any, status: int = 200) -> Response:
    """Create a JSON response."""
    return Response(
        body=json.dumps(data),
        status=status,
        content_type="application/json"
    )


def html_response(content: str, status: int = 200) -> Response:
    """Create an HTML response."""
    return Response(body=content, status=status, content_type="text/html")


def redirect(url: str, status: int = 302) -> Response:
    """Create a redirect response."""
    return Response(body="", status=status, headers={"Location": url})


class Web:
    """
    Simple HTTP server for Ludwig.
    
    Example:
        web = Web()
        
        @web.get("/")
        def home(req):
            return "Hello Ludwig!"
        
        @web.get("/api/users")
        def users(req):
            return {"users": ["alice", "bob"]}
        
        web.run()
    """
    
    def __init__(self, routes: dict = None):
        self._routes: dict[str, tuple[str, Callable]] = {}
        self._static_dirs: dict[str, str] = {}
        self._middleware: list[Callable] = []
        
        # Import existing routes if provided
        if routes:
            for key, handler in routes.items():
                method, path = key.split(":", 1)
                self._routes[key] = (self._path_to_regex(path), handler)
    
    def _path_to_regex(self, path: str) -> str:
        """Convert path with :params to regex."""
        # /users/:id -> /users/(?P<id>[^/]+)
        pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', path)
        return f"^{pattern}$"
    
    def route(self, path: str, methods: list[str] = None):
        """Register a route."""
        methods = methods or ["GET"]
        regex = self._path_to_regex(path)
        
        def decorator(func: Callable):
            for method in methods:
                key = f"{method}:{path}"
                self._routes[key] = (regex, func)
            return func
        return decorator
    
    def get(self, path: str):
        """Register GET route."""
        return self.route(path, ["GET"])
    
    def post(self, path: str):
        """Register POST route."""
        return self.route(path, ["POST"])
    
    def put(self, path: str):
        """Register PUT route."""
        return self.route(path, ["PUT"])
    
    def delete(self, path: str):
        """Register DELETE route."""
        return self.route(path, ["DELETE"])
    
    def api(self, path: str):
        """Register REST API (all methods)."""
        return self.route(path, ["GET", "POST", "PUT", "DELETE"])
    
    def static(self, url_path: str, dir_path: str):
        """Serve static files."""
        self._static_dirs[url_path] = dir_path
    
    def use(self, middleware: Callable):
        """Add middleware."""
        self._middleware.append(middleware)
    
    def _find_route(self, method: str, path: str) -> tuple[Callable, dict]:
        """Find matching route and extract params."""
        for key, (regex, handler) in self._routes.items():
            route_method = key.split(":")[0]
            if route_method != method:
                continue
            
            match = re.match(regex, path)
            if match:
                return handler, match.groupdict()
        
        return None, {}
    
    def _handle_request(self, method: str, path: str, headers: dict, body: Any) -> Response:
        """Handle an HTTP request."""
        parsed = urlparse(path)
        query = parse_qs(parsed.query)
        
        # Check static files
        for url_prefix, dir_path in self._static_dirs.items():
            if parsed.path.startswith(url_prefix):
                file_path = parsed.path[len(url_prefix):]
                full_path = os.path.join(dir_path, file_path.lstrip("/"))
                if os.path.isfile(full_path):
                    with open(full_path, "rb") as f:
                        content = f.read()
                    content_type = self._guess_type(full_path)
                    return Response(body=content, content_type=content_type)
        
        # Find route
        handler, params = self._find_route(method, parsed.path)
        
        if not handler:
            return Response(body="Not Found", status=404)
        
        # Create request
        request = Request(
            method=method,
            path=parsed.path,
            query=query,
            headers=headers,
            body=body,
            params=params
        )
        
        # Call handler
        try:
            result = handler(request)
            
            # Convert result to Response
            if isinstance(result, Response):
                return result
            elif isinstance(result, dict) or isinstance(result, list):
                return json_response(result)
            elif isinstance(result, str):
                return html_response(result)
            else:
                return html_response(str(result))
                
        except Exception as e:
            return Response(
                body=json.dumps({"error": str(e)}),
                status=500,
                content_type="application/json"
            )
    
    def _guess_type(self, path: str) -> str:
        """Guess content type from file extension."""
        ext = os.path.splitext(path)[1].lower()
        types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        return types.get(ext, "application/octet-stream")
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, debug: bool = False, reload: bool = False):
        """Start the web server."""
        if reload:
            self._run_with_reload(host, port, debug)
        else:
            self._run_server(host, port, debug)
    
    def _run_with_reload(self, host: str, port: int, debug: bool):
        """Run server with auto-reload on file changes."""
        import subprocess
        import sys
        import time
        
        print(f"   Auto-reload enabled (watching .py files)")
        
        # Get the main script
        main_script = sys.argv[0] if sys.argv[0].endswith('.py') else None
        if not main_script:
            print("   Warning: Could not detect main script, reload disabled")
            self._run_server(host, port, debug)
            return
        
        watch_dir = os.path.dirname(os.path.abspath(main_script)) or "."
        
        def get_mtimes():
            """Get modification times for all .py files."""
            mtimes = {}
            for root, dirs, files in os.walk(watch_dir):
                # Skip hidden dirs and common non-code dirs
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('__pycache__', 'node_modules', '.venv', 'venv')]
                for f in files:
                    if f.endswith('.py'):
                        path = os.path.join(root, f)
                        try:
                            mtimes[path] = os.stat(path).st_mtime
                        except OSError:
                            pass
            return mtimes
        
        last_mtimes = get_mtimes()
        process = None
        
        while True:
            # Start the server process
            env = os.environ.copy()
            env['LUDWIG_NO_RELOAD'] = '1'  # Prevent child from also reloading
            
            process = subprocess.Popen(
                [sys.executable, main_script],
                env=env
            )
            
            # Watch for changes
            while process.poll() is None:
                time.sleep(1)
                current_mtimes = get_mtimes()
                
                changed = False
                for path, mtime in current_mtimes.items():
                    if path not in last_mtimes or last_mtimes[path] != mtime:
                        print(f"\n   Detected change in {os.path.basename(path)}, reloading...")
                        changed = True
                        break
                
                if changed:
                    process.terminate()
                    process.wait()
                    last_mtimes = current_mtimes
                    break
            
            # If process exited without file change, check exit code
            if process.returncode is not None and process.returncode != 0:
                print(f"   Server exited with code {process.returncode}")
                print("   Waiting for file changes to restart...")
                while get_mtimes() == last_mtimes:
                    time.sleep(1)
                last_mtimes = get_mtimes()
    
    def _run_server(self, host: str, port: int, debug: bool):
        """Run the actual HTTP server."""
        web = self
        
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self._handle("GET")
            
            def do_POST(self):
                self._handle("POST")
            
            def do_PUT(self):
                self._handle("PUT")
            
            def do_DELETE(self):
                self._handle("DELETE")
            
            def _handle(self, method: str):
                # Read body
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length) if content_length else None
                
                if body:
                    try:
                        body = json.loads(body)
                    except:
                        body = body.decode("utf-8")
                
                # Get headers
                headers = dict(self.headers)
                
                # Handle request
                response = web._handle_request(method, self.path, headers, body)
                
                # Send response
                self.send_response(response.status)
                self.send_header("Content-Type", response.content_type)
                for key, value in (response.headers or {}).items():
                    self.send_header(key, value)
                self.end_headers()
                
                if response.body:
                    if isinstance(response.body, bytes):
                        self.wfile.write(response.body)
                    else:
                        self.wfile.write(response.body.encode())
            
            def log_message(self, format, *args):
                if debug:
                    print(f"   {args[0]}")
        
        print(f"   Web server at http://{host}:{port}")
        server = HTTPServer((host, port), Handler)
        server.serve_forever()


# Convenience decorators for standalone use
_default_web: Optional[Web] = None


def _get_web() -> Web:
    global _default_web
    if _default_web is None:
        _default_web = Web()
    return _default_web


def route(path: str, methods: list[str] = None):
    """Standalone route decorator."""
    return _get_web().route(path, methods)


def api(path: str):
    """Standalone API route decorator."""
    return _get_web().api(path)

def get(path: str):
    """Standalone GET route decorator."""
    return _get_web().get(path)

