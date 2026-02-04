"""
Cacao v2 Server - Reactive Python framework with session-scoped state.

Core exports:
    - App: Main application class with routing and event handling
    - Signal: Reactive state primitive with session scoping
    - Computed: Derived state from other signals
    - Session: Per-client session object
"""

from .signal import Signal, Computed
from .session import Session, SessionManager
from .events import Event, EventRegistry
from .app import App

__all__ = [
    "App",
    "Signal",
    "Computed",
    "Session",
    "SessionManager",
    "Event",
    "EventRegistry",
]

__version__ = "2.0.0-dev"
