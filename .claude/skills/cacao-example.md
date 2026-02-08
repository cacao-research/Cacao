---
name: cacao-example
description: Create example applications for Cacao. Use when building demo apps, test cases, or showcasing features. Provides templates for common app patterns like tools, dashboards, forms, and admin panels.
---

# Cacao Example Apps

Examples demonstrate features and serve as test cases. They live in `cacao/examples/` or as standalone projects like `cacao-tools/`.

## Quick Start Templates

### Minimal App

```python
"""Minimal Cacao app."""
import cacao as c

c.config(title="My App", theme="dark")

c.title("Hello World")
c.text("Welcome to Cacao!")
```

### Counter (Signals + Events)

```python
"""Counter demonstrating signals and events."""
import cacao as c

c.config(title="Counter")

count = c.signal(0, name="count")

@c.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + 1)

@c.on("decrement")
async def decrement(session, event):
    count.set(session, count.get(session) - 1)

with c.card("Counter"):
    c.metric("Count", count)
    with c.row():
        c.button("-", on_click="decrement", variant="outline")
        c.button("+", on_click="increment")
```

### Form with Validation

```python
"""Form with input handling."""
import cacao as c

c.config(title="Contact Form")

name = c.signal("", name="name")
email = c.signal("", name="email")
message = c.signal("", name="message")
status = c.signal("", name="status")

@c.on("submit_form")
async def submit(session, event):
    n = name.get(session)
    e = email.get(session)
    m = message.get(session)

    if not n or not e or not m:
        status.set(session, "Please fill all fields")
        return

    # Process form...
    status.set(session, f"Thanks {n}! We'll contact you at {e}")

with c.card("Contact Us"):
    c.input("Name", signal=name, placeholder="Your name")
    c.input("Email", signal=email, placeholder="you@example.com")
    c.textarea(label="Message", signal=message, placeholder="Your message...")
    c.spacer()
    c.button("Submit", on_click="submit_form")
    c.text(status, color="muted")
```

### Dashboard with Metrics

```python
"""Dashboard with KPIs and charts."""
import cacao as c

c.config(title="Sales Dashboard", theme="dark")

# Sample data
sales_data = [
    {"month": "Jan", "revenue": 4500, "orders": 120},
    {"month": "Feb", "revenue": 5200, "orders": 145},
    {"month": "Mar", "revenue": 4800, "orders": 132},
    {"month": "Apr", "revenue": 6100, "orders": 178},
]

c.title("Sales Dashboard")

# Metrics row
with c.row():
    c.metric("Revenue", "$20,600", trend="+15%", trend_direction="up")
    c.metric("Orders", "575", trend="+12%", trend_direction="up")
    c.metric("Avg Order", "$35.83", trend="-2%", trend_direction="down")

c.spacer()

# Charts
with c.row():
    with c.col(span=8):
        with c.card("Revenue Trend"):
            c.line(sales_data, x="month", y="revenue")
    with c.col(span=4):
        with c.card("Orders by Month"):
            c.bar(sales_data, x="month", y="orders")
```

### Admin Panel (AppShell)

```python
"""Admin panel with sidebar navigation."""
import cacao as c

c.config(title="Admin Panel", theme="dark")

with c.app_shell(brand="Admin", default="dashboard"):
    with c.nav_sidebar():
        with c.nav_group("Main", icon="home"):
            c.nav_item("Dashboard", key="dashboard")
            c.nav_item("Users", key="users")
        with c.nav_group("Settings", icon="cog"):
            c.nav_item("General", key="settings")

    with c.shell_content():
        with c.nav_panel("dashboard"):
            c.title("Dashboard", level=2)
            with c.row():
                c.metric("Users", "1,234")
                c.metric("Revenue", "$45k")

        with c.nav_panel("users"):
            c.title("Users", level=2)
            c.table([
                {"name": "Alice", "email": "alice@example.com"},
                {"name": "Bob", "email": "bob@example.com"},
            ])

        with c.nav_panel("settings"):
            c.title("Settings", level=2)
            c.text("Configure your application here.")
```

### Tool App (Static-Ready)

```python
"""Tool that works in static builds."""
import cacao as c

c.config(title="Text Tool", theme="dark")

# Signals for state
input_text = c.signal("", name="input_text")
output = c.signal("", name="output")
mode = c.signal("upper", name="mode")

# These handlers must exist in JS for static builds!
# See: cacao/frontend/src/handlers/

@c.on("set_upper")
async def set_upper(session, event):
    mode.set(session, "upper")

@c.on("set_lower")
async def set_lower(session, event):
    mode.set(session, "lower")

@c.on("process_text")
async def process(session, event):
    text = event.get("value", "")
    m = mode.get(session)
    if m == "upper":
        output.set(session, text.upper())
    else:
        output.set(session, text.lower())

with c.card("Text Transformer"):
    c.text("Transform text to uppercase or lowercase.", color="muted")
    c.spacer()

    with c.row():
        c.button("UPPERCASE", on_click="set_upper")
        c.button("lowercase", on_click="set_lower", variant="outline")

    c.spacer()

    with c.row():
        with c.col(span=6):
            c.textarea(label="Input", on_change="process_text", rows=6)
        with c.col(span=6):
            c.text("Output", size="sm", color="muted")
            c.code(output)
```

## App Structure Patterns

### Single File (Simple)

```
my-app/
└── app.py
```

### Multi-File (Organized)

```
my-app/
├── app.py              # Main entry, layout
├── pages/
│   ├── __init__.py
│   ├── dashboard.py    # Dashboard components
│   └── settings.py     # Settings components
├── components/
│   ├── __init__.py
│   └── custom.py       # Reusable components
└── README.md
```

### Tool Collection (Like cacao-tools)

```
my-tools/
├── app.py              # Main app with navigation
├── tools/
│   ├── __init__.py
│   ├── encoders.py     # Encoder tools
│   ├── generators.py   # Generator tools
│   └── converters.py   # Converter tools
├── .github/
│   └── workflows/
│       └── deploy.yml  # GitHub Pages deployment
└── README.md
```

## Modular Tool Pattern

**app.py**:
```python
import cacao as c
from tools.encoders import base64_tool, url_tool
from tools.generators import uuid_tool

c.config(title="My Tools", theme="dark")

with c.app_shell(brand="Tools", default="base64"):
    with c.nav_sidebar():
        with c.nav_group("Encoders"):
            c.nav_item("Base64", key="base64")
            c.nav_item("URL", key="url")
        with c.nav_group("Generators"):
            c.nav_item("UUID", key="uuid")

    with c.shell_content():
        with c.nav_panel("base64"):
            base64_tool()
        with c.nav_panel("url"):
            url_tool()
        with c.nav_panel("uuid"):
            uuid_tool()
```

**tools/encoders.py**:
```python
import cacao as c

def base64_tool():
    output = c.signal("", name="base64_out")

    with c.card():
        c.text("Encode/decode Base64", color="muted")
        c.spacer()

        with c.row():
            c.button("Encode", on_click="base64_encode")
            c.button("Decode", on_click="base64_decode", variant="outline")

        c.spacer()

        with c.row():
            with c.col(span=6):
                c.textarea(label="Input", on_change="base64_process", rows=6)
            with c.col(span=6):
                c.text("Output", size="sm", color="muted")
                c.code(output)
```

## GitHub Pages Deployment

**`.github/workflows/deploy.yml`**:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Cacao
        run: pip install cacao

      - name: Build static site
        run: |
          REPO_NAME=$(echo "${{ github.repository }}" | cut -d'/' -f2)
          cacao build app.py --base-path "/$REPO_NAME"

      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

## Testing Examples

```bash
# Run in development mode
cacao run app.py

# Build static and preview
cacao build app.py
python -m http.server -d dist

# Build with base path (for GitHub Pages)
cacao build app.py --base-path /my-repo
```

## Checklist for Examples

- [ ] Works with `cacao run` (dynamic mode)
- [ ] Works with `cacao build` (static mode)
- [ ] All event handlers have JS equivalents (for static)
- [ ] Signal names are unique and descriptive
- [ ] Has meaningful title and theme
- [ ] Code is well-organized and documented
- [ ] README explains what the example demonstrates
