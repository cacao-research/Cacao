"""
Application module for Cacao framework.
Provides a simplified API for creating web applications.
"""

from typing import Dict, Any, Optional, Callable
from .server import CacaoServer
from .decorators import ROUTES, mix, register_event_handler

# Add a module-level variable to store the ASCII debug setting
ASCII_DEBUG_MODE = False

class App:
    """
    Main application class for Cacao.
    
    Usage:
        app = cacao.App()
        
        @app.mix("/")
        def home():
            return {
                "type": "div",
                "children": ["Welcome!"]
            }
            
        app.brew()
    """
    
    def __init__(self, extensions=None):
        """
        Initialize the Cacao application.
        
        Args:
            extensions: Optional list of extensions to add to the application
        """
        self.server = None
        self.extensions = extensions or []
        
    def mix(self, path: str):
        """
        Decorator for registering page routes.
        Alias for the global mix decorator.
        """
        return mix(path)
        
    def event(self, event_name: str) -> Callable:
        """
        Decorator for registering event handlers.
        
        Args:
            event_name: Name of the event to handle
            
        Returns:
            Callable: Decorator function
            
        Usage:
            @app.event("button_click")
            def handle_click(event_data):
                # Handle the event
                pass
        """
        def decorator(func: Callable) -> Callable:
            register_event_handler(event_name, func)
            return func
        return decorator
        
    def brew(self, type: str = "web", host: str = "localhost", http_port: int = 1634, ws_port: int = 1633,
             title: str = "Cacao App", width: int = 800, height: int = 600,
             resizable: bool = True, fullscreen: bool = False, ASCII_debug: bool = False,
             theme: Dict[str, Any] = None):
        """
        Start the application in web or desktop mode.
        Like brewing a delicious cup of hot chocolate!
        
        Args:
            type: Application type, either "web" or "desktop"
            host: Host address to bind the server to
            http_port: Port number for the HTTP server
            ws_port: Port number for the WebSocket server
            title: Window title (desktop mode only)
            width: Window width in pixels (desktop mode only)
            height: Window height in pixels (desktop mode only)
            resizable: Whether window can be resized (desktop mode only)
            fullscreen: Whether to start in fullscreen mode (desktop mode only)
            ASCII_debug: If True, disables emojis in logs for better compatibility
            theme: Dictionary containing theme properties to apply globally
        """
        # Set the global ASCII debug mode
        global ASCII_DEBUG_MODE
        ASCII_DEBUG_MODE = ASCII_debug
        
        # Set the global theme if provided
        if theme:
            from .theme import set_theme
            set_theme(theme)
        
        import inspect
        
        frame = inspect.currentframe()
        while frame:
            if frame.f_code.co_name == '<module>':
                break
            frame = frame.f_back
            
        if not frame:
            raise RuntimeError("Could not determine main module")
            
        main_file = frame.f_code.co_filename
        
        if type.lower() == "web":
            # Start as web application
            self.server = CacaoServer(
                host=host,
                http_port=http_port,
                ws_port=ws_port,
                main_file=main_file,
                extensions=self.extensions
            )
            self.server.run()
        elif type.lower() == "desktop":
            # Start as desktop application
            from ..desktop import CacaoDesktopApp
            app = CacaoDesktopApp(
                title=title,
                width=width,
                height=height,
                resizable=resizable,
                fullscreen=fullscreen,
                http_port=http_port,
                ws_port=ws_port,
                main_file=main_file,
                extensions=self.extensions
            )
            app.launch()
        else:
            raise ValueError(f"Invalid application type: {type}. Must be 'web' or 'desktop'")
