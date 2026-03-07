<div align="center">

![image](https://github.com/user-attachments/assets/830a00ca-7948-42ff-9196-adb58357c536)

# Cacao

**High-performance reactive web framework for Python.**

Build dashboards, internal tools, and data apps with a simple API — real WebSocket reactivity, not full-page reruns.

[![PyPI Version](https://img.shields.io/pypi/v/cacao?style=flat-square&color=f5c542)](https://pypi.org/project/cacao/)
[![Downloads](https://img.shields.io/pypi/dm/cacao?style=flat-square&color=green)](https://pepy.tech/project/cacao)
[![Python](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/cacao/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/cacao-research/Cacao/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/cacao-research/Cacao/ci.yml?branch=dev&style=flat-square&label=CI)](https://github.com/cacao-research/Cacao/actions/workflows/ci.yml)
[![GitHub Pages](https://img.shields.io/github/actions/workflow/status/cacao-research/Cacao/pages.yml?branch=main&style=flat-square&label=showcase)](https://github.com/cacao-research/Cacao/actions/workflows/pages.yml)

![React](https://img.shields.io/badge/React-18-61DAFB.svg?style=flat-square&logo=react&logoColor=black)
![WebSocket](https://img.shields.io/badge/WebSocket-realtime-8B5CF6.svg?style=flat-square)
![Starlette](https://img.shields.io/badge/Starlette-ASGI-009688.svg?style=flat-square)
[![GitHub Stars](https://img.shields.io/github/stars/cacao-research/Cacao?style=flat-square&color=f5c542)](https://github.com/cacao-research/Cacao/stargazers)

<br>

[Features](#-features) · [Quick Start](#-quick-start) · [Examples](#-examples) · [Components](#-components) · [Architecture](#-architecture) · [Static Builds](#-static-builds) · [Contributing](#-contributing)

</div>

---

> **v2.0** — Complete rewrite with signal-based reactivity, session-scoped state, plugin hooks, and a Streamlit-like API that doesn't re-run your entire script.

## Quick Start

```bash
pip install cacao
```

```python
import cacao as c

c.title("Hello, Cacao!")
c.text("Welcome to the simplest Python web framework")
```

```bash
cacao run app.py
```

That's it — 3 lines of Python and you have a live web app with hot reload.

---

## Why Cacao?

| Feature | Cacao | Streamlit |
|---------|-------|-----------|
| **Reactivity** | Signal-based (only changed values update) | Full script re-run on every interaction |
| **State** | Session-scoped by design | `st.session_state` bolt-on |
| **Updates** | WebSocket streaming (instant) | HTTP polling (laggy) |
| **Multi-user** | Isolated sessions built-in | Shared state issues |
| **API** | Context managers + decorators | Magic globals |
| **Static export** | `cacao build` — no server needed | Not supported |

---

## Features

### Reactive Signals

```python
count = c.signal(0, name="count")

@c.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + 1)
```

Signals are the core of Cacao. When a value changes, only the affected components update — no full-page reruns, no diffing your entire tree.

### 60+ Built-in Components

Layouts, forms, charts, display elements, navigation — everything you need out of the box.

### Multi-Page Apps

```python
with c.page("/"):
    c.title("Home")

with c.page("/settings"):
    c.title("Settings")
```

Hash-based routing works both in server mode and static builds.

### Static Builds

```bash
cacao build app.py
```

Export your app to a static site (HTML + JS + CSS) that runs entirely in the browser. Deploy to GitHub Pages, Netlify, or any static host — no Python server required.

### Plugin Hooks & Auth

Extensible architecture with plugin registration, authentication hooks, and notification toasts.

### Dark & Light Themes

```python
c.config(theme="dark")  # or "light"
```

---

## Examples

### Interactive Counter

```python
import cacao as c

c.config(title="Counter")
count = c.signal(0, name="count")

@c.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + 1)

@c.on("decrement")
async def decrement(session, event):
    count.set(session, count.get(session) - 1)

c.title("Counter")

with c.card():
    c.metric("Count", count)
    with c.row():
        c.button("-", on_click="decrement", variant="secondary")
        c.button("+", on_click="increment")
```

### Dashboard with Charts

```python
import cacao as c

c.config(title="Sales Dashboard", theme="dark")
sales = c.sample_sales_data()

c.title("Sales Dashboard")

with c.row():
    c.metric("Revenue", "$45,231", trend="+20.1%", trend_direction="up")
    c.metric("Orders", "1,247", trend="+12.5%", trend_direction="up")
    c.metric("Customers", "842", trend="+5.3%", trend_direction="up")

with c.row():
    with c.col(span=8):
        with c.card("Revenue Trend"):
            c.line(sales, x="date", y="revenue", area=True)
    with c.col(span=4):
        with c.card("By Category"):
            c.pie(sales[:5], values="revenue", names="category", donut=True)

with c.card("Recent Transactions"):
    c.table(sales[:10], columns=["date", "category", "revenue", "orders"])
```

More examples in the [`examples/`](examples/) directory:

| Example | Description |
|---------|-------------|
| [`simple/hello.py`](examples/simple/hello.py) | Minimal hello world |
| [`simple/counter.py`](examples/simple/counter.py) | Interactive counter with signals |
| [`simple/metrics.py`](examples/simple/metrics.py) | KPI dashboard |
| [`simple/dashboard.py`](examples/simple/dashboard.py) | Full dashboard with charts |
| [`chat/app.py`](examples/chat/app.py) | Chat application |
| [`todo/server.py`](examples/todo/server.py) | Todo list app |
| [`analytics_dashboard/`](examples/analytics_dashboard/) | Analytics dashboard |

---

## Components

### Layout

| Component | Description |
|-----------|-------------|
| `row()` | Horizontal flex layout |
| `col(span=N)` | Column with 12-grid span |
| `grid()` | CSS grid layout |
| `container()` | Centered container |
| `stack()` | Vertical stack |
| `split()` | Side-by-side split |
| `hero()` | Hero section |
| `card()` | Card container |
| `tabs()` / `tab()` | Tabbed content |
| `accordion()` | Collapsible sections |
| `modal()` | Modal dialog |
| `panel()` | Sliding panel |
| `app_shell()` | Full app layout with sidebar |

### Display

| Component | Description |
|-----------|-------------|
| `title()` / `text()` | Typography |
| `markdown()` | Markdown with optional TOC |
| `code()` | Syntax-highlighted code |
| `metric()` | KPI metric with trend |
| `table()` | Data table |
| `json_view()` | Interactive JSON viewer |
| `badge()` / `alert()` | Status indicators |
| `progress()` | Progress bar |
| `image()` / `video()` | Media |
| `timeline()` | Timeline display |
| `diff()` | Side-by-side diff viewer |
| `breadcrumb()` | Navigation breadcrumb |

### Form

| Component | Description |
|-----------|-------------|
| `button()` | Button with variants |
| `input_field()` | Text input |
| `textarea()` | Multi-line input |
| `select()` | Dropdown select |
| `checkbox()` / `switch()` | Toggle inputs |
| `slider()` | Range slider |
| `date_picker()` | Date picker |
| `search_input()` | Search with suggestions |
| `file_upload()` | File upload |
| `chat()` | Chat input interface |

### Charts

| Component | Description |
|-----------|-------------|
| `line()` / `area()` | Line and area charts |
| `bar()` | Bar chart |
| `pie()` / `donut()` | Pie and donut charts |
| `scatter()` | Scatter plot |
| `gauge()` | Gauge meter |
| `heatmap()` | Heatmap |
| `radar()` | Radar chart |
| `funnel()` | Funnel chart |
| `treemap()` | Treemap |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PYTHON SERVER                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Signals  │  │ Sessions │  │  Events  │  │ WebSocket/HTTP│  │
│  │ (state)  │──│ (per-    │──│ (typed   │──│    Server     │  │
│  │          │  │  client) │  │  async)  │  │  (Starlette)  │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────┬───────┘  │
└────────────────────────────────────────────────────┼───────────┘
                                                     │ JSON
                                                     │ WebSocket
┌────────────────────────────────────────────────────┼───────────┐
│                      REACT CLIENT                  │           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┴──────┐   │
│  │  Hooks   │  │Components│  │  Event   │  │   State     │   │
│  │useCacao()│──│ (60+ UI) │──│Dispatcher│──│   Store     │   │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Data flow:**
```
Python API → JSON definition → WebSocket → React renders
     ↑                                         ↓
Signal.set() ←── Event handler ←── User action
```

---

## CLI

```bash
cacao run app.py                     # Run with hot reload
cacao run app.py --port 3000         # Custom port
cacao run app.py --no-reload         # Disable hot reload
cacao create my-dashboard            # Scaffold a new project
cacao build app.py                   # Build static site
cacao build app.py --base-path /repo # For GitHub Pages subdirectory
```

---

## Static Builds

Cacao generates static sites that run entirely in the browser — no Python server required.

```bash
cacao build app.py
```

Output:
```
dist/
├── index.html    # Your app
├── cacao.js      # Runtime + built-in handlers
└── cacao.css     # Styles
```

**Built-in client-side handlers** for common operations:
- **Encoders** — Base64, URL, HTML entities, JWT decode
- **Generators** — UUID, passwords, Lorem Ipsum
- **Converters** — JSON/YAML, case conversion, number bases
- **Text** — Statistics, regex testing
- **Crypto** — Hash generation, HMAC

Deploy to GitHub Pages:
```yaml
# .github/workflows/deploy.yml
- run: pip install cacao
- run: cacao build app.py --base-path /${{ github.event.repository.name }}
```

See [cacao-tools](https://github.com/cacao-research/cacao-tools) for a full static site example.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, Starlette, Uvicorn, WebSocket |
| Frontend | React 18, Chart.js, LESS |
| Build | esbuild, hatchling |
| State | Signal-based reactivity with session scoping |
| Deployment | Static export, GitHub Pages, any ASGI server |

---

## Project Structure

```
cacao/
├── __init__.py          # Package exports
├── simple.py            # Streamlit-like API (import cacao as c)
├── server/              # Core server
│   ├── ui.py            # 60+ UI components
│   ├── chart.py         # Chart components
│   ├── signal.py        # Signal & Computed reactivity
│   ├── session.py       # Session management
│   ├── events.py        # Event handling
│   ├── server.py        # HTTP + WebSocket server
│   └── data.py          # Data utilities
├── cli/                 # CLI (run, build, create)
├── frontend/            # Frontend source (devs only)
│   ├── src/components/  # React components
│   ├── src/styles/      # LESS styles
│   ├── src/handlers/    # Static build handlers
│   └── dist/            # Build output
└── examples/            # Example apps
```

---

## Contributing

Contributions are welcome! See the repo issues for ideas.

```
fork → feature branch → commit → push → pull request
```

---

<div align="center">

**Cacao** — Reactive Python UIs, made simple.

[Report Bug](https://github.com/cacao-research/Cacao/issues) · [Request Feature](https://github.com/cacao-research/Cacao/issues)

Made with care by [Juan Denis](https://juandenis.com)

</div>
