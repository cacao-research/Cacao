"""
Cacao v2 Server - Reactive Python framework with session-scoped state.

Core exports:
    - App: Main application class with routing and event handling
    - Signal: Reactive state primitive with session scoping
    - Computed: Derived state from other signals
    - Session: Per-client session object
    - Effect: Side effects on signal changes
    - Batch: Batch multiple signal updates
    - Persist: Persist signals to storage
    - Middleware: Event middleware system

Fluent UI (Streamlit-like API):
    - ui: Layout and component builders
    - chart: Chart components
    - data: Data loading and manipulation
"""

# Fluent UI imports
from . import agent, chart, data, llm, tukuy_skills, ui
from .app import App
from .batch import Batch, batch, batch_updates
from .effects import Effect, Watch, effect
from .events import Event, EventRegistry
from .middleware import (
    EventContext,
    MiddlewareChain,
    auth_middleware,
    logging_middleware,
    rate_limit_middleware,
    timeout_middleware,
    transform_middleware,
    validation_middleware,
)
from .persist import FileStorage, MemoryStorage, Persist, PersistManager
from .session import Session, SessionManager
from .signal import Computed, Signal

__all__ = [
    # Core
    "App",
    "Signal",
    "Computed",
    "Session",
    "SessionManager",
    "Event",
    "EventRegistry",
    # Effects
    "Effect",
    "Watch",
    "effect",
    # Batch
    "Batch",
    "batch",
    "batch_updates",
    # Persist
    "Persist",
    "PersistManager",
    "MemoryStorage",
    "FileStorage",
    # Middleware
    "MiddlewareChain",
    "EventContext",
    "logging_middleware",
    "rate_limit_middleware",
    "validation_middleware",
    "auth_middleware",
    "transform_middleware",
    "timeout_middleware",
    # Fluent UI
    "ui",
    "chart",
    "data",
    "llm",
    "tukuy_skills",
    "agent",
]

try:
    from importlib.metadata import version as _get_version

    __version__: str = _get_version("cacao")
except Exception:
    from pathlib import Path as _Path

    _vf = _Path(__file__).resolve().parent.parent / "VERSION"
    __version__ = _vf.read_text().strip() if _vf.exists() else "0.0.0"
