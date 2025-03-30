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
import watchfiles
import importlib
import random
import traceback
from datetime import datetime
from typing import Any, Dict, Callable, Set, Optional
from urllib.parse import parse_qs, urlparse
from .session import SessionManager
from .pwa import PWASupport
from .mixins.logging import LoggingMixin, Colors

from .. import __version__

# Using standard websockets import for version 15.0.1
import websockets
from websockets.server import serve

class CacaoServer(LoggingMixin):
    def __init__(self, host: str = "localhost", http_port: int = 1634, ws_port: int = 1633,
                 verbose: bool = True, enable_pwa: bool = False,
                 persist_sessions: bool = True, session_storage: str = "memory",
                 main_file: Optional[str] = None, extensions=None, hot_reload: bool = False) -> None:
        self.host = host
        self.http_port = http_port
        self.ws_port = ws_port
        self.verbose = verbose
        self.enable_pwa = enable_pwa
        self.hot_reload = hot_reload
        self.extensions = extensions or []
                    
        self._actual_module_name = None

        # Get the name of the calling module if main_file is not specified
        if main_file is None:
            import inspect
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            self.main_module = module.__name__ if module else "main"
        else:
            # If it's a file path, store as is
            if os.path.isfile(main_file):
                self.main_module = main_file
            # Otherwise, remove .py extension if present
            else:
                self.main_module = main_file[:-3] if main_file.endswith('.py') else main_file
            
        # Initialize PWA support if enabled or if there's a PWASupport in extensions
        self.pwa = None
        if enable_pwa:
            self.pwa = PWASupport()
        else:
            # Check if there's a PWASupport instance in extensions
            for ext in self.extensions:
                if isinstance(ext, PWASupport):
                    self.pwa = ext
                    self.enable_pwa = True
                    break
        
        # Initialize session management
        self.session_manager = SessionManager(
            storage_type=session_storage,
            persist_on_refresh=persist_sessions
        )
        
        self.websocket_clients: Set = set()  # Remove type annotation to avoid reference issue
        self.file_watcher_task = None
        self.route_cache = {}
        self.last_reload_time = 0
        self.version_counter = 0
        self.active_components = {}
        
        # Server-side state storage with separate states for each component
        self.state = {
            "counter": 0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_page": "home"  # Default page
        }

    def _print_banner(self):
        """Print server banner with ASCII characters instead of emojis for Windows compatibility."""
        banner = f"""
{Colors.YELLOW}
C  Starting Cacao Server v{__version__}  C

---------------------------
W HTTP Server: http://{self.host}:{self.http_port}
* WebSocket Server: ws://{self.host}:{self.ws_port}
* File Watcher: Active
---------------------------{Colors.ENDC}
"""
        print(banner)

    async def _handle_websocket(self, websocket):
        """Handle WebSocket connections and messages with session support."""
        self.log(f"Client connected", "info", "🌟")
        
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
                "session_id": session_id,
                "state": self.state  # Include current state
            }))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('action') == 'refresh':
                        self.log("Client requested refresh", "info", "🔄")
                        await self.broadcast(json.dumps({
                            "type": "ui_update", 
                            "force": True,
                            "version": self.version_counter,
                            "state": self.state  # Include current state
                        }))
                    elif data.get('action') == 'sync_state':
                        # Handle state sync request
                        new_state = data.get('state', {})
                        self.state.update(new_state)
                        self.log(f"State synced from client: {new_state}", "info", "🔄")
                        
                        # Update session state
                        if hasattr(websocket, "session_id"):
                            self.session_manager.update_session_state(
                                websocket.session_id,
                                self.state
                            )
                        
                        # Broadcast state update
                        await self.broadcast(json.dumps({
                            "type": "ui_update",
                            "force": True,
                            "version": self.version_counter,
                            "state": self.state
                        }))
                    
                    # Update session state after any state changes
                    if hasattr(websocket, "session_id"):
                        self.session_manager.update_session_state(
                            websocket.session_id,
                            self.state
                        )
                except Exception as e:
                    self.log(f"Error processing WebSocket message: {str(e)}", "error", "❌")
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self.log(f"WebSocket error: {str(e)}", "error", "❌")
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
                self.log(f"Update broadcast sent to {len(self.websocket_clients)} clients", "info", "📢")
            except Exception as e:
                self.log(f"Broadcast error: {str(e)}", "error", "❌")

    def _reload_modules(self) -> None:
        """Aggressively reload all relevant modules to ensure fresh code."""
        try:
            # Check if main_module is a file path
            if os.path.isfile(self.main_module) or os.path.isabs(self.main_module):
                # Load the module from file
                import importlib.util
                import sys
                
                # Get the module name from file path
                module_name = os.path.splitext(os.path.basename(self.main_module))[0]
                
                # Create spec and load module
                spec = importlib.util.spec_from_file_location(module_name, self.main_module)
                if spec is None:
                    raise ImportError(f"Could not load spec for module {module_name} from {self.main_module}")
                    
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                # Store the module name for future reference
                self._actual_module_name = module_name
                
                self.log(f"Loaded module {module_name} from {self.main_module}", "info", "📂")
            else:
                # Clear Python's module cache
                if self.main_module in sys.modules:
                    del sys.modules[self.main_module]
                
                # Force reload main module
                importlib.import_module(self.main_module)
                self._actual_module_name = self.main_module
                
                self.log(f"Reloaded {self.main_module} module", "info", "🔄")
        
            # Clear route cache and increment version
            self.route_cache = {}
            self.version_counter += 1
            
            # Clear component cache
            self.active_components = {}
            
        except Exception as e:
            self.log(f"Module reload error: {str(e)}", "error", "❌")
            if self.verbose:
                traceback.print_exc()

    async def _watch_files(self) -> None:
        """Watch for file changes and notify clients."""
        self.log("File watcher active", "info", "👀")
        try:
            # Determine the actual file path to watch
            file_to_watch = None
            
            # If main_file is an absolute path, use it directly
            if self.main_module and os.path.isabs(self.main_module):
                file_to_watch = self.main_module
            # If main_module is a Python file path without .py, add the extension
            elif not self.main_module.endswith('.py') and os.path.isfile(f"{self.main_module}.py"):
                file_to_watch = f"{self.main_module}.py"
            # If it's already a valid file path, use it as is
            elif os.path.isfile(self.main_module):
                file_to_watch = self.main_module
            # Fallback to __main__ module
            else:
                # Try to use __main__ module's file as fallback
                if hasattr(sys.modules['__main__'], '__file__'):
                    file_to_watch = sys.modules['__main__'].__file__
                    self.log(f"Using __main__ module file: {file_to_watch}", "info", "🔄")
        
            # Final validation
            if not file_to_watch or not os.path.isfile(file_to_watch):
                self.log(f"Warning: Cannot find valid file to watch. Tried: {self.main_module}", "warning", "⚠️")
                return
            
            self.log(f"Watching file: {file_to_watch}", "info", "👀")
            
            # Watch the file for changes
            async for changes in watchfiles.awatch(file_to_watch):
                current_time = time.time()
                if current_time - self.last_reload_time < 1.0:
                    continue
                
                self.last_reload_time = current_time
                self.log("File changed", "info", "🔄")
                
                # Reload modules
                self._reload_modules()
                
                # Notify clients
                await self.broadcast(json.dumps({
                    "type": "ui_update",
                    "force": True,
                    "version": self.version_counter,
                    "timestamp": time.time(),
                    "state": self.state  # Include current state
                }))
                self.log("Hot reload triggered", "info", "🔥")
                
        except Exception as e:
            self.log(f"Watcher error: {str(e)}", "error", "⚠️")
            # Wait a bit before retrying to avoid rapid failure loops
            await asyncio.sleep(2.0)
            self.file_watcher_task = asyncio.create_task(self._watch_files())

    async def _handle_http(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle HTTP requests with session and PWA support."""
        try:
            # Set a longer timeout for reading the request
            try:
                data = await asyncio.wait_for(reader.read(8192), timeout=30.0)  # Increased buffer and timeout
            except asyncio.TimeoutError:
                self.log("Request read timeout", "warning", "⏰")
                writer.write(b"HTTP/1.1 408 Request Timeout\r\n\r\n")
                await writer.drain()
                return
            except Exception as read_err:
                self.log(f"Request read error: {str(read_err)}", "error", "❌")
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
                
            # Handle refresh requests (missing endpoint that was causing 404)
            if path == "/api/refresh":
                return await self._handle_refresh(query_params, writer, session_id)
            
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
            self.log(f"Unhandled HTTP error: {str(e)}", "error", "💥")
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
            
            self.log(f"Received action: {action} for component type: {component_type}", "info", "🎯")
            
            # First try to handle the action using registered event handlers
            from .decorators import EVENT_HANDLERS, handle_event
            
            if action in EVENT_HANDLERS:
                # We have a registered handler for this action
                self.log(f"Found registered handler for action: {action}", "info", "🎯")
                
                # Prepare event data
                event_data = {
                    "action": action,
                    "component_type": component_type,
                    "params": {},
                    "value": query_params.get('value', [''])[0]
                }
                
                # Add any other query params to the event data
                for key, value in query_params.items():
                    if key not in ['action', 'component_type', 't']:
                        event_data["params"][key] = value[0] if isinstance(value, list) else value
                
                # Call the registered event handler
                try:
                    await handle_event(action, event_data)
                    self.log(f"Successfully handled event: {action}", "info", "✅")
                except Exception as e:
                    self.log(f"Error handling event: {action} - {str(e)}", "error", "❌")
                    traceback.print_exc()
            # If no registered handler or handler fails, fall back to built-in actions
            elif component_type == 'counter' and action == 'increment_counter':
                # Update counter state
                self.state['counter'] += 1
                self.log(f"Incremented counter to: {self.state['counter']}", "info", "🔢")
            elif component_type == 'timer' and action == 'update_timestamp':
                # Update timestamp state
                self.state['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.log(f"Updated timestamp to: {self.state['timestamp']}", "info", "🕒")
            elif action == 'set_state':
                # Handle generic state setting
                state_name = component_type
                state_value = query_params.get('value', [''])[0]
                
                # Special handling for toggle
                if state_value == 'toggle':
                    current_value = self.state.get(state_name, False)
                    state_value = not current_value
                
                # Convert state value if needed
                if isinstance(state_value, str) and state_value.lower() in ['true', 'false']:
                    state_value = state_value.lower() == 'true'
                
                # Update state
                self.state[state_name] = state_value
                self.log(f"Updated state '{state_name}' to: {state_value}", "info", "🔄")
                
                # Update global state manager
                try:
                    from .state import global_state
                    global_state.update_from_server(self.state)
                except ImportError:
                    pass
            else:
                self.log(f"Unknown action or component type: {action} / {component_type}", "warning", "⚠️")
            
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
                "timestamp": time.time(),
                "state": self.state  # Include current state
            }))
        except Exception as e:
            self.log(f"Action error: {str(e)}", "error", "❌")
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
        
            # Get the module name to use
            module_name = os.path.splitext(os.path.basename(self.main_module))[0]
        
            # Get fresh UI data from the module
            if os.path.isfile(self.main_module):
                # For file paths, use importlib.util to load the module
                import importlib.util
                spec = importlib.util.spec_from_file_location(module_name, self.main_module)
                if spec is None:
                    raise ImportError(f"Could not create spec for module {module_name}")
                
                main_module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = main_module
                spec.loader.exec_module(main_module)
            else:
                # For module names, use importlib
                main_module = importlib.import_module(module_name)
        
            # Make server state available to the main module
            setattr(main_module, '_state', self.state)
        
            # Get the routes from the decorators module
            from .decorators import ROUTES
            
            # Get the route handler for the current path
            path = query_params.get('path', ['/'])[0]
            handler = ROUTES.get(path)
            
            if not handler:
                raise ValueError(f"No route handler found for path: {path}")
            
            # Check if _hash parameter is present in query params
            hash_param = query_params.get('_hash', [''])[0]
            if hash_param and hash_param != self.state.get('current_page', ''):
                # Update the current_page state based on hash
                self.state['current_page'] = hash_param
                self.log(f"Updated state 'current_page' to: {hash_param} from URL hash", "info", "🔄")

            # Call the handler to get UI definition
            result = handler()
            
            # Add metadata
            if isinstance(result, dict):
                result['_v'] = self.version_counter
                result['_t'] = int(time.time() * 1000)
                result['_r'] = random.randint(1, 1000000)
                result['_state'] = self.state  # Include current state
            
            # Update session state after UI generation
            if session_id:
                self.session_manager.update_session_state(session_id, self.state)
            
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
            self.log(f"UI error: {str(e)}", "error", "❌")
            await writer.drain()

    async def _serve_html_template(self, writer: asyncio.StreamWriter, session_id: str) -> None:
        """Serve the main HTML template with PWA and session support."""
        index_path = os.path.join(os.getcwd(), "cacao", "core", "static", "index.html")
        try:
            with open(index_path, "r") as f:
                content = f.read()
                
            # Add WebSocket port as a query parameter to the HTML
            content = content.replace('</head>', f'<meta name="ws-port" content="{self.ws_port}">\n</head>')
            
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

    async def _run_servers(self):
        """Start and run all server components."""
        self._print_banner()
        
        # Start WebSocket server using the newer API
        ws_server = await serve(
            self._handle_websocket,
            self.host,
            self.ws_port
        )
        self.log("WebSocket server ready", "info", "🔌")
        
        # Start HTTP server
        http_server = await asyncio.start_server(
            self._handle_http,
            self.host,
            self.http_port
        )
        self.log("HTTP server ready", "info", "🌐")
        
        # Start file watcher
        self.file_watcher_task = asyncio.create_task(self._watch_files())
        
        try:
            await asyncio.gather(
                ws_server.wait_closed(),
                http_server.serve_forever(),
                self.file_watcher_task
            )
        except KeyboardInterrupt:
            self.log("Shutting down...", "info", "👋")
        except Exception as e:
            self.log(f"Server error: {str(e)}", "error", "❌")

    def run(self, verbose: bool = False) -> None:
        """Run the Cacao server."""
        self.verbose = verbose
        try:
            asyncio.run(self._run_servers())
        except KeyboardInterrupt:
            self.log("Server stopped", "info", "👋")
        except Exception as e:
            self.log(f"Fatal error: {str(e)}", "error", "💥")

    async def _handle_refresh(self, query_params: Dict[str, Any], writer: asyncio.StreamWriter, session_id: str) -> None:
        """Handle refresh requests that trigger UI updates."""
        try:
            self.log("Refresh request received", "info", "🔄")
            
            # Check if a hash parameter is provided
            hash_param = query_params.get('_hash', [''])[0]
            if hash_param and hash_param != self.state.get('current_page', ''):
                # Update the current_page state based on hash
                self.state['current_page'] = hash_param
                self.log(f"Updated state 'current_page' to: {hash_param} from refresh request", "info", "🔄")
                
                # Update global state manager
                try:
                    from .state import global_state
                    global_state.update_from_server(self.state)
                except ImportError:
                    pass
                    
                # Update session state
                if session_id:
                    self.session_manager.update_session_state(session_id, self.state)
            
            # Send success response
            response_data = json.dumps({
                "success": True,
                "refresh": True,
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
            
            # Trigger UI refresh via WebSocket
            await self.broadcast(json.dumps({
                "type": "ui_update",
                "force": True,
                "version": self.version_counter,
                "timestamp": time.time(),
                "state": self.state  # Include current state
            }))
        except Exception as e:
            self.log(f"Refresh error: {str(e)}", "error", "❌")
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
