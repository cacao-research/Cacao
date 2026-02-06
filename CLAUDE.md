# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Cacao is a high-performance reactive web framework for Python that enables building interactive dashboards, internal tools, and data applications. It uses WebSocket-driven real-time updates and a fluent Python API that generates JSON UI definitions.

## Project Structure

```
cacao/
├── frontend/           # Frontend assets
│   ├── src/
│   │   ├── styles/     # Modular LESS files
│   │   │   ├── variables.less
│   │   │   ├── mixins.less
│   │   │   ├── base.less
│   │   │   ├── layouts.less
│   │   │   ├── themes/
│   │   │   └── components/
│   │   └── components/ # Modular JS components
│   │       ├── core/       # constants, utils, ChartWrapper
│   │       ├── layout/     # Row, Col, Grid, Sidebar
│   │       ├── display/    # Card, Metric, Table, Alert, Progress, Gauge
│   │       ├── typography/ # Title, Text, Spacer, Divider
│   │       ├── form/       # Button, Select, Checkbox, Slider, Tabs
│   │       └── charts/     # LineChart, BarChart, PieChart, etc.
│   ├── dist/           # Build output (gitignored)
│   ├── build.js        # Build script
│   └── package.json    # Node dependencies (less, esbuild)
├── server/             # WebSocket server (Starlette)
├── client/             # Client-side utilities
├── cli/                # CLI commands
└── examples/           # Example apps
```

## Common Commands

### Frontend Build
```bash
cd cacao/frontend
npm install
npm run build
```

### Running Examples
```bash
cacao run cacao/examples/dashboard.py --port 8080
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

## Windows Development

Use semicolon (`;`) to separate PowerShell commands, not `&&`.
