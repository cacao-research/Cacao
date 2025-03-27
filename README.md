# 🍫 Cacao

Cacao is a modern, high-performance web framework for building reactive Python apps with real-time capabilities. Designed for developers who want full control without sacrificing simplicity, Cacao blends a clean decorator-based API with a powerful component and state management system — all backed by JSON-defined UIs and WebSocket-driven live updates.

Whether you're creating dashboards, internal tools, or interactive data apps, Cacao offers a fully Pythonic development experience with robust features like hot reload, real-time communication, and seamless frontend-backend integration.

## 🏗️ Architecture

### Core System
- **Decorator-based Routing**: Simple `@mix` decorators for defining UI routes
- **Hot Reload**: Real-time UI updates with WebSocket-based hot reload
- **JSON UI Definitions**: Define UIs using pure Python dictionaries
- **State Management**: Reactive state handling with automatic UI updates
- **Component System**: Create reusable, composable UI components with type-based state isolation

### Extensions
- **Authentication**: Built-in auth system with multiple provider support
- **Plugins**: Extensible plugin system for custom functionality
- **Metrics**: Performance monitoring and analytics
- **Background Tasks**: Async task queue for long-running operations

## ✨ Features

- **Reactive UI**: Build interactive dashboards and data apps with ease
- **Hot Reload**: See your changes instantly with the built-in hot reload system
- **Component-Based**: Create reusable UI components with isolated state
- **Python-Powered**: Use Python for both frontend and backend logic
- **Real-time Updates**: WebSocket-based live updates
- **Theme Support**: Customizable themes with hot-reload support
- **Type Safety**: Full TypeScript-like type hints in Python
- **Developer Tools**: Built-in debugging and development tools

## 🧩 Component State Management

Cacao provides advanced component state isolation:

- Each component can have its own unique state
- Components are identified by a `component_type`
- Server-side routing ensures state updates are component-specific
- Prevents unintended state sharing between components

```python
from cacao import mix, State, Component
from datetime import datetime

# Separate states for different components
counter_state = State(0)
timestamp_state = State(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class Counter(Component):
    def __init__(self):
        super().__init__()
        self.component_type = "counter"  # Add component type
    
    def render(self, ui_state=None):
        counter_value = self._get_counter_value(ui_state)
        return {
            "type": "section",
            "component_type": self.component_type,
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {"content": f"Counter: {counter_value}"}
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Increment",
                            "action": "increment_counter"
                        }
                    }
                ]
            }
        }
```

## 📁 Project Structure

```
cacao/
├── core/                   # Core framework functionality
│   ├── decorators.py      # Route decorators and registry
│   ├── server.py          # HTTP and WebSocket servers
│   ├── state.py           # State management system
│   ├── diffing.py         # UI diffing algorithm
│   └── static/            # Static assets
│       ├── js/            # Client-side JavaScript
│       └── css/           # Stylesheets
├── ui/                    # UI component system
│   ├── components/        # Built-in components
│   │   ├── base.py       # Base component classes
│   │   ├── inputs.py     # Form inputs
│   │   ├── data.py       # Data display components
│   │   └── layout.py     # Layout components
│   └── themes/           # Theming system
├── extensions/           # Framework extensions
│   ├── auth/            # Authentication system
│   ├── plugins/         # Plugin system
│   └── metrics/         # Performance metrics
├── utilities/           # Helper utilities
│   ├── cache.py        # Caching system
│   └── task_queue.py   # Background task queue
└── cli/                # Command-line tools
```

## 🚀 Quick Start

### Installation

```bash
# Install the package in development mode
pip install -e .
```

### Running the Development Server

```bash
# Run with the CLI
python -m cacao serve

# Or with verbose logging
python -m cacao serve -v

# Or directly from main.py
python main.py
```

## 🛠️ Creating UI Components

Define your UI using Python dictionaries with automatic hot reload:

```python
from cacao import mix, State, Component

# Define a reactive state
counter = State(0)

# Create a reusable component
class Counter(Component):
    def render(self):
        return {
            "type": "section",
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {"content": f"Count: {counter.value}"}
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Increment",
                            "onClick": lambda: counter.set(counter.value + 1)
                        }
                    }
                ]
            }
        }

# Define a route
@mix("/")
def home():
    return {
        "layout": "column",
        "children": [
            {
                "type": "navbar",
                "props": {
                    "brand": "Cacao",
                    "links": [
                        {"name": "Home", "url": "/"},
                        {"name": "About", "url": "/about"}
                    ]
                }
            },
            Counter(),  # Use the custom component
            {
                "type": "footer",
                "props": {"text": "© 2025 Cacao Framework"}
            }
        ]
    }
```

## 🔄 Hot Reload

Cacao includes a powerful hot reload system that automatically refreshes your UI when you make changes to your code:

1. Start the development server
2. Open your browser to http://localhost:1634
3. Edit your UI code in `main.py`
4. Watch as your changes appear instantly with a smooth brown overlay animation

### Manual Refresh

If you need to force a refresh, you can:

- Click the refresh button in the bottom-right corner of the page
- Press Ctrl+R (or Cmd+R) to force a refresh
- Press F5 to reload the page completely

## 📊 State Management

Cacao provides a flexible, component-aware state management system:

```python
# Create separate states for different components
counter_state = State(0)
timestamp_state = State(datetime.now())

# Component-specific state updates
@counter_state.subscribe
def on_counter_change(new_value):
    print(f"Counter changed to: {new_value}")

@timestamp_state.subscribe
def on_timestamp_change(new_value):
    print(f"Timestamp updated to: {new_value}")
```

## 🧱 Component System

Create reusable components with the Component base class:

```python
from cacao import Component

class MyComponent(Component):
    def __init__(self, title: str):
        self.title = title
    
    def render(self):
        return {
            "type": "section",
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {"content": self.title}
                    }
                ]
            }
        }
```

## ❓ Troubleshooting

If hot reload isn't working:

1. Check the browser console for errors
2. Make sure the WebSocket connection is established
3. Try using the manual refresh button
4. Restart the server with verbose logging: `python -m cacao serve -v`

## 👥 Contributing

Contributions are welcome! Please read our contributing guidelines for details.

## 📄 License

MIT
