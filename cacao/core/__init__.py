"""
Core module initialization for the Cacao framework.
"""

from .decorators import mix, page, documented
from .server import CacaoServer
from .state import State, StateChange
from ..ui.components.base import Component, ComponentProps
from .session import SessionManager  # New import
from .pwa import PWASupport  # New import
from ..desktop import CacaoDesktopApp  # New import

# Initialize state
from .decorators import ROUTES, clear_routes

def run(verbose: bool = False, pwa_mode: bool = False, 
        persist_sessions: bool = True, session_storage: str = "memory"):
    """Run the Cacao development server."""
    server = CacaoServer(verbose=verbose, enable_pwa=pwa_mode, 
                         persist_sessions=persist_sessions,
                         session_storage=session_storage)
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {str(e)}")
        raise

def run_desktop(title: str = "Cacao Desktop App", width: int = 800, height: int = 600,
                resizable: bool = True, fullscreen: bool = False, 
                http_port: int = 1634, ws_port: int = 1633):
    """Run Cacao as a desktop application."""
    app = CacaoDesktopApp(
        title=title, 
        width=width, 
        height=height,
        resizable=resizable, 
        fullscreen=fullscreen,
        http_port=http_port,
        ws_port=ws_port
    )
    try:
        app.launch()
    except Exception as e:
        print(f"Error launching desktop app: {str(e)}")
        raise

__all__ = [
    "mix",
    "page",
    "documented",
    "run",
    "run_desktop",
    "CacaoServer",
    "ROUTES",
    "clear_routes",
    "State",
    "StateChange",
    "Component",
    "ComponentProps",
    "SessionManager",
    "PWASupport"
]
