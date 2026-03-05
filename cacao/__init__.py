"""
Cacao v2 - Reactive web framework for Python.

Simple API (recommended):
    import cacao as c

    c.config(title="My App")
    c.title("Hello World")
    with c.row():
        c.metric("Users", 100)

Full API (for advanced usage):
    from cacao.server.ui import App, row, metric

    app = App(title="My App")
    with app.page("/"):
        with row():
            metric("Users", 100)
    app.run()
"""

# Import everything from the simple module for easy access
# This uses wildcard import to automatically pick up all exports
from .simple import *

# Also expose the full server module for advanced usage
from . import server

# Keep App accessible at top level for those who want it
from .server.ui import App
from .server.session import Session

# Re-export for explicit access
from .simple import (
    Signal,
    Computed,
)

try:
    from importlib.metadata import version as _get_version
    __version__: str = _get_version("cacao")
except Exception:
    from pathlib import Path as _Path
    __version__ = (_Path(__file__).resolve().parent / "VERSION").read_text().strip() if (_Path(__file__).resolve().parent / "VERSION").exists() else "0.0.0"
