"""Desktop application launcher for Cacao."""

import threading
import time
import sys
import os
from .core.server import CacaoServer

class CacaoDesktopApp:
    def __init__(self, title: str = "Cacao Desktop App", width: int = 800, height: int = 600,
                 resizable: bool = True, fullscreen: bool = False, http_port: int = 1634,
                 ws_port: int = 1633, main_file: str = None, extensions=None):
        self.title = title
        self.width = width
        self.height = height
        self.resizable = resizable
        self.fullscreen = fullscreen
        self.http_port = http_port
        self.ws_port = ws_port
        self.main_file = main_file # Assign main_file
        self.extensions = extensions or []
        
    def start_server(self):
        """Start the Cacao server in a separate thread."""
        # Ensure we have access to the routes before starting server
        from .core.decorators import ROUTES
        
        # Updated to use http_port, ws_port and main_file
        self.server = CacaoServer(
            host="localhost",
            http_port=self.http_port,
            ws_port=self.ws_port,
            enable_pwa=False,
            main_file=self.main_file, # Pass main_file to the server
            extensions=self.extensions # Pass extensions to the server
        )
        
        # Log the available routes for debugging
        route_paths = list(ROUTES.keys())
        print(f"* Available routes: {route_paths}")
        
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
            
        # Import main module first if it's a file path to ensure routes are registered
        if self.main_file and self.main_file.endswith('.py'):
            import importlib.util
            try:
                # Load the module to ensure routes are registered before starting server
                module_name = os.path.basename(self.main_file).replace('.py', '')
                spec = importlib.util.spec_from_file_location(module_name, self.main_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"* Successfully imported main module: {module_name}")
            except Exception as e:
                print(f"* Warning: Error importing main module: {str(e)}")
        
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