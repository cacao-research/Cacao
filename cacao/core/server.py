"""
Server module for the Cacao framework.
Implements two asynchronous servers:
- An HTTP server on port 1634 for front-end requests.
- A WebSocket server on port 1633 for real-time updates.
"""

import asyncio
import json
import os
import sys
import time
import websockets
import watchfiles
import colorama
import importlib
import random
import traceback
from datetime import datetime
from typing import Any, Dict, Callable, Set, Optional
from urllib.parse import parse_qs, urlparse
from .session import SessionManager
from .pwa import PWASupport

# Initialize colorama for Windows support
colorama.init()

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class CacaoServer:
    def __init__(self, host: str = "localhost", http_port: int = 1634, ws_port: int = 1633, 
                 verbose: bool = True, enable_pwa: bool = False, 
                 persist_sessions: bool = True, session_storage: str = "memory"):
        self.host = host
        self.http_port = http_port
        self.ws_port = ws_port
        self.verbose = verbose
        self.enable_pwa = enable_pwa
        
        # Initialize PWA support if enabled
        self.pwa = PWASupport() if enable_pwa else None
        
        # Initialize session management
        self.session_manager = SessionManager(
            storage_type=session_storage,
            persist_on_refresh=persist_sessions
        )
        
        self.websocket_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.file_watcher_task = None
        self.route_cache = {}
        self.last_reload_time = 0
        self.version_counter = 0
        self.active_components = {}
        
        # Server-side state storage with separate states for each component
        self.state = {
            "counter": 0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _print_banner(self):
        banner = f"""
{Colors.YELLOW}
🍫 Starting Cacao Server 🍫
---------------------------
🌐 HTTP Server: http://{self.host}:{self.http_port}
🔌 WebSocket Server: ws://{self.host}:{self.ws_port}
📡 File Watcher: Active
---------------------------{Colors.ENDC}
"""
        print(banner)

    def _log(self, message: str, level: str = "info", emoji: str = ""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {
            "debug": Colors.BLUE,
            "info": Colors.GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED
        }.get(level, Colors.ENDC)
        
        formatted_message = f"{color}{timestamp} {emoji} {message}{Colors.ENDC}"
        print(formatted_message)

    async def _handle_websocket(self, websocket: websockets.WebSocketServerProtocol):
        """Handle WebSocket connections and messages with session support."""
        self._log(f"Client connected", "info", "🌟")
        
        # Create or restore session
        session_id = None
        if hasattr(websocket, "request_headers"):
            cookies = websocket.request_headers.get("cookie", "")
            session_id = self._extract_session_id(cookies)
            
        if not session_id:
            session_id = self.session_manager.create_session()
            
        # Store session ID with websocket
        websocket.session_id = session_id
        self.websocket_clients.add(websocket)
        
        try:
            # Get session state
            session = self.session_manager.get_session(session_id)
            if session and session.get("state"):
                # Restore state from session
                self.state.update(session["state"])
            
            # Send initial state to new client
            await websocket.send(json.dumps({
                "type": "ui_update",
                "force": True,
                "version": self.version_counter,
                "timestamp": time.time(),
                "session_id": session_id
            }))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('action') == 'refresh':
                        self._log("Client requested refresh", "info", "🔄")
                        await self.broadcast(json.dumps({
                            "type": "ui_update", 
                            "force": True,
                            "version": self.version_counter
                        }))
                    
                    # Update session state after any state changes
                    if hasattr(websocket, "session_id"):
                        self.session_manager.update_session_state(
                            websocket.session_id,
                            self.state
                        )
                except Exception as e:
                    self._log(f"Error processing WebSocket message: {str(e)}", "error", "❌")
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self._log(f"WebSocket error: {str(e)}", "error", "❌")
        finally:
            self.websocket_clients.remove(websocket)

    def _extract_session_id(self, cookies: str) -> Optional[str]:
        """Extract session ID from cookies string."""
        if not cookies:
            return None
            
        cookie_pairs = cookies.split(";")
        for pair in cookie_pairs:
            if "=" in pair:
                name, value = pair.strip().split("=", 1)
                if name == "cacao_session":
                    return value
        return None

    async def broadcast(self, message: str) -> None:
        """Broadcast a message to all connected WebSocket clients."""
        if self.websocket_clients:
            try:
                await asyncio.gather(*[
                    client.send(message) 
                    for client in self.websocket_clients
                ])
                self._log(f"Update broadcast sent to {len(self.websocket_clients)} clients", "info", "📢")
            except Exception as e:
                self._log(f"Broadcast error: {str(e)}", "error", "❌")

    def _reload_modules(self):
        """Aggressively reload all relevant modules to ensure fresh code."""
        try:
            # Clear Python's module cache
            if 'main' in sys.modules:
                del sys.modules['main']
            
            # Force reload main module
            importlib.import_module('main')
            self._log("Reloaded main module", "info", "🔄")
            
            # Clear route cache and increment version
            self.route_cache = {}
            self.version_counter += 1
            
            # Clear component cache
            self.active_components = {}
            
        except Exception as e:
            self._log(f"Module reload error: {str(e)}", "error", "❌")
            if self.verbose:
                traceback.print_exc()

    async def _watch_files(self):
        """Watch for file changes and notify clients."""
        self._log("File watcher active", "info", "👀")
        try:
            async for changes in watchfiles.awatch("main.py"):
                current_time = time.time()
                if current_time - self.last_reload_time < 1.0:
                    continue
                
                self.last_reload_time = current_time
                self._log("File changed", "info", "🔄")
                
                # Reload modules
                self._reload_modules()
                
                # Notify clients
                await self.broadcast(json.dumps({
                    "type": "ui_update",
                    "force": True,
                    "version": self.version_counter,
                    "timestamp": time.time()
                }))
                self._log("Hot reload triggered", "info", "🔥")
                
        except Exception as e:
            self._log(f"Watcher error: {str(e)}", "error", "⚠️")
            self.file_watcher_task = asyncio.create_task(self._watch_files())

    async def _handle_http(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle HTTP requests with session and PWA support."""
        try:
            # Set a timeout for reading the request
            try:
                data = await asyncio.wait_for(reader.read(2048), timeout=5.0)
            except asyncio.TimeoutError:
                self._log("Request read timeout", "warning", "⏰")
                writer.write(b"HTTP/1.1 408 Request Timeout\r\n\r\n")
                await writer.drain()
                return
            except Exception as read_err:
                self._log(f"Request read error: {str(read_err)}", "error", "❌")
                writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
                await writer.drain()
                return

            request_text = data.decode("utf-8", errors="ignore")
            lines = request_text.splitlines()
            
            if not lines:
                writer.write(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                await writer.drain()
                return

            request_line = lines[0]
            parts = request_line.split()
            if len(parts) < 2:
                writer.write(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                await writer.drain()
                return

            method, path = parts[0], parts[1]
            
            # Parse query parameters
            query_params = {}
            if '?' in path:
                path_parts = path.split('?', 1)
                path = path_parts[0]
                query_string = path_parts[1]
                parsed_url = urlparse(f"http://dummy.com?{query_string}")
                query_params = parse_qs(parsed_url.query)

            # Parse headers
            headers = {}
            for line in lines[1:]:
                if not line.strip():
                    break
                header_parts = line.split(":", 1)
                if len(header_parts) == 2:
                    headers[header_parts[0].strip().lower()] = header_parts[1].strip()

            # Handle PWA routes if enabled
            if self.enable_pwa:
                if path == "/manifest.json":
                    return await self._serve_manifest(writer)
                elif path == "/service-worker.js":
                    return await self._serve_service_worker(writer)
                elif path == "/offline.html":
                    return await self._serve_offline_page(writer)
            
            # Handle session cookie
            session_id = None
            if "cookie" in headers:
                session_id = self._extract_session_id(headers["cookie"])
                
            if not session_id:
                session_id = self.session_manager.create_session()
            
            # Serve static files
            if path.startswith("/static/"):
                return await self._serve_static_file(path, writer)
            
            # Handle actions via GET request
            if path == "/api/action":
                return await self._handle_action(query_params, writer, session_id)
            
            # Serve UI definition
            if path == "/api/ui":
                return await self._serve_ui_definition(query_params, writer, session_id)
            
            # Serve HTML template
            if "accept" in headers and "text/html" in headers["accept"]:
                return await self._serve_html_template(writer, session_id)

            # Fallback 404
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()

        except Exception as e:
            self._log(f"Unhandled HTTP error: {str(e)}", "error", "💥")
            if self.verbose:
                traceback.print_exc()
            
            # Send generic 500 error
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            await writer.drain()
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    async def _serve_static_file(self, path: str, writer: asyncio.StreamWriter) -> None:
        """Serve static files with proper MIME type detection."""
        static_dir = os.path.join(os.getcwd(), "cacao", "core", "static")
        file_path = os.path.join(static_dir, path[len("/static/"):])
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            
            # Detect MIME type
            mime_types = {
                ".css": "text/css",
                ".js": "application/javascript",
                ".html": "text/html",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png"
            }
            ext = os.path.splitext(file_path)[1]
            content_type = mime_types.get(ext, "application/octet-stream")
            
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
            ).encode("utf-8") + content
            writer.write(response)
            await writer.drain()
        except FileNotFoundError:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()

    async def _handle_action(self, query_params: Dict[str, Any], writer: asyncio.StreamWriter, session_id: str) -> None:
        """Handle actions via GET request with session support."""
        try:
            action = query_params.get('action', [''])[0]
            component_type = query_params.get('component_type', ['unknown'])[0]
            
            self._log(f"Received action: {action} for component type: {component_type}", "info", "🎯")
            
            # Handle different actions based on the component type and action
            if component_type == 'counter' and action == 'increment_counter':
                # Update counter state
                self.state['counter'] += 1
                self._log(f"Incremented counter to: {self.state['counter']}", "info", "🔢")
            elif component_type == 'timer' and action == 'update_timestamp':
                # Update timestamp state
                self.state['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._log(f"Updated timestamp to: {self.state['timestamp']}", "info", "🕒")
            else:
                self._log(f"Unknown action or component type: {action} / {component_type}", "warning", "⚠️")
            
            # Update session state after action
            if session_id:
                self.session_manager.update_session_state(session_id, self.state)
            
            # Send success response
            response_data = json.dumps({
                "success": True,
                "action": action,
                "component_type": component_type,
                "state": self.state
            })
            
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                f"Set-Cookie: cacao_session={session_id}; Path=/; HttpOnly; SameSite=Strict\r\n"
                f"Content-Length: {len(response_data)}\r\n"
                "\r\n"
                f"{response_data}"
            )
            writer.write(response.encode())
            await writer.drain()
            
            # Trigger UI refresh
            await self.broadcast(json.dumps({
                "type": "ui_update",
                "force": True,
                "version": self.version_counter,
                "timestamp": time.time()
            }))
        except Exception as e:
            self._log(f"Action error: {str(e)}", "error", "❌")
            error_response = json.dumps({"error": str(e)})
            response = (
                "HTTP/1.1 500 Internal Server Error\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(error_response)}\r\n"
                "\r\n"
                f"{error_response}"
            )
            writer.write(response.encode())
            await writer.drain()

    async def _serve_ui_definition(self, query_params: Dict[str, Any], writer: asyncio.StreamWriter, session_id: str) -> None:
        """Serve the UI definition with version tracking."""
        try:
            # Force reload if requested
            if 'force' in query_params:
                self._reload_modules()
            
            # Get fresh UI data
            from main import home, Counter, Timer
            
            # Make server state available to the home function
            # This is a hack to pass state to the component
            sys.modules['main']._state = self.state
            
            # Call home function to get UI definition
            result = home()
            
            # Add metadata
            if isinstance(result, dict):
                result['_v'] = self.version_counter
                result['_t'] = int(time.time() * 1000)
                result['_r'] = random.randint(1, 1000000)
            
            # Process children to inject state based on component type
            if isinstance(result, dict) and 'children' in result and isinstance(result['children'], list):
                for i, child in enumerate(result['children']):
                    if isinstance(child, dict) and 'component_type' in child:
                        # Handle different component types
                        if child['component_type'] == 'counter':
                            # This is a counter component, update it with state
                            counter = Counter()
                            result['children'][i] = counter.render(self.state)
                        elif child['component_type'] == 'timer':
                            # This is a timer component, update it with state
                            timer = Timer()
                            result['children'][i] = timer.render(self.state)
            
            json_body = json.dumps(result)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json; charset=utf-8\r\n"
                "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                "Pragma: no-cache\r\n"
                "Expires: 0\r\n"
                f"Set-Cookie: cacao_session={session_id}; Path=/; HttpOnly; SameSite=Strict\r\n"
                f"Content-Length: {len(json_body)}\r\n"
                "\r\n"
                f"{json_body}"
            )
            writer.write(response.encode("utf-8"))
            await writer.drain()
        except Exception as e:
            response = (
                "HTTP/1.1 500 Internal Server Error\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n\r\n"
                f"{str(e)}"
            )
            writer.write(response.encode("utf-8"))
            self._log(f"UI error: {str(e)}", "error", "❌")
            await writer.drain()

    async def _serve_html_template(self, writer: asyncio.StreamWriter, session_id: str) -> None:
        """Serve the main HTML template with PWA and session support."""
        index_path = os.path.join(os.getcwd(), "cacao", "core", "static", "index.html")
        try:
            with open(index_path, "r") as f:
                content = f.read()
                
            # Add PWA meta tags if enabled
            if self.enable_pwa:
                pwa_meta = """
                    <link rel="manifest" href="/manifest.json">
                    <meta name="theme-color" content="#6B4226">
                    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">
                """
                content = content.replace("</head>", f"{pwa_meta}</head>")
                
                # Add service worker registration
                sw_script = """
                    <script>
                        if ('serviceWorker' in navigator) {
                            navigator.serviceWorker.register('/service-worker.js')
                                .then(registration => console.log('ServiceWorker registered'))
                                .catch(err => console.error('ServiceWorker registration failed:', err));
                        }
                    </script>
                """
                content = content.replace("</body>", f"{sw_script}</body>")
            
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/html\r\n"
                f"Set-Cookie: cacao_session={session_id}; Path=/; HttpOnly; SameSite=Strict\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
                f"{content}"
            )
            writer.write(response.encode())
            await writer.drain()
        except FileNotFoundError:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()

    async def _serve_manifest(self, writer: asyncio.StreamWriter) -> None:
        """Serve the PWA manifest.json file."""
        if not self.pwa:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()
            return
            
        manifest = self.pwa.generate_manifest()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(manifest)}\r\n"
            "\r\n"
            f"{manifest}"
        )
        writer.write(response.encode())
        await writer.drain()

    async def _serve_service_worker(self, writer: asyncio.StreamWriter) -> None:
        """Serve the PWA service worker script."""
        if not self.pwa:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()
            return
            
        sw_code = self.pwa.generate_service_worker()
        if not sw_code:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()
            return
            
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/javascript\r\n"
            f"Content-Length: {len(sw_code)}\r\n"
            "\r\n"
            f"{sw_code}"
        )
        writer.write(response.encode())
        await writer.drain()

    async def _serve_offline_page(self, writer: asyncio.StreamWriter) -> None:
        """Serve the offline fallback page."""
        offline_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Offline - Cacao App</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding: 40px; }
                h1 { color: #6B4226; }
            </style>
        </head>
        <body>
            <h1>You are offline</h1>
            <p>Please check your internet connection to continue using this application.</p>
        </body>
        </html>
        """
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(offline_html)}\r\n"
            "\r\n"
            f"{offline_html}"
        )
        writer.write(response.encode())
        await writer.drain()

    async def _run_servers(self):
        """Start and run all server components."""
        self._print_banner()
        
        # Start WebSocket server
        ws_server = await websockets.serve(
            self._handle_websocket,
            self.host,
            self.ws_port
        )
        self._log("WebSocket server ready", "info", "🔌")
        
        # Start HTTP server
        http_server = await asyncio.start_server(
            self._handle_http,
            self.host,
            self.http_port
        )
        self._log("HTTP server ready", "info", "🌐")
        
        # Start file watcher
        self.file_watcher_task = asyncio.create_task(self._watch_files())
        
        try:
            await asyncio.gather(
                ws_server.wait_closed(),
                http_server.serve_forever(),
                self.file_watcher_task
            )
        except KeyboardInterrupt:
            self._log("Shutting down...", "info", "👋")
        except Exception as e:
            self._log(f"Server error: {str(e)}", "error", "❌")

    def run(self, verbose: bool = False) -> None:
        """Run the Cacao server."""
        self.verbose = verbose
        try:
            asyncio.run(self._run_servers())
        except KeyboardInterrupt:
            self._log("Server stopped", "info", "👋")
        except Exception as e:
            self._log(f"Fatal error: {str(e)}", "error", "💥")
