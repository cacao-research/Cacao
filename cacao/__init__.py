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
# Also expose the full server module for advanced usage
from . import server as server  # noqa: F401
from .server.session import Session as Session  # noqa: F401

# Keep App accessible at top level for those who want it
from .server.ui import App as App  # noqa: F401
from .simple import *  # noqa: F403

# Re-export for explicit access
from .simple import Computed as Computed  # noqa: F401
from .simple import Signal as Signal  # noqa: F401

try:
    from importlib.metadata import version as _get_version

    __version__: str = _get_version("cacao")
except Exception:
    from pathlib import Path as _Path

    __version__ = (
        (_Path(__file__).resolve().parent / "VERSION").read_text().strip()
        if (_Path(__file__).resolve().parent / "VERSION").exists()
        else "0.0.0"
    )


def __getattr__(name: str) -> None:
    """Provide helpful 'Did you mean?' messages for typos in component names."""
    # Skip private/dunder names — let Python raise the default error
    if name.startswith("_"):
        raise AttributeError(f"module 'cacao' has no attribute '{name}'")

    from .server.errors import did_you_mean

    matches = did_you_mean(name)
    if matches:
        suggestions = ", ".join(f"c.{m}()" for m in matches)
        raise AttributeError(
            f"module 'cacao' has no attribute '{name}'. Did you mean: {suggestions}?"
        )
    raise AttributeError(f"module 'cacao' has no attribute '{name}'")
