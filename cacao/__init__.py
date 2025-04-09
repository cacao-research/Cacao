"""
Cacao - A high-performance, reactive web framework for Python
"""

__version__ = "1.0.21"

from .core.app import App
from .core.decorators import mix
from .core import run, run_desktop, State, Component
from .utilities.icons import icon_registry, process_icons_in_component

__all__ = [
    "App",
    "mix",
    "run",
    "run_desktop",
    "State",
    "Component",
    "icon_registry"
]
