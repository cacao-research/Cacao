![image](https://github.com/user-attachments/assets/830a00ca-7948-42ff-9196-adb58357c536)

# Cacao

[![PyPI Version](https://img.shields.io/pypi/v/cacao)](https://pypi.org/project/cacao/)
[![Downloads](https://static.pepy.tech/badge/cacao)](https://pepy.tech/project/cacao)
[![Python Versions](https://img.shields.io/pypi/pyversions/cacao)](https://pypi.org/project/cacao/)
[![License](https://img.shields.io/pypi/l/cacao)](https://github.com/jhd3197/Cacao/blob/main/LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/jhd3197/Cacao/publish.yml?branch=main)](https://github.com/jhd3197/Cacao/actions)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/Cacao?style=social)](https://github.com/jhd3197/Cacao)

---

**High-performance reactive web framework for Python.** Build dashboards, internal tools, and data apps with a simple API — 10x faster than Streamlit with true WebSocket reactivity.

> **v2.0** - Complete rewrite with signal-based reactivity, session-scoped state, and a Streamlit-like API that doesn't re-run your entire script.

## Quick Start

```bash
pip install cacao
```

### Hello World (4 lines)

```python
import cacao as c

c.title("Hello, Cacao!")
c.text("Welcome to the simplest Python web framework")
```

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

Run with:
```bash
cacao run dashboard.py
```

## Why Cacao?

| Feature | Cacao | Streamlit |
|---------|-------|-----------|
| **Reactivity** | Signal-based (only changed values update) | Full script re-run on every interaction |
| **State** | Session-scoped by design | `st.session_state` bolt-on |
| **Updates** | WebSocket streaming (instant) | HTTP polling (laggy) |
| **Multi-user** | Isolated sessions built-in | Shared state issues |
| **API** | Context managers + decorators | Magic globals |

## Core Concepts

### Signals (Reactive State)

```python
count = c.signal(0, name="count")

# Get value for a session
current = count.get(session)

# Set value (auto-syncs to client)
count.set(session, current + 1)
```

### Event Handlers

```python
@c.on("submit")
async def handle_submit(session, event):
    print(event.get("value"))
```

### Layout Components

```python
with c.row():           # Horizontal layout
    with c.col(span=8): # 8/12 width column
        c.text("Main content")
    with c.col(span=4): # 4/12 width column
        c.text("Sidebar")

with c.card("Title"):   # Card container
    c.metric("Value", 100)

with c.tabs():          # Tabbed content
    with c.tab("tab1", "First"):
        c.text("Tab 1 content")
    with c.tab("tab2", "Second"):
        c.text("Tab 2 content")
```

### Form Components

```python
c.button("Click me", on_click="submit")
c.input("Name", signal=name_signal)
c.select("Category", ["A", "B", "C"])
c.checkbox("Agree", signal=agree_signal)
c.slider("Volume", min=0, max=100)
```

### Charts

```python
c.line(data, x="date", y="value")
c.bar(data, x="category", y="count")
c.pie(data, values="amount", names="label")
c.area(data, x="date", y="value")
c.scatter(data, x="x", y="y")
c.gauge(value=75, max_value=100)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PYTHON SERVER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Signals  │  │ Sessions │  │  Events  │  │ WebSocket/HTTP│   │
│  │ (state)  │──│ (per-    │──│ (typed   │──│    Server     │   │
│  │          │  │  client) │  │  async)  │  │               │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────┬───────┘   │
└────────────────────────────────────────────────────┼───────────┘
                                                     │ JSON
                                                     │ WebSocket
┌────────────────────────────────────────────────────┼───────────┐
│                      REACT CLIENT                   │           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┴──────┐    │
│  │  Hooks   │  │Components│  │  Event   │  │   State     │    │
│  │useCacao()│──│ (your UI)│──│Dispatcher│──│   Store     │    │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
cacao/
├── __init__.py          # Simple API exports
├── simple.py            # Streamlit-like API
├── server/              # Core server
│   ├── app.py           # App class
│   ├── signal.py        # Signal, Computed
│   ├── session.py       # Session management
│   ├── events.py        # Event handling
│   ├── server.py        # WebSocket server
│   ├── ui.py            # UI components
│   ├── chart.py         # Chart components
│   └── data.py          # Data utilities
├── cli/                 # CLI commands
└── examples/            # Example apps
```

## CLI

```bash
# Run an app with hot reload
cacao run app.py

# Run on custom port
cacao run app.py --port 3000

# Create a new project
cacao create my-dashboard

# Build a static site (no server required)
cacao build app.py

# Build for GitHub Pages subdirectory
cacao build app.py --base-path /my-repo
```

## Static Builds

Cacao can generate static sites that run entirely in the browser — no Python server required. Perfect for GitHub Pages, Netlify, or any static hosting.

```bash
cacao build app.py
```

This creates a `dist/` folder with:
- `index.html` - Your app
- `cacao.js` - Runtime with built-in handlers
- `cacao.css` - Styles

**Built-in handlers** for common operations work automatically:
- Encoders: Base64, URL, HTML entities, JWT decode
- Generators: UUID, passwords, Lorem Ipsum
- Converters: JSON/YAML, case conversion, number bases
- Text: Statistics, regex testing
- Crypto: Hash generation, HMAC

Deploy to GitHub Pages:
```yaml
# .github/workflows/deploy.yml
- run: pip install cacao
- run: cacao build app.py --base-path /${{ github.event.repository.name }}
```

See [cacao-tools](https://github.com/cacao-research/cacao-tools) for a full static site example.

## Examples

See the `examples/` directory:
- `examples/simple/hello.py` - Minimal app
- `examples/simple/counter.py` - Interactive counter
- `examples/simple/metrics.py` - KPI dashboard
- `examples/simple/dashboard.py` - Full dashboard with charts

## Contributing

Contributions are welcome! Please read our contributing guidelines for details.

## License

MIT
