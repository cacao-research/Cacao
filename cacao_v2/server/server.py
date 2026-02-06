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
    from .ui import App


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
    routes = [
        Route("/", index_handler),
        Route("/health", health_handler),
        Route("/api/pages", pages_handler),
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


def _get_dashboard_html(title: str, theme: str) -> str:
    """Generate the self-contained dashboard HTML with React renderer."""
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            /* Cacao/Chocolate dark theme - warm browns with caramel accents */
            --bg-primary: #1a1412;
            --bg-secondary: #231c18;
            --bg-tertiary: #2d241e;
            --bg-card: #352a22;
            --bg-card-hover: #3d322a;
            --text-primary: #f5ebe0;
            --text-secondary: #c4a98a;
            --text-muted: #8b7355;
            --border-color: rgba(139, 115, 85, 0.3);
            --border-subtle: rgba(139, 115, 85, 0.15);
            --accent-primary: #d4a574;
            --accent-secondary: #e8c49a;
            --accent-glow: rgba(212, 165, 116, 0.2);
            --success: #7cb342;
            --success-bg: rgba(124, 179, 66, 0.15);
            --warning: #ffb74d;
            --warning-bg: rgba(255, 183, 77, 0.15);
            --danger: #e57373;
            --danger-bg: rgba(229, 115, 115, 0.15);
            --info: #64b5f6;
            --info-bg: rgba(100, 181, 246, 0.15);
            --gradient-start: #d4a574;
            --gradient-end: #8b5a3c;
            --chart-1: #d4a574;
            --chart-2: #8b5a3c;
            --chart-3: #7cb342;
            --chart-4: #64b5f6;
            --chart-5: #ffb74d;
            --chart-6: #e57373;
            --spacing-unit: 4px;
        }}
        [data-theme="light"] {{
            --bg-primary: #faf6f1;
            --bg-secondary: #f5ebe0;
            --bg-tertiary: #ede0d4;
            --bg-card: #ffffff;
            --bg-card-hover: #fdfbf8;
            --text-primary: #3d2c1e;
            --text-secondary: #6b5344;
            --text-muted: #9c8675;
            --border-color: rgba(109, 83, 68, 0.2);
            --border-subtle: rgba(109, 83, 68, 0.1);
            --accent-primary: #8b5a3c;
            --accent-secondary: #a0674a;
            --accent-glow: rgba(139, 90, 60, 0.15);
        }}
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        #root {{ display: flex; min-height: 100vh; width: 100%; }}
        .app-container {{ flex: 1; display: flex; width: 100%; }}
        .main-content {{
            flex: 1;
            width: 100%;
            min-width: 0;
            padding: 2rem 2.5rem;
            overflow-y: auto;
            background: var(--bg-primary);
        }}
        .sidebar {{
            width: 260px;
            flex-shrink: 0;
            background: var(--bg-secondary);
            border-left: 1px solid var(--border-color);
            padding: 1.5rem;
            overflow-y: auto;
        }}
        /* Layout components */
        .c-row {{
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap;
            align-items: stretch;
            width: 100%;
        }}
        .c-row.justify-between {{ justify-content: space-between; }}
        .c-col {{
            display: flex;
            flex-direction: column;
            flex: 1;
            min-width: 0;
        }}
        .c-grid {{
            display: grid !important;
            width: 100%;
        }}
        .col-span-3 {{ flex: 0 0 calc(25% - 12px); min-width: 180px; }}
        .col-span-4 {{ flex: 0 0 calc(33.333% - 12px); min-width: 220px; }}
        .col-span-6 {{ flex: 0 0 calc(50% - 10px); min-width: 280px; }}
        .col-span-8 {{ flex: 0 0 calc(66.666% - 8px); min-width: 360px; }}
        .col-span-12 {{ flex: 0 0 100%; }}
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            transition: border-color 0.2s ease;
        }}
        .card:hover {{
            border-color: var(--accent-primary);
        }}
        .card-title {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-subtle);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .metric {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            min-width: 180px;
            flex: 1;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }}
        .metric::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
        }}
        .metric:hover {{
            border-color: var(--accent-primary);
            background: var(--bg-card-hover);
        }}
        .metric-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 500;
        }}
        .metric-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        .metric-trend {{
            font-size: 0.8rem;
            margin-top: 0.625rem;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.2rem 0.5rem;
            border-radius: 6px;
            font-weight: 500;
        }}
        .metric-trend.up {{
            color: var(--success);
            background: var(--success-bg);
        }}
        .metric-trend.down {{
            color: var(--danger);
            background: var(--danger-bg);
        }}
        .title {{ margin-bottom: 0.5rem; color: var(--text-primary); }}
        .title-1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.02em; }}
        .title-2 {{ font-size: 1.5rem; font-weight: 600; }}
        .title-3 {{ font-size: 1.125rem; font-weight: 600; color: var(--text-secondary); }}
        .title-4 {{ font-size: 1rem; font-weight: 600; color: var(--text-secondary); }}
        .text {{ color: var(--text-secondary); line-height: 1.6; }}
        .text-muted {{ color: var(--text-muted); }}
        .text-sm {{ font-size: 0.875rem; }}
        .text-lg {{ font-size: 1.125rem; }}
        .spacer {{ height: 1rem; }}
        .spacer-2 {{ height: 0.5rem; }}
        .spacer-4 {{ height: 1rem; }}
        .spacer-8 {{ height: 2rem; }}
        .divider {{
            border: none;
            border-top: 1px solid var(--border-subtle);
            margin: 1rem 0;
        }}
        .alert {{
            padding: 0.875rem 1rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
            font-size: 0.875rem;
        }}
        .alert-info {{ background: var(--info-bg); border: 1px solid var(--info); color: var(--info); }}
        .alert-success {{ background: var(--success-bg); border: 1px solid var(--success); color: var(--success); }}
        .alert-warning {{ background: var(--warning-bg); border: 1px solid var(--warning); color: var(--warning); }}
        .alert-error {{ background: var(--danger-bg); border: 1px solid var(--danger); color: var(--danger); }}
        .progress-container {{ margin: 0.5rem 0; }}
        .progress-label {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.375rem; font-weight: 500; }}
        .progress-bar {{
            height: 8px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: var(--accent-primary);
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        .gauge-container {{ display: flex; flex-direction: column; align-items: center; padding: 1rem; }}
        .gauge-svg {{ width: 120px; height: 80px; }}
        .gauge-value {{ font-size: 1.5rem; font-weight: 700; margin-top: 0.5rem; color: var(--text-primary); }}
        .gauge-title {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }}
        .table-container {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; }}
        th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border-subtle); }}
        th {{
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.04em;
            background: var(--bg-tertiary);
        }}
        tbody tr:hover {{ background: var(--bg-card-hover); }}
        .btn {{
            padding: 0.625rem 1.25rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.875rem;
            cursor: pointer;
            border: none;
            transition: all 0.15s ease;
        }}
        .btn-primary {{
            background: var(--accent-primary);
            color: var(--bg-primary);
            font-weight: 600;
        }}
        .btn-primary:hover {{ background: var(--accent-secondary); }}
        .btn-secondary {{
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }}
        .btn-secondary:hover {{ background: var(--bg-card-hover); }}
        .btn-ghost {{ background: transparent; color: var(--text-secondary); }}
        .btn-ghost:hover {{ background: var(--bg-tertiary); }}
        .select-container {{ margin-bottom: 1rem; }}
        .select-label {{
            display: block;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 0.375rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        .select {{
            width: 100%;
            padding: 0.625rem 0.875rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background: var(--bg-tertiary);
            color: var(--text-primary);
            font-size: 0.875rem;
            cursor: pointer;
        }}
        .select:hover {{ border-color: var(--accent-primary); }}
        .select:focus {{ outline: none; border-color: var(--accent-primary); }}
        .checkbox-container {{
            display: flex;
            align-items: flex-start;
            gap: 0.625rem;
            margin-bottom: 0.875rem;
            padding: 0.5rem;
            border-radius: 6px;
        }}
        .checkbox-container:hover {{ background: var(--bg-tertiary); }}
        .checkbox {{
            width: 18px;
            height: 18px;
            accent-color: var(--accent-primary);
            cursor: pointer;
            flex-shrink: 0;
            margin-top: 2px;
        }}
        .checkbox-label {{ font-size: 0.875rem; color: var(--text-primary); }}
        .checkbox-desc {{ font-size: 0.75rem; color: var(--text-muted); margin-top: 0.125rem; }}
        .slider-container {{ margin-bottom: 1rem; }}
        .slider-label {{
            display: block;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}
        .slider {{
            width: 100%;
            accent-color: var(--accent-primary);
            cursor: pointer;
        }}
        .tabs {{
            display: flex;
            gap: 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 1.25rem;
        }}
        .tab {{
            padding: 0.625rem 1rem;
            font-size: 0.875rem;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            margin-bottom: -1px;
            transition: all 0.15s ease;
            font-weight: 500;
        }}
        .tab:hover {{ color: var(--text-primary); }}
        .tab.active {{
            color: var(--accent-primary);
            border-bottom-color: var(--accent-primary);
        }}
        .chart-container {{ width: 100%; height: 280px; }}
        .loading {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: var(--text-muted);
            font-size: 0.875rem;
        }}
        @media (max-width: 1024px) {{
            .main-content {{ padding: 1.5rem; }}
            .col-span-3, .col-span-4 {{ flex: 0 0 calc(50% - 10px); min-width: 180px; }}
            .col-span-8 {{ flex: 0 0 100%; min-width: unset; }}
        }}
        @media (max-width: 768px) {{
            .sidebar {{ display: none; }}
            .main-content {{ padding: 1rem; }}
            .col-span-3, .col-span-4, .col-span-6, .col-span-8 {{ flex: 0 0 100%; min-width: unset; }}
            .c-row {{ flex-direction: column !important; }}
            .metric {{ min-width: unset; }}
            .title-1 {{ font-size: 1.75rem; }}
            .metric-value {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div id="root"><div class="loading">Loading dashboard...</div></div>
    <script>
    const {{ createElement: h, useState, useEffect, useRef }} = React;
    // Chocolate/Cacao themed chart colors
    const COLORS = ['#d4a574', '#8b5a3c', '#7cb342', '#64b5f6', '#ffb74d', '#e57373', '#a1887f', '#90a4ae', '#ce93d8', '#80cbc4'];

    // Chart.js wrapper component
    function ChartComponent({{ type, data, options, height }}) {{
        const canvasRef = useRef(null);
        const chartRef = useRef(null);

        useEffect(() => {{
            if (!canvasRef.current || !data) return;
            if (chartRef.current) chartRef.current.destroy();

            const ctx = canvasRef.current.getContext('2d');
            Chart.defaults.color = '#c4a98a';
            Chart.defaults.borderColor = 'rgba(139, 115, 85, 0.2)';

            chartRef.current = new Chart(ctx, {{ type, data, options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: data.datasets?.length > 1 }} }},
                ...options
            }} }});

            return () => {{ if (chartRef.current) chartRef.current.destroy(); }};
        }}, [type, JSON.stringify(data)]);

        return h('div', {{ style: {{ height: height || 300, width: '100%' }} }},
            h('canvas', {{ ref: canvasRef }})
        );
    }}

    // Component renderers
    const renderers = {{
        Row: ({{ props, children }}) => h('div', {{
            className: 'c-row' + (props.justify === 'between' ? ' justify-between' : ''),
            style: {{ gap: ((props.gap || 4) * 4) + 'px' }}
        }}, children),
        Col: ({{ props, children }}) => h('div', {{
            className: 'c-col' + (props.span ? ' col-span-' + props.span : ''),
            style: {{ gap: ((props.gap || 4) * 4) + 'px' }}
        }}, children),
        Grid: ({{ props, children }}) => h('div', {{
            className: 'c-grid',
            style: {{ gap: ((props.gap || 4) * 4) + 'px', gridTemplateColumns: 'repeat(' + (props.cols || 12) + ', 1fr)' }}
        }}, children),
        Card: ({{ props, children }}) => h('div', {{ className: 'card' }}, [
            props.title && h('div', {{ className: 'card-title', key: 'title' }}, props.title),
            ...children
        ]),
        Sidebar: ({{ props, children }}) => h('div', {{ className: 'sidebar' }}, children),
        Title: ({{ props }}) => h('h' + (props.level || 1), {{ className: 'title title-' + (props.level || 1) }}, props.text),
        Text: ({{ props }}) => h('p', {{ className: 'text ' + (props.color === 'muted' ? 'text-muted' : '') + ' ' + (props.size === 'sm' ? 'text-sm' : props.size === 'lg' ? 'text-lg' : '') }}, props.content),
        Spacer: ({{ props }}) => h('div', {{ style: {{ height: (props.size || 4) * 4 }} }}),
        Divider: () => h('hr', {{ className: 'divider' }}),
        Metric: ({{ props }}) => h('div', {{ className: 'metric' }}, [
            h('div', {{ className: 'metric-label', key: 'label' }}, props.label),
            h('div', {{ className: 'metric-value', key: 'value' }}, (props.prefix || '') + props.value + (props.suffix || '')),
            props.trend && h('div', {{ className: 'metric-trend ' + (props.trendDirection || (props.trend.startsWith('+') ? 'up' : 'down')), key: 'trend' }},
                (props.trendDirection === 'up' || props.trend.startsWith('+') ? '↑ ' : '↓ ') + props.trend
            )
        ]),
        Alert: ({{ props }}) => h('div', {{ className: 'alert alert-' + (props.type || 'info') }}, [
            props.title && h('strong', {{ key: 'title' }}, props.title + ': '),
            props.message
        ]),
        Progress: ({{ props }}) => h('div', {{ className: 'progress-container' }}, [
            props.label && h('div', {{ className: 'progress-label', key: 'label' }}, props.label),
            h('div', {{ className: 'progress-bar', key: 'bar' }},
                h('div', {{ className: 'progress-fill', style: {{ width: ((props.value / (props.max || 100)) * 100) + '%' }} }})
            )
        ]),
        Gauge: ({{ props }}) => {{
            const pct = (props.value / (props.max_value || 100)) * 100;
            const angle = (pct / 100) * 180;
            return h('div', {{ className: 'gauge-container' }}, [
                h('svg', {{ className: 'gauge-svg', viewBox: '0 0 120 80', key: 'svg' }}, [
                    h('defs', {{ key: 'defs' }}, h('linearGradient', {{ id: 'gaugeGradient', x1: '0%', y1: '0%', x2: '100%', y2: '0%' }}, [
                        h('stop', {{ offset: '0%', stopColor: 'var(--gradient-start)', key: 's1' }}),
                        h('stop', {{ offset: '100%', stopColor: 'var(--gradient-end)', key: 's2' }})
                    ])),
                    h('path', {{ d: 'M10 70 A50 50 0 0 1 110 70', fill: 'none', stroke: 'var(--bg-tertiary)', strokeWidth: 12, strokeLinecap: 'round', key: 'bg' }}),
                    h('path', {{ d: 'M10 70 A50 50 0 0 1 110 70', fill: 'none', stroke: 'url(#gaugeGradient)', strokeWidth: 12, strokeLinecap: 'round', strokeDasharray: ((angle / 180) * 157) + ' 157', key: 'fill' }})
                ]),
                h('div', {{ className: 'gauge-value', key: 'value' }}, props.format ? props.format.replace('{{value}}', props.value) : props.value + '%'),
                props.title && h('div', {{ className: 'gauge-title', key: 'title' }}, props.title)
            ]);
        }},
        Table: ({{ props }}) => {{
            const data = props.data || [];
            const columns = props.columns || (data[0] ? Object.keys(data[0]) : []);
            const colDefs = columns.map(c => typeof c === 'string' ? {{ key: c, title: c }} : c);
            return h('div', {{ className: 'table-container' }},
                h('table', null, [
                    h('thead', {{ key: 'head' }}, h('tr', null, colDefs.map(c => h('th', {{ key: c.key }}, c.title || c.key)))),
                    h('tbody', {{ key: 'body' }}, data.slice(0, props.pageSize || 10).map((row, i) =>
                        h('tr', {{ key: i }}, colDefs.map(c => h('td', {{ key: c.key }}, formatValue(row[c.key]))))
                    ))
                ])
            );
        }},
        Button: ({{ props }}) => h('button', {{ className: 'btn btn-' + (props.variant || 'primary') }}, props.label),
        Select: ({{ props }}) => h('div', {{ className: 'select-container' }}, [
            h('label', {{ className: 'select-label', key: 'label' }}, props.label),
            h('select', {{ className: 'select', key: 'select' }},
                (props.options || []).map((o, i) => h('option', {{ key: i, value: o.value || o }}, o.label || o))
            )
        ]),
        Checkbox: ({{ props }}) => h('div', {{ className: 'checkbox-container' }}, [
            h('input', {{ type: 'checkbox', className: 'checkbox', key: 'input' }}),
            h('div', {{ key: 'text' }}, [
                h('div', {{ className: 'checkbox-label', key: 'label' }}, props.label),
                props.description && h('div', {{ className: 'checkbox-desc', key: 'desc' }}, props.description)
            ])
        ]),
        Slider: ({{ props }}) => h('div', {{ className: 'slider-container' }}, [
            h('label', {{ className: 'slider-label', key: 'label' }}, props.label),
            h('input', {{ type: 'range', className: 'slider', min: props.min || 0, max: props.max || 100, step: props.step || 1, key: 'input' }})
        ]),
        Tabs: ({{ props, children, setActiveTab, activeTab }}) => {{
            const tabs = children.filter(c => c && c.props && c.props.type === 'Tab');
            const current = activeTab || props.default || (tabs[0]?.props?.props?.tabKey);
            return h('div', null, [
                h('div', {{ className: 'tabs', key: 'tabs' }}, tabs.map(t =>
                    h('div', {{
                        className: 'tab ' + (t.props.props.tabKey === current ? 'active' : ''),
                        key: t.props.props.tabKey,
                        onClick: () => setActiveTab(t.props.props.tabKey)
                    }}, t.props.props.label)
                )),
                tabs.find(t => t.props.props.tabKey === current)
            ]);
        }},
        Tab: ({{ props, children }}) => h('div', null, children),
        // Charts using Chart.js - match Python component types and props
        LineChart: ({{ props }}) => {{
            const data = props.data || [];
            const yKeys = props.yFields || [];
            const xField = props.xField;
            const chartData = {{
                labels: data.map(d => d[xField]),
                datasets: yKeys.map((k, i) => ({{
                    label: k,
                    data: data.map(d => d[k]),
                    borderColor: COLORS[i % COLORS.length],
                    backgroundColor: props.area ? COLORS[i % COLORS.length] + '40' : 'transparent',
                    fill: props.area,
                    tension: props.smooth ? 0.4 : 0
                }}))
            }};
            return h(ChartComponent, {{ type: 'line', data: chartData, height: props.height }});
        }},
        BarChart: ({{ props }}) => {{
            const data = props.data || [];
            const yKeys = props.yFields || [];
            const xField = props.xField;
            const chartData = {{
                labels: data.map(d => d[xField]),
                datasets: yKeys.map((k, i) => ({{
                    label: k,
                    data: data.map(d => d[k]),
                    backgroundColor: COLORS[i % COLORS.length]
                }}))
            }};
            return h(ChartComponent, {{ type: 'bar', data: chartData, height: props.height, options: {{ indexAxis: props.horizontal ? 'y' : 'x' }} }});
        }},
        PieChart: ({{ props }}) => {{
            const data = props.data || [];
            const chartData = {{
                labels: data.map(d => d[props.nameField]),
                datasets: [{{
                    data: data.map(d => d[props.valueField]),
                    backgroundColor: COLORS.slice(0, data.length)
                }}]
            }};
            return h(ChartComponent, {{ type: props.donut ? 'doughnut' : 'pie', data: chartData, height: props.height }});
        }},
        AreaChart: ({{ props }}) => {{
            const data = props.data || [];
            const yKeys = props.yFields || [];
            const xField = props.xField;
            const chartData = {{
                labels: data.map(d => d[xField]),
                datasets: yKeys.map((k, i) => ({{
                    label: k,
                    data: data.map(d => d[k]),
                    borderColor: COLORS[i % COLORS.length],
                    backgroundColor: COLORS[i % COLORS.length] + '40',
                    fill: true,
                    tension: 0.4
                }}))
            }};
            return h(ChartComponent, {{ type: 'line', data: chartData, height: props.height }});
        }},
        GaugeChart: ({{ props }}) => {{
            const pct = (props.value / (props.maxValue || 100)) * 100;
            const angle = (pct / 100) * 180;
            return h('div', {{ className: 'gauge-container' }}, [
                h('svg', {{ className: 'gauge-svg', viewBox: '0 0 120 80', key: 'svg' }}, [
                    h('defs', {{ key: 'defs' }}, h('linearGradient', {{ id: 'gaugeGradient2', x1: '0%', y1: '0%', x2: '100%', y2: '0%' }}, [
                        h('stop', {{ offset: '0%', stopColor: 'var(--gradient-start)', key: 's1' }}),
                        h('stop', {{ offset: '100%', stopColor: 'var(--gradient-end)', key: 's2' }})
                    ])),
                    h('path', {{ d: 'M10 70 A50 50 0 0 1 110 70', fill: 'none', stroke: 'var(--bg-tertiary)', strokeWidth: 12, strokeLinecap: 'round', key: 'bg' }}),
                    h('path', {{ d: 'M10 70 A50 50 0 0 1 110 70', fill: 'none', stroke: 'url(#gaugeGradient2)', strokeWidth: 12, strokeLinecap: 'round', strokeDasharray: ((angle / 180) * 157) + ' 157', key: 'fill' }})
                ]),
                h('div', {{ className: 'gauge-value', key: 'value' }}, props.format ? props.format.replace('{{value}}', props.value) : props.value + '%'),
                props.title && h('div', {{ className: 'gauge-title', key: 'title' }}, props.title)
            ]);
        }},
        ScatterChart: ({{ props }}) => {{
            const data = props.data || [];
            const chartData = {{
                datasets: [{{
                    label: 'Data',
                    data: data.map(d => ({{ x: d[props.xField], y: d[props.yField] }})),
                    backgroundColor: COLORS[0]
                }}]
            }};
            return h(ChartComponent, {{ type: 'scatter', data: chartData, height: props.height }});
        }},
        HeatmapChart: ({{ props }}) => h('div', {{ className: 'chart-placeholder' }}, '[Heatmap: Coming soon]'),
        FunnelChart: ({{ props }}) => {{
            const data = props.data || [];
            const chartData = {{
                labels: data.map(d => d[props.nameField]),
                datasets: [{{
                    data: data.map(d => d[props.valueField]),
                    backgroundColor: COLORS.slice(0, data.length)
                }}]
            }};
            return h(ChartComponent, {{ type: 'bar', data: chartData, height: props.height, options: {{ indexAxis: 'y' }} }});
        }},
        RadarChart: ({{ props }}) => {{
            const data = props.data || [];
            const valueFields = props.valueFields || [];
            const chartData = {{
                labels: data.map(d => d[props.categoryField]),
                datasets: valueFields.map((k, i) => ({{
                    label: k,
                    data: data.map(d => d[k]),
                    borderColor: COLORS[i % COLORS.length],
                    backgroundColor: COLORS[i % COLORS.length] + '40',
                    fill: props.fill
                }}))
            }};
            return h(ChartComponent, {{ type: 'radar', data: chartData, height: props.height }});
        }},
        TreemapChart: ({{ props }}) => h('div', {{ className: 'chart-placeholder' }}, '[Treemap: Coming soon]')
    }};

    function normalizeChartData(data) {{
        if (!data) return [];
        if (Array.isArray(data)) return data;
        const keys = Object.keys(data);
        if (keys.length === 0) return [];
        const len = data[keys[0]]?.length || 0;
        return Array.from({{ length: len }}, (_, i) => keys.reduce((obj, k) => ({{ ...obj, [k]: data[k][i] }}), {{}}));
    }}

    function formatValue(v) {{
        if (v === null || v === undefined) return '-';
        if (typeof v === 'number') return v.toLocaleString();
        return String(v);
    }}

    function renderComponent(comp, key, setActiveTab, activeTab) {{
        if (!comp || !comp.type) return null;
        const Renderer = renderers[comp.type];
        if (!Renderer) {{
            console.warn('Unknown component type:', comp.type);
            return h('div', {{ key, style: {{ color: 'var(--warning)', fontSize: '0.875rem' }} }}, '[' + comp.type + ']');
        }}
        const children = (comp.children || []).map((c, i) => renderComponent(c, i, setActiveTab, activeTab));
        return h(Renderer, {{ props: comp.props || {{}}, children, key, setActiveTab, activeTab, type: comp.type }});
    }}

    function Dashboard() {{
        const [pages, setPages] = useState(null);
        const [currentPage, setCurrentPage] = useState('/');
        const [activeTab, setActiveTab] = useState(null);
        const [error, setError] = useState(null);

        useEffect(() => {{
            fetch('/api/pages')
                .then(r => r.json())
                .then(data => setPages(data))
                .catch(e => setError(e.message));
        }}, []);

        if (error) return h('div', {{ className: 'loading', style: {{ color: 'var(--danger)' }} }}, 'Error: ' + error);
        if (!pages) return h('div', {{ className: 'loading' }}, 'Loading...');

        const pageData = pages.pages || {{}};
        const components = pageData[currentPage] || [];

        const sidebarIdx = components.findIndex(c => c.type === 'Sidebar');
        const sidebar = sidebarIdx >= 0 ? components[sidebarIdx] : null;
        const mainComponents = sidebarIdx >= 0 ? [...components.slice(0, sidebarIdx), ...components.slice(sidebarIdx + 1)] : components;

        return h('div', {{ className: 'app-container' }}, [
            h('div', {{ className: 'main-content', key: 'main' }}, mainComponents.map((c, i) => renderComponent(c, i, setActiveTab, activeTab))),
            sidebar && h('div', {{ className: 'sidebar', key: 'sidebar' }}, (sidebar.children || []).map((c, i) => renderComponent(c, i, setActiveTab, activeTab)))
        ]);
    }}

    ReactDOM.createRoot(document.getElementById('root')).render(h(Dashboard));
    </script>
</body>
</html>'''
