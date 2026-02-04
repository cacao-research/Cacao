"""
WebSocket server for Cacao v2.

Uses Starlette for HTTP and WebSocket handling. The server manages
WebSocket connections, dispatches events, and syncs state to clients.
"""

from __future__ import annotations

import json
import asyncio
from typing import TYPE_CHECKING, Any

from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import HTMLResponse, JSONResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from .signal import Signal
from .session import Session

if TYPE_CHECKING:
    from .app import App


def create_server(app: "App") -> Starlette:
    """
    Create a Starlette server for the Cacao app.

    Args:
        app: The Cacao App instance

    Returns:
        Configured Starlette application
    """

    async def websocket_handler(websocket: WebSocket) -> None:
        """Handle WebSocket connections."""
        await websocket.accept()

        # Create session for this connection
        session = app.sessions.create(websocket)

        if app.debug:
            print(f"[Cacao] Session {session.id} connected")

        try:
            # Send initial state
            initial_state = _get_all_signal_values(session)
            await session.send_init(initial_state)

            # Set up signal subscription to push updates
            unsubscribers: list[callable] = []

            def create_subscriber(signal_name: str) -> callable:
                def on_change(session_id: str, value: Any) -> None:
                    if session_id == session.id:
                        session.queue_update(signal_name, value)

                return on_change

            for name, signal in Signal.get_all_signals().items():
                if hasattr(signal, "subscribe"):
                    unsub = signal.subscribe(create_subscriber(name))
                    unsubscribers.append(unsub)

            # Handle incoming messages
            while True:
                data = await websocket.receive_text()

                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    if app.debug:
                        print(f"[Cacao] Invalid JSON: {data}")
                    continue

                msg_type = message.get("type")

                if msg_type == "event":
                    event_name = message.get("name", "")
                    event_data = message.get("data", {})

                    if app.debug:
                        print(f"[Cacao] Event: {event_name} {event_data}")

                    await app.handle_event(session, event_name, event_data)

        except WebSocketDisconnect:
            pass
        except Exception as e:
            if app.debug:
                print(f"[Cacao] WebSocket error: {e}")
        finally:
            # Clean up
            for unsub in unsubscribers:
                unsub()

            app.sessions.remove(session.id)

            if app.debug:
                print(f"[Cacao] Session {session.id} disconnected")

    async def health_handler(request: Any) -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse({
            "status": "ok",
            "sessions": app.sessions.count,
        })

    async def index_handler(request: Any) -> HTMLResponse:
        """Serve a simple index page for development."""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Cacao v2</title>
    <style>
        body { font-family: system-ui, sans-serif; padding: 2rem; }
        .status { padding: 0.5rem 1rem; border-radius: 4px; display: inline-block; }
        .connected { background: #d4edda; color: #155724; }
        .disconnected { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>Cacao v2 Server</h1>
    <p>Server is running. Connect your React client to <code>ws://localhost:8000/ws</code></p>
    <p>Status: <span id="status" class="status disconnected">Checking...</span></p>
    <p>Sessions: <span id="sessions">-</span></p>
    <script>
        async function checkHealth() {
            try {
                const res = await fetch('/health');
                const data = await res.json();
                document.getElementById('status').textContent = data.status;
                document.getElementById('status').className = 'status connected';
                document.getElementById('sessions').textContent = data.sessions;
            } catch (e) {
                document.getElementById('status').textContent = 'disconnected';
                document.getElementById('status').className = 'status disconnected';
            }
        }
        checkHealth();
        setInterval(checkHealth, 5000);
    </script>
</body>
</html>
"""
        return HTMLResponse(html)

    # Set up routes
    routes = [
        Route("/", index_handler),
        Route("/health", health_handler),
        WebSocketRoute("/ws", websocket_handler),
    ]

    # Create Starlette app
    starlette_app = Starlette(
        debug=app.debug,
        routes=routes,
        on_startup=[app.startup],
        on_shutdown=[app.shutdown],
    )

    # Add CORS middleware for development
    starlette_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return starlette_app


def _get_all_signal_values(session: Session) -> dict[str, Any]:
    """Get all signal values for a session."""
    result = {}
    for name, signal in Signal.get_all_signals().items():
        if hasattr(signal, "get"):
            result[name] = signal.get(session)
    return result


def run_server(
    app: "App",
    *,
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False,
) -> None:
    """
    Run the Cacao server.

    Args:
        app: The Cacao App instance
        host: Host to bind to
        port: Port to listen on
        reload: Enable auto-reload (requires uvicorn[standard])
    """
    import uvicorn

    starlette_app = create_server(app)

    print(f"[Cacao] Starting server at http://{host}:{port}")
    print(f"[Cacao] WebSocket endpoint: ws://{host}:{port}/ws")

    uvicorn.run(
        starlette_app,
        host=host,
        port=port,
        reload=reload,
    )
