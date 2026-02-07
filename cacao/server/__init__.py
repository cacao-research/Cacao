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

from .signal import Signal, Computed
from .session import Session, SessionManager
from .events import Event, EventRegistry
from .app import App
from .effects import Effect, Watch, effect
from .batch import Batch, batch, batch_updates
from .persist import Persist, PersistManager, MemoryStorage, FileStorage
from .middleware import (
    MiddlewareChain,
    EventContext,
    logging_middleware,
    rate_limit_middleware,
    validation_middleware,
    auth_middleware,
    transform_middleware,
    timeout_middleware,
)

# Fluent UI imports
from . import ui
from . import chart
from . import data

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
]

__version__ = "2.0.0"
