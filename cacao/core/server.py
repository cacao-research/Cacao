"""
Server module for the Cacao framework.
Implements two asynchronous servers:
- An HTTP server on port 1634 for front-end requests.
- A WebSocket server on port 1633 for real-time updates.
"""

# Global server instance
global_server = None

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
from ..utilities.icons import icon_registry

from .. import __version__

# Using standard websockets import for version 15.0.1
import websockets
from websockets.server import serve

class CacaoServer(LoggingMixin):
    # Class variable to store the current server instance
    _instance = None
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
        """Print server banner with proper emoji handling based on ASCII_DEBUG_MODE."""
        # Title line with chocolate bar emojis
        self.log(f"Starting Cacao Server v{__version__}", "warning", "🍫")
        
        # Print divider
        print(f"{Colors.YELLOW}---------------------------{Colors.ENDC}")
        
        # Server information
        self.log(f"HTTP Server: http://{self.host}:{self.http_port}", "warning", "🌎")
        self.log(f"WebSocket Server: ws://{self.host}:{self.ws_port}", "warning", "🌎")
        
        # Print divider
        print(f"{Colors.YELLOW}---------------------------{Colors.ENDC}")

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
            # If there's session state, send it to the client
            if session_id:
                state = self.session_manager.get_session_state(session_id)
                if state:
                    self.state.update(state)
                    await websocket.send(json.dumps({
                        "type": "state_sync",
                        "state": self.state
                    }))
            
            # Main message loop
            async for message in websocket:
                try:
                    data = json.loads(message)
                    event_type = data.get('type', '')
                    event_name = data.get('event', '')
                    event_data = data.get('data', {})
                    component_id = data.get('component_id', None)
                    
                    if event_type == 'event':
                        # Handle events via decorator
                        from .decorators import handle_event
                        from .state import global_state
                        result = handle_event(event_name, event_data)
                        
                        # If event returned a value, update both server and global state
                        if result is not None and isinstance(result, dict):
                            # Update server state
                            self.state.update(result)
                            
                            # Update global state manager
                            global_state.update_from_server(self.state)
                            
                            # Update session state
                            if session_id:
                                self.session_manager.update_session_state(session_id, self.state)
                            
                            # Send event result
                            await websocket.send(json.dumps({
                                "type": "event_result",
                                "event": event_name,
                                "result": result
                            }))
                            
                            # Broadcast state update to all clients
                            await self.broadcast(json.dumps({
                                "type": "state_sync",
                                "state": self.state,
                                "timestamp": time.time()
                            }))
                        
                    elif event_type == 'ping':
                        # Send pong response
                        await websocket.send(json.dumps({
                            "type": "pong",
                            "timestamp": time.time()
                        }))
                        
                    elif event_type in ['state_update', 'component_updated']:
                        # State update from client
                        component_state = data.get('state', {})
                        if component_id and component_state:
                            # Add logging to track component updates
                            print(f"Updating component {component_id} with state: {component_state}")
                            print(f"Session ID: {session_id}, WebSocket ID: {id(websocket)}")
                            self.active_components[component_id] = component_state
                        
                        # Update global state
                        for state_name, state_value in component_state.items():
                            self.state[state_name] = state_value
                        
                        # Update session state
                        if session_id:
                            self.session_manager.update_session_state(session_id, self.state)
                        
                        # Broadcast state update to all clients
                        await self.broadcast(json.dumps({
                            "type": "state_update",
                            "state": component_state,
                            "timestamp": time.time()
                        }))
                            
                    else:
                        self.log(f"Unknown event type: {event_type}", "warning", "⚠️")
                        
                except json.JSONDecodeError:
                    self.log("Received invalid JSON", "error", "❌")
                except Exception as e:
                    self.log(f"Error handling message: {str(e)}", "error", "❌")
                    if self.verbose:
                        traceback.print_exc()
        
        except websockets.exceptions.ConnectionClosed:
            self.log("Client disconnected normally", "info", "💤")
        except Exception as e:
            self.log(f"Client connection error: {str(e)}", "error", "⚡")
        finally:
            # Clean up client from active set
            self.websocket_clients.discard(websocket)
            
    def _extract_session_id(self, cookies: str) -> Optional[str]:
        """Extract session ID from cookies string."""
        if not cookies:
            return None
            
        cookie_parts = cookies.split(';')
        for part in cookie_parts:
            if '=' in part:
                name, value = part.strip().split('=', 1)
                if name == 'cacao_session':
                    return value
                    
        return None
                
    async def broadcast(self, message: str) -> None:
        """Broadcast a message to all connected WebSocket clients."""
        if not self.websocket_clients:
            return
            
        disconnected = set()
        
        for websocket in self.websocket_clients:
            try:
                await websocket.send(message)
            except (websockets.exceptions.ConnectionClosed, ConnectionResetError):
                disconnected.add(websocket)
            except Exception as e:
                self.log(f"Error broadcasting to client: {str(e)}", "error", "❌")
                disconnected.add(websocket)
                
        # Remove disconnected clients
        self.websocket_clients.difference_update(disconnected)
    
    @classmethod
    async def broadcast_state_update(cls, state_name: str, state_value: Any) -> None:
        """
        Broadcast a state update to all connected WebSocket clients.
        
        Args:
            state_name: Name of the state being updated
            state_value: New value of the state
        """
        if not cls._instance:
            return
            
        try:
            # Update server-side state
            cls._instance.state[state_name] = state_value
            
            # Broadcast state update
            await self.broadcast(json.dumps({
                "type": "state_update",
                "state_name": state_name,
                "state_value": state_value,
                "timestamp": time.time()
            }))
            
            self.log(f"Broadcasted state update: {state_name} = {state_value}", "info", "🔄")
        except Exception as e:
            self.log(f"Error broadcasting state update: {str(e)}", "error", "❌")
    
    def _reload_modules(self) -> None:
        """Reload modules to pick up changes."""
        try:
            self.version_counter += 1
            
            # If main_module is a file path, import it directly
            if os.path.isfile(self.main_module):
                module_name = os.path.basename(self.main_module).replace('.py', '')
                if not self._actual_module_name:
                    self._actual_module_name = module_name
                
                # Import the module using spec from file
                import importlib.util
                spec = importlib.util.spec_from_file_location(module_name, self.main_module)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    sys.modules[module_name] = module
                    
                    # Clear routes and reload
                    from .decorators import clear_routes
                    clear_routes()
                    
                    # Reload the module
                    importlib.reload(module)
                    
                    self.log(f"Reloaded module: {module_name}", "info", "🔄")
            else:
                # Dynamically reload the original calling module
                if self.main_module in sys.modules:
                    importlib.reload(sys.modules[self.main_module])
                    self.log(f"Reloaded module: {self.main_module}", "info", "🔄")
                else:
                    self.log(f"Module not found: {self.main_module}", "warning", "⚠️")
            
            # Clear component cache
            self.active_components = {}
            
        except Exception as e:
            self.log(f"Module reload error: {str(e)}", "error", "❌")
            if self.verbose:
                traceback.print_exc()

    async def _watch_files(self) -> None:
        """Watch for file changes and notify clients."""
        self.log("File watcher active", "info", "📂")
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
            
            # Log the path for debugging
            self.log(f"Received request for path: {path}", "info", "📤")
            
            # Handle root path explicitly - redirect to HTML template
            if path == "/" or path == "":
                self.log("Handling root path request", "info", "📤")
                return await self._serve_html_template(writer, session_id)
                
            # Handle actions via GET request
            if path == "/api/action":
                return await self._handle_action(query_params, writer, session_id)
                
            # Handle refresh requests
            if path == "/api/refresh":
                return await self._handle_refresh(query_params, writer, session_id)
            
            # Serve UI definition
            if path == "/api/ui":
                return await self._serve_ui_definition(query_params, writer, session_id)

            # Handle event requests
            elif path == "/api/event":
                return await self._handle_event(query_params, writer, session_id)
            
            # Serve HTML template for other paths with HTML accept header
            if "accept" in headers and "text/html" in headers["accept"]:
                return await self._serve_html_template(writer, session_id)

            # Fallback 404
            self.log(f"No handler for path: {path}", "warning", "!")
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
        self.log(f"Serving static file: {path}", "info", "📄")
        
        # Get cacao package base dir
        cacao_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Try multiple static paths, similar to HTML template
        static_dirs = [
            os.path.join(cacao_base_dir, "core", "static"),
            os.path.join(os.path.dirname(__file__), "static"),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
        ]
        
        content = None
        for static_dir in static_dirs:
            file_path = os.path.join(static_dir, path[len("/static/"):])
            self.log(f"Trying to load static file from: {file_path}", "info", "📁")
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                    self.log(f"Successfully loaded static file from: {file_path}", "info", "✅")
                    break
            except FileNotFoundError:
                continue
                
        if content is None:
            self.log(f"Static file not found: {path}", "error", "❌")
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()
            return
            
        try:
            # Detect MIME type
            mime_types = {
                ".css": "text/css",
                ".js": "application/javascript",
                ".html": "text/html",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png"
            }
            ext = os.path.splitext(path)[1]
            content_type = mime_types.get(ext, "application/octet-stream")
            
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
            ).encode("utf-8") + content
            writer.write(response)
            await writer.drain()
        except Exception as e:
            self.log(f"Error serving static file: {str(e)}", "error", "❌")
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            await writer.drain()

    async def _handle_action(self, query_params: Dict[str, Any], writer: asyncio.StreamWriter, session_id: str) -> None:
        """Handle actions via GET request with session support."""
        try:
            action = query_params.get('action', [''])[0]
            component_type = query_params.get('component', [''])[0]
            
            self.log(f"Handling action: {action} for component: {component_type}", "info", "🎬")
            
            if action == 'increment':
                # Increment counter
                self.state['counter'] = self.state.get('counter', 0) + 1
                self.log(f"Incremented counter to: {self.state['counter']}", "info", "🔢")
            elif action == 'update_timestamp':
                # Update timestamp
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
                
                # Special handling for current_page state
                if state_name == 'current_page' or (not state_name and state_value in ['home', 'dashboard', 'settings']):
                    # If this is a page navigation, update current_page state
                    self.state['current_page'] = state_value
                    self.log(f"Updated navigation to page: {state_value}", "info", "🧭")
                
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
            
            # Check if this is an immediate action that requires UI refresh
            immediate = query_params.get('immediate', ['false'])[0].lower() == 'true'
            
            # Send success response
            response_data = json.dumps({
                "success": True,
                "action": action,
                "component_type": component_type,
                "state": self.state,
                "immediate": immediate  # Include flag in response
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
            
            # Broadcast update to all clients
            await self.broadcast(json.dumps({
                "type": "state_update",
                "state": self.state
            }))
        
        except Exception as e:
            self.log(f"Action error: {str(e)}", "error", "❌")
            response = (
                "HTTP/1.1 500 Internal Server Error\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n\r\n"
                f"{str(e)}"
            )
            writer.write(response.encode("utf-8"))
            await writer.drain()

    async def _handle_refresh(self, query_params: Dict[str, Any], writer: asyncio.StreamWriter, session_id: str) -> None:
        """Handle refresh requests with session support."""
        try:
            self.version_counter += 1
            
            # Load state from session if available
            if session_id:
                session_state = self.session_manager.get_session_state(session_id)
                if session_state:
                    self.state.update(session_state)
            
            response_data = json.dumps({
                "success": True,
                "version": self.version_counter,
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
            writer.write(response.encode("utf-8"))
            await writer.drain()
        
        except Exception as e:
            self.log(f"Refresh error: {str(e)}", "error", "❌")
            response = (
                "HTTP/1.1 500 Internal Server Error\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n\r\n"
                f"{str(e)}"
            )
            writer.write(response.encode("utf-8"))
            await writer.drain()

    async def _handle_event(self, query_params: Dict[str, Any], writer: asyncio.StreamWriter, session_id: str) -> None:
        """Handle event requests triggered from the frontend."""
        try:
            event_name = query_params.get('event', [None])[0]
            value_str = query_params.get('value', [None])[0] # Get value as string first
            # TODO: Consider how to pass other parameters if needed by handlers

            if not event_name:
                self.log("Missing 'event' parameter in event request", "warning", "⚠️")
                writer.write(b"HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\n\r\n")
                writer.write(json.dumps({"error": "Missing 'event' parameter"}).encode("utf-8"))
                await writer.drain()
                return

            self.log(f"Handling event: {event_name} with value string: '{value_str}'", "info", "⚡")

            # Import the event handler dynamically
            from .decorators import handle_event # Assuming handle_event exists and works this way

            # Prepare event argument (focus on 'value' for now)
            event_arg = None
            if value_str is not None:
                 # Attempt to convert value based on typical usage (float for sliders)
                 try:
                     event_arg = float(value_str)
                 except (ValueError, TypeError):
                     self.log(f"Could not convert event value '{value_str}' to float for event '{event_name}'. Passing as string.", "warning", "⚠️")
                     event_arg = value_str # Fallback to string if conversion fails

            # Call the event handler - Assumes handle_event(name, arg) signature
            # This might need adjustment based on the actual implementation of handle_event
            # and how it looks up and calls the decorated function.
            result = handle_event(event_name, event_arg)

            # Send success response
            response_data = {"status": "success"}
            if result is not None:
                 response_data["result"] = result # Include result if handler returned something

            writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
            writer.write(json.dumps(response_data).encode("utf-8"))
            await writer.drain()
            self.log(f"Event '{event_name}' handled successfully", "info", "✅")

        except Exception as e:
            self.log(f"Error handling event '{event_name}': {str(e)}", "error", "❌")
            if self.verbose:
                traceback.print_exc()
            
            # Send error response
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: application/json\r\n\r\n")
            writer.write(json.dumps({"error": f"Error handling event: {str(e)}"}).encode("utf-8"))
            await writer.drain()

    async def _serve_ui_definition(self, query_params: Dict[str, Any], writer: asyncio.StreamWriter, session_id: str) -> None:
        """Serve the UI definition JSON with session support."""
        try:
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
            
            # Ensure we're using the most recent current_page value
            current_page = self.state.get('current_page')
            if current_page:
                self.log(f"Using current page from state: {current_page}", "info", "📄")
                # Add current_page to the UI state to ensure it's passed to the handler
                if not hasattr(handler, 'ui_state'):
                    handler.ui_state = {}
                handler.ui_state = {'current_page': current_page}

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
        self.log("Serving HTML template", "info", "🌟")
        
        # Try different paths to find the index.html file
        # Get cacao package base dir
        cacao_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        possible_paths = [
            os.path.join(cacao_base_dir, "core", "static", "index.html"),
            os.path.join(os.path.dirname(__file__), "static", "index.html"),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "index.html"),
            # Search directly in the cacao install directory
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                         "cacao", "core", "static", "index.html")
        ]
        
        content = None
        for path in possible_paths:
            self.log(f"Trying to load HTML template from: {path}", "info", "📁")
            try:
                with open(path, "r") as f:
                    content = f.read()
                    self.log(f"Successfully loaded HTML template from: {path}", "info", "✅")
                    break
            except FileNotFoundError:
                continue
        
        if content is None:
            self.log("HTML template not found in any of the expected locations", "error", "❌")
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\nHTML template not found")
            await writer.drain()
            return
            
        try:
            # Add PWA manifest link if enabled
            if self.enable_pwa:
                manifest_link = '<link rel="manifest" href="/manifest.json">'
                content = content.replace('</head>', f'{manifest_link}\n</head>')
            
            # Format the content with the session ID
            content = content.replace('{session_id}', session_id)
            
            # Add debugging meta tag to track server version
            debug_meta = f'<meta name="cacao-server-version" content="{self.version_counter}">'
            content = content.replace('<head>', f'<head>\n{debug_meta}')
            
            self.log(f"Sending HTML template (length: {len(content)})", "info", "📤")
            
            # Write the response
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Set-Cookie: cacao_session={session_id}; Path=/; HttpOnly; SameSite=Strict\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
                f"{content}"
            )
            writer.write(response.encode("utf-8"))
            await writer.drain()
            
            self.log("HTML template served successfully", "info", "✅")
            
        except Exception as e:
            self.log(f"Error serving HTML template: {str(e)}", "error", "❌")
            if self.verbose:
                traceback.print_exc()
            
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            await writer.drain()

    async def _serve_manifest(self, writer: asyncio.StreamWriter) -> None:
        """Serve the PWA manifest.json file."""
        if not self.pwa:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()
            return
            
        manifest_data = self.pwa.generate_manifest()
        json_body = json.dumps(manifest_data)
        
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(json_body)}\r\n"
            "\r\n"
            f"{json_body}"
        )
        writer.write(response.encode("utf-8"))
        await writer.drain()
        
    async def _serve_service_worker(self, writer: asyncio.StreamWriter) -> None:
        """Serve the PWA service worker JavaScript file."""
        if not self.pwa:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()
            return
            
        sw_content = self.pwa.generate_service_worker()
        
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/javascript\r\n"
            f"Content-Length: {len(sw_content)}\r\n"
            "\r\n"
            f"{sw_content}"
        )
        writer.write(response.encode("utf-8"))
        await writer.drain()
        
    async def _serve_offline_page(self, writer: asyncio.StreamWriter) -> None:
        """Serve the PWA offline fallback page."""
        if not self.pwa:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
            await writer.drain()
            return
            
        offline_content = self.pwa.generate_offline_page()
        
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(offline_content)}\r\n"
            "\r\n"
            f"{offline_content}"
        )
        writer.write(response.encode("utf-8"))
        await writer.drain()
    
    async def _setup_ws_server(self):
        """Set up the WebSocket server."""
        self.log("WebSocket server ready", "info", "🌎")
        return await serve(
            self._handle_websocket,
            self.host,
            self.ws_port
        )
        
    async def _run_servers(self):
        """Run both HTTP and WebSocket servers concurrently."""
        
        # Start the WebSocket server
        ws_server = await self._setup_ws_server()
        
        # Set up the HTTP server
        http_server = await asyncio.start_server(
            self._handle_http,
            self.host,
            self.http_port
        )
        
        self.log("HTTP server ready", "info", "🌎")
        
        # Set up file watching if hot reload is enabled or always for now
        if self.hot_reload or True:  # Currently always enabled for development
            self.file_watcher_task = asyncio.create_task(self._watch_files())
        
        # Keep the servers running
        await asyncio.gather(
            ws_server.wait_closed(),
            http_server.serve_forever(),
        )
    def _initialize_icon_registry(self):
        """Initialize the icon registry with configuration from cacao.json."""
        try:
            # Look for cacao.json in the current directory
            config_path = os.path.join(os.getcwd(), "cacao.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                # Extract icon configuration if present
                if 'icons' in config:
                    self.log("Initializing icon registry", "info", "🔣")
                    icon_registry.initialize(config['icons'])
                    self.log(f"Icon registry initialized with config", "info", "✅")
            else:
                self.log("No cacao.json found, using default icon configuration", "warning", "⚠️")
                # Initialize with empty config
                icon_registry.initialize({})
                
        except Exception as e:
            self.log(f"Error initializing icon registry: {str(e)}", "error", "❌")
            # Initialize with empty config to avoid further errors
            icon_registry.initialize({})

    def _apply_extensions(self):
        """Apply all registered extensions to the server."""
        if not self.extensions:
            return
            
        self.log(f"Applying {len(self.extensions)} extension(s)", "info", "🔌")
        for extension in self.extensions:
            try:
                if hasattr(extension, 'apply'):
                    extension.apply(self)
                    self.log(f"Applied extension: {extension.__class__.__name__}", "info", "✅")
                else:
                    self.log(f"Extension {extension.__class__.__name__} has no apply method", "warning", "⚠️")
            except Exception as e:
                self.log(f"Error applying extension {extension.__class__.__name__}: {str(e)}", "error", "❌")
                if self.verbose:
                    traceback.print_exc()

    def run(self):
        """Run the server (blocking call)."""
        global global_server
        try:
            global_server = self
            self._print_banner()
            
            # Apply extensions
            self._apply_extensions()
            

            # Import and access the route handlers
            # This forces the decorators to be evaluated
            try:
                import sys
                if self.main_module in sys.modules:
                    from .decorators import ROUTES
                    if ROUTES:
                        route_paths = list(ROUTES.keys())
                        self.log(f"Routes loaded: {route_paths}", "info", "🛤️")
                    else:
                        self.log("No routes registered", "warning", "⚠️")
                else:
                    # If main_module is a file path, try to import it
                    if os.path.isfile(self.main_module):
                        module_name = os.path.basename(self.main_module).replace('.py', '')
                        try:
                            import importlib.util
                            spec = importlib.util.spec_from_file_location(module_name, self.main_module)
                            if spec and spec.loader:
                                module = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(module)
                                sys.modules[module_name] = module
                                self._actual_module_name = module_name
                                from .decorators import ROUTES
                                if ROUTES:
                                    route_paths = list(ROUTES.keys())
                                    self.log(f" Routes loaded from file: {route_paths}", "info", "🛤️")
                                else:
                                    self.log("No routes registered from file", "warning", "⚠️")
                        except Exception as e:
                            self.log(f"Error importing module from file: {str(e)}", "error", "❌")
            except Exception as e:
                self.log(f"Error loading routes: {str(e)}", "error", "❌")
                
            # Reset the terminal settings for Windows
            os.system("")
            # Initialize the icon registry
            self._initialize_icon_registry()
            
            # Run the asyncio event loop
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                
            asyncio.run(self._run_servers())
                
        except KeyboardInterrupt:
            self.log("Server stopped", "info", "🛑")
        except Exception as e:
            self.log(f"Server error: {str(e)}", "error", "💥")
            if self.verbose:
                traceback.print_exc()
        finally:
            global_server = None
            
    def shutdown(self):
        """Shutdown the server cleanly."""
        self.log("Shutting down server", "info", "🛑")
        # Close all WebSocket connections
        for websocket in self.websocket_clients:
            try:
                websocket.close()
            except:
                pass
        
        # Cancel file watcher task
        if self.file_watcher_task:
            self.file_watcher_task.cancel()
