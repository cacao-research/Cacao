"""Desktop application launcher for Cacao."""

import threading
import time
import sys
from .core.server import CacaoServer

class CacaoDesktopApp:
    def __init__(self, title: str = "Cacao Desktop App", width: int = 800, height: int = 600, 
                 resizable: bool = True, fullscreen: bool = False, http_port: int = 1634, 
                 ws_port: int = 1633, main_file: str = None): 
        self.title = title
        self.width = width
        self.height = height
        self.resizable = resizable
        self.fullscreen = fullscreen
        self.http_port = http_port
        self.ws_port = ws_port
        self.main_file = main_file # Assign main_file
        
    def start_server(self):
        """Start the Cacao server in a separate thread."""
        # Updated to use http_port, ws_port and main_file
        self.server = CacaoServer(
            host="localhost", 
            http_port=self.http_port,
            ws_port=self.ws_port,
            enable_pwa=False,
            main_file=self.main_file # Pass main_file to the server
        )
        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Wait for server to start
        time.sleep(1.0)
        
    def launch(self):
        """Launch the desktop application."""
        try:
            import webview
        except ImportError:
            print("Error: pywebview is not installed.")
            print("Please install it using: pip install pywebview")
            sys.exit(1)
            
        self.start_server()
        
        # Create a window
        self.window = webview.create_window(
            title=self.title,
            url=f"http://localhost:{self.http_port}",  # Use http_port here
            width=self.width,
            height=self.height,
            resizable=self.resizable,
            fullscreen=self.fullscreen
        )
        
        # Start the WebView event loop
        webview.start()