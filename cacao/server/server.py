"""
WebSocket server for Cacao v2.

Uses Starlette for HTTP and WebSocket handling. The server manages
WebSocket connections, dispatches events, and syncs state to clients.
"""

from __future__ import annotations

import json
import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, Any

from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.responses import HTMLResponse, JSONResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from .signal import Signal
from .session import Session

if TYPE_CHECKING:
    from .ui import App

# Path to frontend build output
FRONTEND_DIST_DIR = Path(__file__).parent.parent / "frontend" / "dist"


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

    async def pages_handler(request: Any) -> JSONResponse:
        """Return the component tree for all pages."""
        # Check if app has fluent UI pages
        if hasattr(app, "get_all_pages"):
            pages = app.get_all_pages()
        else:
            pages = {"/": []}

        # Get app metadata
        metadata = {
            "title": getattr(app, "title", "Cacao App"),
            "theme": getattr(app, "theme", "dark"),
        }

        return JSONResponse({
            "pages": pages,
            "metadata": metadata,
        })

    async def index_handler(request: Any) -> HTMLResponse:
        """Serve the dashboard UI."""
        # Get app metadata
        title = getattr(app, "title", "Cacao App")
        theme = getattr(app, "theme", "dark")

        html = _get_dashboard_html(title, theme)
        return HTMLResponse(html)

    # Set up routes
    # Note: Catch-all route "{path:path}" handles SPA routing - any path
    # not matched by earlier routes serves the index HTML, allowing
    # direct navigation to routes like /base64, /uuid, etc.
    routes = [
        Route("/health", health_handler),
        Route("/api/pages", pages_handler),
        WebSocketRoute("/ws", websocket_handler),
        Mount("/static", StaticFiles(directory=str(FRONTEND_DIST_DIR)), name="static"),
        Route("/", index_handler),
        Route("/{path:path}", index_handler),  # Catch-all for SPA routing
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
    port: int = 1502,  # 1502: Columbus encounters cacao beans in Honduras
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


def _get_dashboard_html(title: str, theme: str) -> str:
    """Generate the dashboard HTML that links to external CSS and JS."""
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="/static/cacao.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</head>
<body>
    <div id="root"><div class="loading">Loading...</div></div>
    <script src="/static/cacao.js"></script>
</body>
</html>'''
