# Cacao

A reactive web framework for Python. Build dashboards and data apps with a fluent Python API.

## Quick Start

```bash
# Install
pip install cacao uvicorn

# Create app.py
cat > app.py << 'EOF'
import cacao as c

c.config(title="My Dashboard")

with c.page("/"):
    c.title("Hello Cacao")
    with c.row():
        c.metric("Users", 1234, trend="+12%")
        c.metric("Revenue", "$45,231", trend="+8%")

c.run()
EOF

# Run (default port: 1604)
cacao run app.py
```

Open http://localhost:1604

## Features

- **Fluent Python API** - No HTML/JS needed
- **Real-time updates** - WebSocket-based state sync
- **Built-in components** - Metrics, charts, tables, forms
- **Auto port finding** - Increments if port in use
- **Hot reload** - Changes apply instantly

## Components

### Layout
```python
with c.row(gap=4):
    with c.col(span=6):
        c.card("Left")
    with c.col(span=6):
        c.card("Right")
```

### Data Display
```python
c.metric("Sales", "$12,345", trend="+15%", trend_direction="up")
c.table(data, columns=["name", "value"])
c.progress("Loading", value=75, max=100)
```

### Charts
```python
c.line(data, x="date", y=["revenue", "costs"])
c.bar(data, x="category", y="count")
c.pie(data, name_field="label", value_field="value")
```

### Forms
```python
c.button("Submit", on_click="submit")
c.select("Period", options=["Day", "Week", "Month"])
c.slider("Volume", min=0, max=100)
```

## Signals (Reactive State)

```python
count = c.signal(0, name="count")

@c.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + 1)

with c.page("/"):
    c.metric("Count", count)
    c.button("+", on_click="increment")
```

## File Structure

```
cacao/
├── frontend/           # React + LESS source
│   ├── src/
│   │   ├── styles/     # Modular LESS
│   │   └── components/ # React components
│   └── dist/           # Built CSS/JS
├── server/             # Starlette server
├── cli/                # CLI commands
└── examples/           # Example apps
```

## Build Frontend

```bash
cd cacao/frontend
npm install
npm run build
```

## Default Ports

- HTTP: 1604
- WebSocket: 1604/ws

If the port is in use, it auto-increments to find an available one.
