# Cacao

**A high-performance reactive web framework for Python**

Cacao makes it easy to build interactive dashboards, internal tools, and data applications using Python. It features WebSocket-driven real-time updates, JSON-defined UIs, and supports both web and desktop modes.

## Features

- **Reactive State Management** - Changes to state automatically update the UI
- **Real-time Updates** - WebSocket-powered for instant client-server communication
- **JSON-based UI** - Define your interface with Python dictionaries
- **Hot Reload** - See changes instantly during development
- **Desktop Support** - Run your app as a native desktop application
- **Component System** - Build reusable UI components

## Quick Example

```python
import cacao
from cacao import State

app = cacao.App()
counter = State(0)

@app.event("increment")
def handle_increment(event_data=None):
    counter.set(counter.value + 1)
    return {"counter": counter.value}

@app.mix("/")
def home():
    return {
        "type": "div",
        "children": [
            {"type": "h1", "props": {"content": "Counter App"}},
            {"type": "text", "props": {"content": str(counter.value)}},
            {"type": "button", "props": {"label": "+", "action": "increment"}}
        ]
    }

if __name__ == "__main__":
    app.brew()
```

## Installation

```bash
pip install cacao
```

## Getting Started

Ready to dive in? Check out the [Quickstart Guide](getting-started/quickstart.md) to build your first Cacao app.

## Documentation

| Section | Description |
|---------|-------------|
| [Getting Started](getting-started/installation.md) | Installation and first steps |
| [Guide](guide/concepts.md) | Core concepts and patterns |
| [Examples](examples/index.md) | Example applications gallery |
| [API Reference](api/index.md) | Full API documentation |
| [CLI Reference](cli.md) | Command-line tools |

## Current Status

Cacao is in early development (v1.0.x). APIs may change as the framework evolves.
