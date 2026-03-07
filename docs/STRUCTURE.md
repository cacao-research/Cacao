# Cacao App Structure Guide

Cacao supports two project patterns: **simple** (single file) and **structured** (multi-file). Pick whichever fits your app's complexity.

## Simple (Single File)

Best for: small tools, demos, prototypes, scripts under ~200 lines.

```
my-app/
├── app.py
└── requirements.txt
```

```python
# app.py
import cacao as c

c.config(title="My Tool")

name = c.signal("", name="name")

with c.page("/"):
    c.title("Greeter")
    c.input("Name", signal=name, on_change="greet")
    c.text("Hello!", signal=name)

@c.on("greet")
async def handle_greet(session, event):
    pass  # signal updates automatically
```

Everything in one file. No imports, no folders. Run with `cacao run app.py`.

Create with:
```bash
cacao create my-app --template minimal
```

---

## Structured (Multi-File)

Best for: dashboards, documentation sites, multi-page apps, anything with data files or shared components.

```
my-app/
├── app.py                 # Entry point: config + imports
├── pages/                 # One file per page
│   ├── __init__.py
│   ├── home.py
│   ├── dashboard.py
│   └── settings.py
├── components/            # Reusable UI blocks
│   ├── __init__.py
│   ├── header.py
│   └── sidebar.py
├── handlers/              # Event handlers
│   ├── __init__.py
│   └── events.py
├── data/                  # Data files (JSON, CSV, etc.)
│   └── config.json
└── requirements.txt
```

Create with:
```bash
cacao create my-app --template structured
```

### How it works

**`app.py`** is the entry point. It configures the app with `c.config()` and imports everything:

```python
# app.py
import cacao as c

c.config(title="My Dashboard", theme="dark")

# Import pages — each page registers itself with c.page()
from pages import home, dashboard, settings  # noqa: F401

# Import handlers — each handler registers itself with @c.on()
from handlers import events  # noqa: F401
```

**`pages/`** — each file defines one page using `with c.page(path)`:

```python
# pages/dashboard.py
import cacao as c
from components.sidebar import render_filters

with c.page("/dashboard"):
    c.title("Dashboard")

    with c.row():
        c.metric("Users", 1234)
        c.metric("Revenue", "$56K")

    render_filters()
```

**`components/`** — reusable UI functions called from pages:

```python
# components/sidebar.py
import cacao as c

def render_filters():
    """Render filter controls."""
    with c.card("Filters"):
        c.select("Period", options=["7d", "30d", "90d"])
        c.select("Region", options=["All", "US", "EU"])
```

**`handlers/`** — event handlers grouped by feature:

```python
# handlers/events.py
import cacao as c
from cacao.server.session import Session

@c.on("apply_filters")
async def handle_filters(session: Session, event: dict) -> None:
    # update signals based on filter selection
    pass
```

**`data/`** — external data files instead of inline blobs:

```python
# pages/docs.py
import json
from pathlib import Path
import cacao as c

_data = json.loads((Path(__file__).parent.parent / "data" / "docs.json").read_text())

with c.page("/docs"):
    for item in _data["modules"]:
        c.text(item["name"])
```

### Key Rules

1. **`app.py` is always the entry point.** It calls `c.config()` and imports pages/handlers. Run with `cacao run app.py`.

2. **Pages register themselves.** Each page file uses `with c.page("/path")` at module level. Importing the file is enough to register it.

3. **Handlers register themselves.** Each handler uses `@c.on("event")` at module level. Importing the file registers it.

4. **Components are plain functions.** They take arguments and call `c.*` functions. No registration needed — just import and call.

5. **Data lives in `data/`.** Never inline large JSON/CSV in Python files. Load from `data/` using `json.load()` or similar.

6. **One concern per file.** A page file defines layout. A handler file defines logic. A component file defines reusable UI. Don't mix.

---

## When to Use Which

| Scenario | Pattern |
|---|---|
| Quick prototype or demo | Simple |
| Single-page tool | Simple |
| Under ~200 lines of UI | Simple |
| Multi-page app | Structured |
| App with data files | Structured |
| Team project | Structured |
| Generated docs site | Structured |
| App with chat/AI features | Structured |

---

## For Code Generators (AI / CacaoDocs)

If you're generating Cacao apps programmatically:

1. **Always use the structured pattern** for non-trivial apps
2. **Write data to `data/*.json`**, never inline as Python string literals
3. **One page per file** in `pages/` — name files after the page slug
4. **Group handlers** by feature in `handlers/`
5. **Extract repeated UI** into `components/`
6. **Keep `app.py` minimal** — only config and imports

Example generator output for a docs site:

```
docs-app/
├── app.py                    # c.config() + imports
├── data/
│   └── docs.json             # Extracted documentation data
├── pages/
│   ├── __init__.py
│   ├── overview.py           # Overview/stats panel
│   ├── modules.py            # Module listing
│   ├── classes.py            # Class details
│   ├── functions.py          # Function details
│   └── chat.py               # AI chat panel
├── components/
│   ├── __init__.py
│   ├── docstring.py          # Renders docstring blocks
│   └── source_view.py        # Source code viewer
├── handlers/
│   ├── __init__.py
│   └── chat.py               # Chat event handlers
└── requirements.txt
```
