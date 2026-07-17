"""
Tests for Ludwig core module
"""

import pytest
from ludwig import App
from ludwig.core import Config


class TestApp:
    """Test App class."""
    
    def test_app_creation(self):
        """Test creating an App instance."""
        app = App()
        assert app is not None
    
    def test_app_with_name(self):
        """Test App with custom name."""
        app = App(name="Test App")
        assert app.config.name == "Test App"
    
    def test_route_registration(self):
        """Test registering routes."""
        app = App()
        
        @app.get("/test")
        def handler(req):
            return "ok"
        
        assert "/test" in app._routes or len(app._routes) > 0
    
    def test_multiple_methods(self):
        """Test different HTTP methods."""
        app = App()
        
        @app.get("/resource")
        def get_handler(req):
            return {"method": "GET"}
        
        @app.post("/resource")
        def post_handler(req):
            return {"method": "POST"}
        
        @app.put("/resource/:id")
        def put_handler(req):
            return {"method": "PUT"}
        
        @app.delete("/resource/:id")
        def delete_handler(req):
            return {"method": "DELETE"}
        
        # Routes should be registered
        assert len(app._routes) >= 4


class TestConfig:
    """Test Config class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = Config()
        assert config.host == "0.0.0.0"
        assert config.port == 8000
        assert config.debug is False
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = Config(
            name="Custom",
            host="127.0.0.1",
            port=3000,
            debug=True,
        )
        assert config.name == "Custom"
        assert config.host == "127.0.0.1"
        assert config.port == 3000
        assert config.debug is True
