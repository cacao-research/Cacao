"""
WebSocket server for Cacao v2.

Uses Starlette for HTTP and WebSocket handling. The server manages
WebSocket connections, dispatches events, and syncs state to clients.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket, WebSocketDisconnect

from .errors import format_friendly_error
from .log import get_logger, get_uvicorn_log_config
from .plugin import get_registry
from .session import Session
from .signal import Signal

if TYPE_CHECKING:
    from .app import App

logger = get_logger("cacao.server")

# Path to frontend build output
FRONTEND_DIST_DIR = Path(__file__).parent.parent / "frontend" / "dist"


def create_server(app: App) -> Starlette:
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
        await get_registry().run_hook("on_session_start", session)

        logger.debug("Session %s connected", session.id, extra={"label": "ws"})

        try:
            # Check auth requirement
            from .auth import get_auth_provider

            auth_provider = get_auth_provider()
            if auth_provider and not session.metadata.get("authenticated"):
                await session.send({"type": "auth_required"})

            # Send initial state
            initial_state = _get_all_signal_values(session)
            await session.send_init(initial_state)

            # Send registered keyboard shortcuts
            shortcuts = getattr(app, "_shortcuts", [])
            if shortcuts:
                await session.send(
                    {
                        "type": "register_shortcuts",
                        "shortcuts": shortcuts,
                    }
                )

            # Set up signal subscription to push updates
            unsubscribers: list[Callable[..., Any]] = []

            def create_subscriber(signal_name: str) -> Callable[[str, Any], None]:
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
                    logger.warning("Invalid JSON: %s", data, extra={"label": "ws"})
                    continue

                msg_type = message.get("type")
                if app.debug:
                    _preview = data[:200] + ("..." if len(data) > 200 else "")
                    logger.debug(
                        "WS recv [%s] %s", msg_type, _preview,
                        extra={"label": "ws:recv"},
                    )

                if msg_type == "event":
                    event_name = message.get("name", "")
                    event_data = message.get("data", {})

                    logger.debug("Event: %s %s", event_name, event_data, extra={"label": "event"})

                    try:
                        await app.handle_event(session, event_name, event_data)
                    except Exception as ev_exc:
                        logger.exception(
                            "Error handling event '%s'", event_name,
                            extra={"label": "error"},
                        )
                        if app.debug:
                            err = format_friendly_error(
                                ev_exc, context=f"handling event '{event_name}'",
                            )
                            await session.send({"type": "server:error", **err})

                elif msg_type == "chat:send":
                    # LLM-powered chat message
                    signal_name = message.get("signal", "")
                    text = message.get("text", "")
                    if signal_name and text:
                        from .llm import handle_chat_message

                        sig = Signal.get_all_signals().get(signal_name)
                        if sig:
                            asyncio.create_task(
                                handle_chat_message(session, sig, text)
                            )

                elif msg_type == "interface:submit":
                    from .interface import handle_interface_event

                    iface_id = message.get("id", "")
                    input_values = message.get("inputs", {})
                    logger.debug("Interface submit: %s", iface_id, extra={"label": "interface"})
                    asyncio.create_task(
                        handle_interface_event(session, iface_id, input_values)
                    )

                elif msg_type == "interface:flag":
                    from .interface import handle_interface_flag

                    iface_id = message.get("id", "")
                    input_values = message.get("inputs", {})
                    output_value = message.get("output")
                    note = message.get("note", "")
                    await handle_interface_flag(
                        session, iface_id, input_values, output_value, note
                    )

                elif msg_type == "extract:submit":
                    from .llm import extract_structured

                    text = message.get("text", "")
                    schema = message.get("schema")
                    model_str = message.get("model", "openai/gpt-4o")
                    api_key = message.get("api_key")
                    extract_id = message.get("id", "")

                    async def _do_extract(
                        _s: Session, _text: str, _schema: dict, _model: str, _key: str | None, _eid: str
                    ) -> None:
                        try:
                            result = await extract_structured(
                                _text, schema=_schema, model=_model, api_key=_key,
                            )
                            await _s.send({
                                "type": "extract:result",
                                "id": _eid,
                                "result": result.get("result", {}),
                                "usage": result.get("usage", {}),
                            })
                        except Exception as e:
                            await _s.send({
                                "type": "extract:error",
                                "id": _eid,
                                "error": str(e),
                            })

                    asyncio.create_task(
                        _do_extract(session, text, schema, model_str, api_key, extract_id)
                    )

                elif msg_type == "document:upload":
                    from .llm import ingest_document

                    file_path = message.get("file_path", "")
                    file_type = message.get("file_type")
                    schema = message.get("schema")
                    model_str = message.get("model", "openai/gpt-4o")
                    api_key = message.get("api_key")
                    doc_id = message.get("id", "")

                    async def _do_ingest(
                        _s: Session, _path: str, _ft: str | None, _schema: dict | None,
                        _model: str, _key: str | None, _did: str,
                    ) -> None:
                        try:
                            result = await ingest_document(
                                _path, file_type=_ft, schema=_schema,
                                model=_model, api_key=_key,
                            )
                            await _s.send({
                                "type": "document:result",
                                "id": _did,
                                "text": result.get("text", ""),
                                "metadata": result.get("metadata", {}),
                                "extracted": result.get("extracted"),
                                "extraction_usage": result.get("extraction_usage"),
                            })
                        except Exception as e:
                            await _s.send({
                                "type": "document:error",
                                "id": _did,
                                "error": str(e),
                            })

                    asyncio.create_task(
                        _do_ingest(session, file_path, file_type, schema, model_str, api_key, doc_id)
                    )

                elif msg_type == "models:discover":
                    from .llm import discover_models

                    grouped = message.get("grouped", True)

                    async def _do_discover(_s: Session, _grouped: bool) -> None:
                        try:
                            models = await asyncio.to_thread(
                                discover_models, grouped=_grouped, include_capabilities=True,
                            )
                            await _s.send({
                                "type": "models:result",
                                "models": models,
                            })
                        except Exception as e:
                            await _s.send({
                                "type": "models:error",
                                "error": str(e),
                            })

                    asyncio.create_task(_do_discover(session, grouped))

                elif msg_type == "cost:get":
                    from .llm import get_cost_tracker

                    tracker = get_cost_tracker(session.id)
                    await session.send({
                        "type": "cost:summary",
                        "summary": tracker.summary(),
                    })

                # ── Tukuy Skills ──────────────────────────────────
                elif msg_type == "skill:invoke":
                    from .tukuy_skills import handle_skill_invoke

                    asyncio.create_task(
                        handle_skill_invoke(
                            session,
                            skill_name=message.get("skill_name", ""),
                            inputs=message.get("inputs", {}),
                            invoke_id=message.get("id", ""),
                        )
                    )

                elif msg_type == "skill:browse":
                    from .tukuy_skills import handle_skill_browse

                    asyncio.create_task(handle_skill_browse(session))

                elif msg_type == "skill:search":
                    from .tukuy_skills import handle_skill_search

                    asyncio.create_task(
                        handle_skill_search(
                            session,
                            query=message.get("query", ""),
                            limit=message.get("limit", 20),
                        )
                    )

                elif msg_type == "skill:details":
                    from .tukuy_skills import handle_skill_details

                    asyncio.create_task(
                        handle_skill_details(
                            session,
                            skill_names=message.get("names", []),
                        )
                    )

                elif msg_type == "chain:run":
                    from .tukuy_skills import handle_chain_run

                    asyncio.create_task(
                        handle_chain_run(
                            session,
                            chain_id=message.get("id", ""),
                            steps=message.get("steps", []),
                            input_value=message.get("input", ""),
                        )
                    )

                elif msg_type == "transform:run":
                    from .tukuy_skills import handle_transform

                    asyncio.create_task(
                        handle_transform(
                            session,
                            transform_id=message.get("id", ""),
                            transformer_name=message.get("name", ""),
                            input_value=message.get("input", ""),
                            params=message.get("params"),
                        )
                    )

                elif msg_type == "transform:list":
                    from .tukuy_skills import handle_transform_list

                    asyncio.create_task(handle_transform_list(session))

                elif msg_type == "safety:set":
                    from .tukuy_skills import handle_safety_set

                    asyncio.create_task(
                        handle_safety_set(
                            session,
                            policy_config=message.get("policy", {}),
                        )
                    )

                elif msg_type == "safety:get":
                    from .tukuy_skills import handle_safety_get

                    asyncio.create_task(handle_safety_get(session))

                # ── Agent Components ──────────────────────────────
                elif msg_type == "agent:run":
                    from .agent import handle_agent_run

                    asyncio.create_task(
                        handle_agent_run(
                            session,
                            agent_id=message.get("agent_id", ""),
                            text=message.get("text", ""),
                        )
                    )

                elif msg_type == "multi_agent:run":
                    from .agent import handle_multi_agent_run

                    asyncio.create_task(
                        handle_multi_agent_run(
                            session,
                            multi_id=message.get("multi_id", ""),
                            text=message.get("text", ""),
                        )
                    )

                elif msg_type == "budget:get":
                    from .llm import get_cost_tracker

                    tracker = get_cost_tracker(session.id)
                    await session.send({
                        "type": "budget:summary",
                        "summary": tracker.summary(),
                    })

                # ── SQL Query ─────────────────────────────────────
                elif msg_type == "sql_query":
                    from .sql import handle_sql_query

                    asyncio.create_task(
                        handle_sql_query(
                            session,
                            connection=message.get("connection", ""),
                            conn_type=message.get("connType", "unknown"),
                            query=message.get("query", ""),
                            max_rows=message.get("maxRows", 1000),
                        )
                    )

        except WebSocketDisconnect:
            pass
        except Exception as e:
            logger.warning("WebSocket error: %s", e, extra={"label": "ws"})
        finally:
            # Clean up
            for unsub in unsubscribers:
                unsub()

            # Clean up Tukuy session policy
            from .tukuy_skills import cleanup_session_policy
            cleanup_session_policy(session.id)

            await get_registry().run_hook("on_session_end", session)
            app.sessions.remove(session.id)

            logger.debug("Session %s disconnected", session.id, extra={"label": "ws"})

    async def health_handler(request: Any) -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse(
            {
                "status": "ok",
                "sessions": app.sessions.count,
            }
        )

    async def pages_handler(request: Any) -> JSONResponse:
        """Return the component tree for all pages."""
        try:
            # Check if app has fluent UI pages
            if hasattr(app, "get_all_pages"):
                pages = app.get_all_pages()
            else:
                pages = {"/": []}
        except Exception as page_exc:
            logger.exception("Error building pages", extra={"label": "error"})
            err = format_friendly_error(page_exc, context="building the component tree")
            return JSONResponse(
                {"pages": {"/": []}, "metadata": {"title": "Error"}, "slots": {}, "error": err},
                status_code=200,  # 200 so the frontend can display the overlay
            )

        # Get app metadata
        metadata = {
            "title": getattr(app, "title", "Cacao App"),
            "theme": getattr(app, "theme", "dark"),
        }

        # Get plugin slot content
        registry = get_registry()
        slots: dict[str, list[dict[str, Any]]] = {}
        for slot_name in ("header", "footer", "sidebar", "head"):
            renderers = registry.get_slot_renderers(slot_name)
            if renderers:
                slot_content: list[dict[str, Any]] = []
                for renderer in renderers:
                    try:
                        result = renderer()
                        if hasattr(result, "__await__"):
                            result = await result
                        # Result should be a Component or dict
                        if hasattr(result, "to_dict"):
                            slot_content.append(result.to_dict())
                        elif isinstance(result, dict):
                            slot_content.append(result)
                        elif isinstance(result, str):
                            slot_content.append({"type": "RawHtml", "props": {"html": result}})
                    except Exception:
                        logger.exception("Error in slot renderer for '%s'", slot_name)
                if slot_content:
                    slots[slot_name] = slot_content

        return JSONResponse(
            {
                "pages": pages,
                "metadata": metadata,
                "slots": slots,
            }
        )

    async def auth_login_handler(request: Any) -> JSONResponse:
        """Handle login requests."""
        from .auth import get_auth_provider

        provider = get_auth_provider()
        if not provider:
            return JSONResponse(
                {"success": False, "message": "Auth not configured"}, status_code=400
            )

        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"success": False, "message": "Invalid request"}, status_code=400)

        user = await provider.authenticate(body)
        if user:
            token = ""
            if hasattr(provider, "create_token"):
                token = provider.create_token(user)
            return JSONResponse(
                {
                    "success": True,
                    "token": token,
                    "user": {"username": user.username, "permissions": list(user.permissions)},
                }
            )
        return JSONResponse({"success": False, "message": "Invalid credentials"}, status_code=401)

    async def index_handler(request: Any) -> HTMLResponse:
        """Serve the dashboard UI."""
        # Get app metadata
        title = getattr(app, "title", "Cacao App")
        theme = getattr(app, "theme", "dark")
        branding = getattr(app, "branding", None)

        # Determine which component categories are used
        categories: set[str] | None = None
        if hasattr(app, "get_used_categories"):
            categories = app.get_used_categories()

        # Gather custom themes and plugin scripts
        custom_themes = getattr(app, "_custom_themes", {})
        plugin_scripts = _get_plugin_scripts()

        html = _get_dashboard_html(
            title,
            theme,
            branding,
            categories=categories,
            custom_themes=custom_themes,
            plugin_scripts=plugin_scripts,
            debug=app.debug,
        )
        return HTMLResponse(html)

    # Set up routes
    # Note: Catch-all route "{path:path}" handles SPA routing - any path
    # not matched by earlier routes serves the index HTML, allowing
    # direct navigation to routes like /base64, /uuid, etc.
    routes = [
        Route("/health", health_handler),
        Route("/api/pages", pages_handler),
        Route("/api/auth/login", auth_login_handler, methods=["POST"]),
        WebSocketRoute("/ws", websocket_handler),
        Mount("/static", StaticFiles(directory=str(FRONTEND_DIST_DIR)), name="static"),
    ]

    # Mount plugin static files directory if it exists
    plugins_dir = Path.cwd() / "plugins"
    if plugins_dir.is_dir():
        routes.append(Mount("/plugins", StaticFiles(directory=str(plugins_dir)), name="plugins"))

    routes.extend(
        [
            Route("/", index_handler),
            Route("/{path:path}", index_handler),  # Catch-all for SPA routing
        ]
    )

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
    app: App,
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

    log_config = get_uvicorn_log_config(debug=app.debug)
    logger.info(
        "Listening on http://%s:%d",
        host,
        port,
        extra={"label": "ready"},
    )

    uvicorn.run(
        starlette_app,
        host=host,
        port=port,
        reload=reload,
        log_config=log_config,
    )


def _get_branding_html(branding: bool | str | None) -> str:
    """Generate branding badge HTML."""
    if not branding:
        return ""
    if isinstance(branding, str):
        content = branding
    else:
        content = (
            'Built with <a href="https://github.com/cacao-research/Cacao"'
            ' target="_blank"><strong>Cacao</strong></a> &#x1F90E;'
        )
    return f'\n    <div class="cacao-branding">{content}</div>'


def _get_css_links(categories: set[str] | None) -> str:
    """Generate CSS link tags based on used categories."""
    if categories is not None and (FRONTEND_DIST_DIR / "cacao-core.css").exists():
        # Split CSS: core + per-category
        links = ['    <link rel="stylesheet" href="/static/cacao-core.css">']
        for cat in sorted(categories):
            links.append(f'    <link rel="stylesheet" href="/static/cacao-cat-{cat}.css">')
        return "\n".join(links)

    # Fallback: load full bundle
    return '    <link rel="stylesheet" href="/static/cacao.css">'


def _get_plugin_scripts() -> list[str]:
    """Get JS URLs registered by plugins for custom components."""
    registry = get_registry()
    scripts: list[str] = []
    for plugin in registry.all().values():
        for url in plugin.metadata.get("js_urls", []):
            scripts.append(url)
    return scripts


def _get_custom_theme_css(themes: dict[str, dict[str, str]]) -> str:
    """Generate CSS for custom themes."""
    if not themes:
        return ""
    parts = []
    for name, variables in themes.items():
        props = "\n".join(f"    --{k}: {v};" for k, v in variables.items())
        parts.append(f'  [data-theme="{name}"] {{\n{props}\n  }}')
    css = "\n".join(parts)
    return f"\n    <style>\n{css}\n    </style>"


def _get_dashboard_html(
    title: str,
    theme: str,
    branding: bool | str | None = None,
    categories: set[str] | None = None,
    custom_themes: dict[str, dict[str, str]] | None = None,
    plugin_scripts: list[str] | None = None,
    debug: bool = False,
) -> str:
    """Generate the dashboard HTML that links to external CSS and JS."""
    branding_html = _get_branding_html(branding)
    css_links = _get_css_links(categories)
    needs_charts = categories is None or "charts" in (categories or set())
    chartjs_tag = (
        '\n    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>'
        if needs_charts
        else ""
    )
    theme_css = _get_custom_theme_css(custom_themes or {})
    plugin_script_tags = ""
    for url in plugin_scripts or []:
        plugin_script_tags += f'\n    <script src="{url}"></script>'
    debug_script = (
        '\n    <script>window.__CACAO_DEBUG__ = true;</script>'
        if debug else ""
    )
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
{css_links}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>{chartjs_tag}{theme_css}
</head>
<body>
    <div id="root"><div class="loading">Loading...</div></div>{branding_html}{debug_script}
    <script src="/static/cacao.js"></script>{plugin_script_tags}
</body>
</html>'''
