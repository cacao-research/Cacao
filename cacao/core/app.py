"""
Application module for Cacao framework.
Provides a simplified API for creating web applications.
"""

from typing import Dict, Any, Optional
from .server import CacaoServer
from .decorators import ROUTES, mix

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
    
    def __init__(self):
        self.server = None
        
    def mix(self, path: str):
        """
        Decorator for registering page routes.
        Alias for the global mix decorator.
        """
        return mix(path)
        
    def brew(self, host: str = "localhost", http_port: int = 1634, ws_port: int = 1633):
        """
        Start the application server.
        Like brewing a delicious cup of hot chocolate!
        """
        import inspect
        frame = inspect.currentframe()
        while frame:
            if frame.f_code.co_name == '<module>':
                break
            frame = frame.f_back
            
        if not frame:
            raise RuntimeError("Could not determine main module")
            
        main_file = frame.f_code.co_filename
        
        self.server = CacaoServer(
            host=host,
            http_port=http_port,
            ws_port=ws_port,
            main_file=main_file
        )
        self.server.run()
