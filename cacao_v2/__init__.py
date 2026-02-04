"""
Cacao v2 - Reactive web framework for Python.

A clean-slate rewrite using:
- Python with Signals (reactive state), async events, session isolation
- React + Vite + TypeScript for client rendering
- JSON state sync over WebSocket
"""

from .server import App, Signal, Computed, Session

__all__ = ["App", "Signal", "Computed", "Session"]

__version__ = "2.0.0-dev"
