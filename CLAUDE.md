# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Cacao is a high-performance reactive web framework for Python that enables building interactive dashboards, internal tools, and data applications. It uses WebSocket-driven real-time updates and a fluent Python API that generates JSON UI definitions.

## Project Structure

```
cacao/
├── frontend/           # Frontend assets (Node.js for devs only)
│   ├── src/
│   │   ├── styles/     # Modular LESS files
│   │   │   ├── variables.less
│   │   │   ├── mixins.less
│   │   │   ├── base.less
│   │   │   ├── layouts.less
│   │   │   ├── themes/
│   │   │   └── components/
│   │   ├── components/ # React components (render JSON → UI)
│   │   │   ├── core/       # constants, utils, websocket, static-runtime
│   │   │   ├── layout/     # Row, Col, Grid, AppShell, NavSidebar
│   │   │   ├── display/    # Card, Metric, Table, Alert, Progress
│   │   │   ├── typography/ # Title, Text, Code, Divider
│   │   │   ├── form/       # Button, Input, Select, Slider, Tabs
│   │   │   └── charts/     # LineChart, BarChart, PieChart, etc.
│   │   └── handlers/   # Built-in JS handlers for static builds
│   │       ├── encoders.js   # base64, url, html, jwt
│   │       ├── generators.js # uuid, password, lorem
│   │       ├── converters.js # yaml, case, number base
│   │       ├── text.js       # stats, regex
│   │       └── crypto.js     # hash, hmac
│   ├── dist/           # Build output (gitignored)
│   ├── build.js        # Build script
│   └── package.json    # Node dependencies (less, esbuild)
├── server/             # WebSocket server (Starlette)
│   ├── ui.py           # Python component definitions
│   ├── server.py       # HTTP + WebSocket server
│   └── signal.py       # Reactive state management
├── simple.py           # Simple API (import cacao as c)
├── cli/                # CLI commands (run, build, create)
└── examples/           # Example apps
```

## Common Commands

### Frontend Build (developers only)
```bash
cd cacao/frontend
npm install
npm run build
```

### Running Apps
```bash
cacao run app.py                    # Run with hot reload
cacao run app.py --port 8080        # Custom port
cacao run app.py --no-reload        # No hot reload
```

### Static Build (for GitHub Pages, no server needed)
```bash
cacao build app.py                  # Build to dist/
cacao build app.py --base-path /repo  # For GitHub Pages subdirectory
python -m http.server -d dist       # Preview locally
```

## Architecture

### Server
- Starlette-based HTTP + WebSocket server (`server/server.py`)
- Serves frontend from `frontend/dist/`
- WebSocket endpoint at `/ws` for real-time state sync

### Frontend
- React components rendered from JSON definitions
- LESS compiled to `dist/cacao.css`
- JS bundled with esbuild to `dist/cacao.js`
- External dependencies: React, ReactDOM, Chart.js (loaded from CDN)

### Data Flow
```
Python fluent API → JSON UI definition → WebSocket → React renders
         ↑                                              ↓
    Signal.set() ←── Event handler ←── Client action
```

## Code Conventions

- Type hints required for all Python code
- Google-style docstrings
- Frontend source in `src/`, compiled output in `dist/`
- Components organized by category (layout, display, form, charts)

## Adding New Components

When creating new components, use the `cacao-component` skill which provides step-by-step guidance. Components require changes across multiple files:

1. **Python API** (`server/ui.py`) - Component function with type hints
2. **Simple API** (`simple.py`) - Wrapper that calls `_ensure_context()`
3. **React Component** (`frontend/src/components/{category}/`) - JS component
4. **LESS Styles** (`frontend/src/styles/components/`) - Component styles
5. **Handlers** (`frontend/src/handlers/`) - For static build event handling
6. **Exports** - Add to `index.js` files and `__all__` lists

After changes: `cd frontend && npm run build`

## Static Build System

Cacao supports static builds for serverless deployment (GitHub Pages, etc.):

- **Handlers are built-in**: All common operations (base64, hash, uuid, etc.) are bundled into `cacao.js`
- **No Node.js for users**: Only framework developers need Node.js
- **URL routing**: Hash-based routing (`#/page`) for SPA on static hosts

## Windows Development

Use semicolon (`;`) to separate PowerShell commands, not `&&`.
