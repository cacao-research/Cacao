![image](https://github.com/user-attachments/assets/830a00ca-7948-42ff-9196-adb58357c536)

# 🍫 Cacao

[![PyPI Version](https://img.shields.io/pypi/v/Cacao)](https://pypi.org/project/Cacao/)
[![Downloads](https://static.pepy.tech/badge/Cacao)](https://pepy.tech/project/Cacao)
[![Python Versions](https://img.shields.io/pypi/pyversions/Cacao)](https://pypi.org/project/Cacao/)
[![License](https://img.shields.io/pypi/l/Cacao)](https://github.com/jhd3197/cacao/blob/main/LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/jhd3197/cacao/publish.yml?branch=main)](https://github.com/jhd3197/cacao/actions)
[![GitHub Stars](https://img.shields.io/github/stars/jhd3197/cacao?style=social)](https://github.com/jhd3197/cacao)

---
## Description

Cacao is a modern, high-performance web framework for building reactive Python apps with real-time capabilities. Designed for developers who want full control without sacrificing simplicity, Cacao blends a clean decorator-based API with a powerful component and state management system — all backed by JSON-defined UIs and WebSocket-driven live updates.

Whether you're creating dashboards, internal tools, or interactive data apps, Cacao offers a fully Pythonic development experience with robust features like hot reload, real-time communication, and seamless frontend-backend integration.

> **⚠️ Warning:** Cacao is currently in early development. Features and APIs are subject to change, and breaking changes may occur in future updates. Use with caution in production environments.


## 🏗️ Architecture

### Core System
- **Decorator-based Routing**: Simple `@mix` decorators for defining UI routes
- **Hot Reload**: Real-time UI updates with WebSocket-based hot reload
- **JSON UI Definitions**: Define UIs using pure Python dictionaries
- **State Management**: Reactive state handling with automatic UI updates
- **Component System**: Create reusable, composable UI components with type-based state isolation
- **Progressive Web App (PWA)**: Built-in PWA capabilities with offline support
- **Session Management**: Persistent session state across page refreshes
- **Desktop Application Mode**: Run Cacao apps as native desktop applications
- **Hybrid Mode Support**: Run the same codebase in both web and desktop environments

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
- **PWA Support**: Make your app installable with offline capabilities
- **Session Persistence**: Maintain state across page refreshes
- **Desktop Mode**: Run as a standalone desktop application
- **React Integration**: Use React components from npm packages directly in your Cacao apps
- **Hybrid Mode**: Switch between web and desktop modes with the same codebase
- **Global Theme System**: Consistent styling with theme inheritance
- **Component-Level Theming**: Override global themes at component level

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
│   ├── pwa.py            # PWA support functionality
│   ├── session.py        # Session persistence management
│   └── static/            # Static assets
│       ├── js/            # Client-side JavaScript
│       ├── css/           # Stylesheets
│       └── icons/         # PWA icons
├── desktop.py            # Desktop application support
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

### Simple Example

Here's a minimal example showing how to create a basic Cacao application:

```python
import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "style": {
                "padding": "20px",
                "fontFamily": "Arial, sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Welcome to Cacao",
                    "style": {
                        "color": "#f0be9b",
                        "marginBottom": "20px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "A deliciously simple web framework!",
                    "style": {
                        "color": "#D4A76A"
                    }
                }
            }
        ]
    }

if __name__ == "__main__":
    app.brew()  # Run the app like brewing hot chocolate!
```

### Advanced Layout Example

For more complex applications, Cacao provides layout components like `SidebarLayout`:

```python
from cacao import App
from cacao.ui.components.sidebar_layout import SidebarLayout

app = App()

class DashboardPage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {"padding": "20px"},
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "grid",
                                "gridTemplateColumns": "repeat(2, 1fr)",
                                "gap": "20px"
                            },
                            "children": [
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "backgroundColor": "#F5F5F5",
                                            "borderRadius": "8px",
                                            "padding": "20px"
                                        },
                                        "children": [
                                            {
                                                "type": "h2",
                                                "props": {
                                                    "content": "Users",
                                                    "style": {"color": "#6B4226"}
                                                }
                                            },
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": "1,234",
                                                    "style": {
                                                        "fontSize": "24px",
                                                        "fontWeight": "bold"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

# Define navigation structure
nav_items = [
    {"id": "home", "label": "Home", "icon": "H"},
    {"id": "dashboard", "label": "Dashboard", "icon": "D"},
    {"id": "settings", "label": "Settings", "icon": "S"}
]

# Create layout with components
sidebar_layout = SidebarLayout(
    nav_items=nav_items,
    content_components={
        "dashboard": DashboardPage()
    },
    app_title="My Cacao App"
)

@app.mix("/")
def home():
    return sidebar_layout.render()

if __name__ == "__main__":
    app.brew(
        type="desktop",  # Can be "web" or "desktop"
        title="Cacao Example",
        width=800,
        height=600,
        resizable=True
    )
```

## 🛠️ Creating UI Components

Cacao allows you to define UI components with isolated state management and automatic hot reload. For a complete example of component creation and state management, check out `examples/counter_example.py` which demonstrates:

- Component-specific state isolation using `component_type`
- Event handling with `@app.event` decorators
- State management with `State` class
- Type-safe component implementations

For example, see how a counter component is created:

```python
from cacao import App, State, Component

# Define state and create component - See examples/counter_example.py for full implementation
counter_state = State(0)

class Counter(Component):
    def __init__(self) -> None:
        super().__init__()
        self.component_type = "counter"  # Enable state isolation
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
from cacao import State
from datetime import datetime

# Create separate states for different components
counter_state = State(0)
timestamp_state = State(datetime.now())

# Update state values
counter_state.update(5)
timestamp_state.update(datetime.now())

# Component-specific state updates via event handlers
@mix.event("increment_counter")
async def handle_increment(event):
    counter_state.update(counter_state.value + 1)
    print(f"Counter changed to: {counter_state.value}")

@mix.event("refresh_timestamp")
async def handle_refresh(event):
    timestamp_state.update(datetime.now())
    print(f"Timestamp updated to: {timestamp_state.value}")
```

## 🧱 Component System

Create reusable components with the Component base class:

```python
from cacao import Component
from typing import Dict, Any, Optional

class MyComponent(Component):
    def __init__(self, title: str):
        """Initialize the component with a title."""
        super().__init__()
        self.title = title
        self.component_type = "my-component"  # Unique component type for state isolation
    
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Render the component.
        
        Args:
            ui_state: Optional state from the UI definition
            
        Returns:
            JSON UI definition for the component
        """
        return {
            "type": "section",
            "component_type": self.component_type,  # Include component type in output
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {"content": self.title}
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Click Me",
                            "action": "component_action",
                            "params": {"component_id": id(self)}  # Pass component ID in action
                        }
                    }
                ]
            }
        }
```

## 🌐 Progressive Web App (PWA) Support

Cacao includes built-in PWA capabilities, allowing your applications to be installed on devices and work offline:

```python
from cacao import run
from cacao.core.server import CacaoServer

# Run with PWA support enabled
server = CacaoServer(
    verbose=True,
    enable_pwa=True,  # Enable PWA support
    persist_sessions=True  # Enable session persistence
)
server.run()
```

### PWA Configuration

The PWA support can be customized in your cacao.json configuration:

```json
{
    "pwa": {
        "name": "Cacao App",
        "short_name": "Cacao",
        "description": "A Cacao Progressive Web App",
        "theme_color": "#6B4226",
        "background_color": "#F5F5F5",
        "display": "standalone",
        "start_url": "/"
    }
}
```

### PWA Features

- **Offline Support**: Applications continue to work without an internet connection
- **Installation**: Users can install your app on mobile and desktop devices
- **Service Worker**: Automatic service worker generation for resource caching
- **PWA Manifest**: Auto-generated manifest.json with customizable options

## 💾 Session Management

Cacao's session management system provides persistent state across page refreshes:

```python
from cacao import run

# Run with session persistence
run(persist_sessions=True, session_storage="memory")  # or "file"
```

### Session Storage Options

- **Memory Storage**: Sessions are stored in memory (default, cleared on server restart)
- **File Storage**: Sessions are stored in files (persists through server restarts)

### Session Features

- **Automatic State Persistence**: App state automatically persists across page refreshes
- **Session Expiration**: Configurable session timeout (defaults to 24 hours)
- **Cross-Tab State**: State can be shared across browser tabs (same session)
- **Security**: Sessions are secured with HTTP-only cookies

## 🖥️ Desktop Application Mode

Cacao's unified `brew()` method now supports both web and desktop applications through a single interface:

```python
# Run as web application
app.brew()

# Run as desktop application
app.brew(
    type="desktop",
    title="My Desktop App",
    width=800,
    height=600,
    resizable=True,
    fullscreen=False
)
```


### Desktop Features

- **Native Window**: Runs in a native OS window without browser UI
- **Window Controls**: Customize window size, title, and behavior
- **Automatic Server**: Built-in Cacao server runs in the background
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Hybrid Support**: Same codebase can run in both web and desktop modes


## ⚛️ React Integration

Cacao provides seamless integration with React components from npm packages:

```python
from cacao import App
from cacao.ui import ReactComponent
from cacao.extensions.react_extension import ReactExtension

# Create app with React extension
app = App(extensions=[ReactExtension()])

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "children": [
                {
                    "type": "h1",
                    "props": {
                        "content": "CodeMirror Example"
                    }
                },
                # Use CodeMirror React component
                ReactComponent(
                    package="codemirror",
                    component="CodeMirror",
                    props={
                        "value": "const hello = 'world';",
                        "options": {
                            "mode": "javascript",
                            "theme": "material",
                            "lineNumbers": True
                        }
                    },
                    css=["lib/codemirror.css", "theme/material.css"]
                ).render()
            ]
        }
    }
```

### React Integration Features

- **NPM Package Integration**: Use React components from npm packages directly
- **Dynamic Loading**: Components are loaded on-demand from CDNs
- **Props Passing**: Pass props to React components from Python
- **Event Handling**: Handle events from React components in Python
- **CSS Loading**: Automatically load CSS files for React components
- **Multiple Components**: Use multiple React components in the same app

For more details, see [React Integration Guide](docs/REACT_INTEGRATION.md) and check out the examples in `examples/react_component_example.py` and `examples/advanced_react_example.py`.


### 🎨 Theme System

Cacao now includes a powerful global theme system that allows consistent styling across your entire application:

### Setting a Global Theme

```python
import cacao

app = cacao.App()

# Define your custom theme
my_theme = {
    "colors": {
        "primary": "#2196F3",
        "secondary": "#03A9F4",
        "background": "#F0F8FF",
        "text": "#2C3E50",
        "accent": "#FF5722",
        "sidebar_bg": "#1A365D",
        "sidebar_header_bg": "#2C5282",
        "content_bg": "#F0F8FF",
        "card_bg": "#FFFFFF",
        "border_color": "#BEE3F8"
    }
}

# Apply theme when starting the app
app.brew(
    type="web",
    theme=my_theme
)
```

### Example Implementation

Check out the `examples/sidebar_layout_example.py` for a practical implementation of hybrid mode:

```bash
# Run in web browser mode
python examples/sidebar_layout_example.py

# Run in desktop mode
python examples/sidebar_layout_example.py --mode desktop
```

This example demonstrates how to create a multi-page application using the SidebarLayout component that can run in either web or desktop mode with identical functionality.

## 🧪 Testing Framework

Cacao includes a comprehensive testing framework built on pytest, making it easy to validate your application's behavior:

```python
# Run all tests with the test manager
python test.py

# Run specific test files
python test.py test/test_state.py test/test_server.py

# Run tests matching a pattern
python test.py -k "component"
```

### Test Organization

Tests are organized by subsystem for clear separation of concerns:

- **`test_components.py`**: Component creation and rendering
- **`test_integration.py`**: Component and state integration
- **`test_plugins.py`**: Plugin system functionality
- **`test_pwa.py`**: Progressive Web App features
- **`test_server.py`**: HTTP and WebSocket server
- **`test_session.py`**: Session management and persistence
- **`test_state.py`**: Reactive state management
- **`test_ui_components.py`**: UI component system

### Writing Tests

Cacao follows the Arrange-Act-Assert pattern for clear, readable tests:

```python
def test_state_reactivity():
    # Arrange
    counter = State(0)
    
    # Act
    counter.set(5)
    
    # Assert
    assert counter.value == 5

def test_component_rendering():
    # Arrange
    button = Button(label="Click me")
    
    # Act
    rendered = button.render()
    
    # Assert
    assert rendered["type"] == "button"
    assert rendered["props"]["label"] == "Click me"
```

### Test Fixtures

The testing framework provides useful fixtures to simplify testing:

```python
@pytest.fixture
def test_state():
    """Fixture for creating a test state instance"""
    return State(initial_value=0)

@pytest.fixture
def test_component():
    """Fixture for creating a basic test component"""
    class TestComponent(Component):
        def render(self):
            return {
                "type": "div",
                "props": {"content": "Test Component"}
            }
    return TestComponent()
```

Use the test runner to automatically discover and execute tests while suppressing warnings and providing clear output.

## 📸 Screenshots

<img width="1184" alt="image" src="https://github.com/user-attachments/assets/bfe66a0b-1712-49cd-a617-43c16590a5b9" />

<img width="1241" alt="image" src="https://github.com/user-attachments/assets/9dfd5cc8-b547-4a43-bcf0-acc322bf1e22" />

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
