"""
Core module initialization for the Cacao framework.
"""

from .decorators import mix, page, documented
from .server import CacaoServer
from .state import State, StateChange
from ..ui.components.base import Component, ComponentProps
from .session import SessionManager
from .pwa import PWASupport
from .mixins.logging import LoggingMixin
from .mixins.validation import ValidationMixin
from ..utilities.icons import icon_registry, process_icons_in_component
from .theme import get_theme, set_theme, reset_theme, get_color

# Initialize state
from .decorators import ROUTES, clear_routes, EVENT_HANDLERS, get_event_handlers, register_event_handler, handle_event

def run(host: str = "localhost", port: int = 1634, verbose: bool = False,
        pwa_mode: bool = False, persist_sessions: bool = True,
        session_storage: str = "memory", extensions=None, hot_reload: bool = False):
    """
    Run the Cacao development server.
    
    Args:
        host: Host address to bind the server to
        port: Port number for the HTTP server
        verbose: Enable verbose logging
        pwa_mode: Enable PWA support
        persist_sessions: Enable session persistence
        session_storage: Session storage type ('memory' or 'file')
        extensions: List of extensions to enable (e.g., PWASupport instance)
        hot_reload: Enable hot reloading
    """
    # If extensions list is provided, enable PWA if any PWASupport instance is found
    enable_pwa = pwa_mode
    if extensions and any(isinstance(ext, PWASupport) for ext in extensions):
        enable_pwa = True
    
    server = CacaoServer(
        host=host,
        http_port=port,
        verbose=verbose,
        enable_pwa=enable_pwa,
        persist_sessions=persist_sessions,
        session_storage=session_storage,
        extensions=extensions,
        hot_reload=hot_reload
    )
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {str(e)}")
        raise

import signal
import sys
import inspect
import os.path

def run_desktop(title: str = "Cacao Desktop App", width: int = 800, height: int = 600,
                resizable: bool = True, fullscreen: bool = False, 
                http_port: int = 1634, ws_port: int = 1633, main_file: str = None):
    """Run Cacao as a desktop application.
    
    Args:
        title: Window title
        width: Window width in pixels
        height: Window height in pixels
        resizable: Whether window can be resized
        fullscreen: Whether to start in fullscreen mode
        http_port: Port for HTTP server
        ws_port: Port for WebSocket server
        main_file: Path to main application file (auto-detected if None)
    """
    # Auto-detect the calling file if not provided
    if main_file is None:
        # Get the frame of the caller (who called run_desktop)
        caller_frame = inspect.stack()[1]
        main_file = caller_frame.filename
        
    from ..desktop import CacaoDesktopApp
    app = CacaoDesktopApp(
        title=title, 
        width=width, 
        height=height,
        resizable=resizable, 
        fullscreen=fullscreen,
        http_port=http_port,
        ws_port=ws_port,
        main_file=main_file
    )
    
    # Define signal handler for graceful shutdown
    def signal_handler(sig, frame):
        print("\nDesktop app stopped by user")
        if hasattr(app, 'shutdown'):
            app.shutdown()
        sys.exit(0)
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        app.launch()
    except KeyboardInterrupt:
        print("\nDesktop app stopped by user")
        # Make sure to properly clean up resources
        if hasattr(app, 'shutdown'):
            app.shutdown()
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
    "EVENT_HANDLERS",
    "get_event_handlers",
    "register_event_handler",
    "handle_event",
    "State",
    "StateChange",
    "Component",
    "ComponentProps",
    "SessionManager",
    "PWASupport",
    "LoggingMixin",
    "ValidationMixin",
    "icon_registry",
    "process_icons_in_component",
    "get_theme",
    "set_theme",
    "reset_theme",
    "get_color"
]
