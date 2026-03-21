"""
Ludwig - Simple Python for Web, IoT, and AI

One framework. Web, IoT, AI. Pure Python.
"""

__version__ = "2.0.0"

# Core
from ludwig.core import App, Config

# Web
from ludwig.web import Web, route, api

# IoT
from ludwig.iot import (
    Robot,
    Alarm,
    Sensor,
    Light,
    Motor,
    Camera,
    Home,
    Garden,
    Pin,
)

# AI
from ludwig.ai import Assistant, Vision, Automator

# Database
from ludwig.db import Database, Model

__all__ = [
    # Core
    "App",
    "Config",
    # Web
    "Web",
    "route",
    "api",
    # IoT
    "Robot",
    "Alarm",
    "Sensor",
    "Light",
    "Motor",
    "Camera",
    "Home",
    "Garden",
    "Pin",
    # AI
    "Assistant",
    "Vision",
    "Automator",
    # Database
    "Database",
    "Model",
]
