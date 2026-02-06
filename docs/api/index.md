# API Reference

Complete API documentation for Cacao.

## Core Modules

### cacao

The main module providing the primary API.

```python
import cacao

app = cacao.App()
```

### cacao.App

The main application class.

```python
class App:
    def __init__(self) -> None:
        """Initialize a new Cacao application."""

    def mix(self, route: str) -> Callable:
        """
        Decorator to register a route handler.

        Args:
            route: URL path for this route (e.g., "/" or "/about")

        Returns:
            Decorator function

        Example:
            @app.mix("/")
            def home():
                return {"type": "h1", "props": {"content": "Hello"}}
        """

    def event(self, event_name: str) -> Callable:
        """
        Decorator to register an event handler.

        Args:
            event_name: Name of the event to handle

        Returns:
            Decorator function

        Example:
            @app.event("button_clicked")
            def handle_click(event_data=None):
                return {"status": "success"}
        """

    def brew(
        self,
        type: str = "web",
        title: str = "Cacao App",
        host: str = "localhost",
        port: int = 1634,
        ws_port: int = 1633,
        theme: dict = None,
        **kwargs
    ) -> None:
        """
        Start the application.

        Args:
            type: "web" or "desktop"
            title: Window title (desktop mode)
            host: Server host
            port: HTTP server port
            ws_port: WebSocket server port
            theme: Theme configuration dict
        """
```

### cacao.State

Reactive state container.

```python
from cacao import State

class State[T]:
    def __init__(self, initial_value: T) -> None:
        """
        Create a new state container.

        Args:
            initial_value: Initial value of any type
        """

    @property
    def value(self) -> T:
        """Get the current value."""

    def set(self, new_value: T) -> None:
        """
        Replace the current value.

        Args:
            new_value: New value to set
        """

    def update(self, updates: dict) -> None:
        """
        Merge updates into the current value (for dict values).

        Args:
            updates: Dictionary of updates to merge
        """

    def subscribe(self, callback: Callable[[T], None]) -> Callable:
        """
        Decorator to subscribe to state changes.

        Args:
            callback: Function called with new value on change

        Returns:
            The callback function
        """
```

### cacao.Component

Base class for UI components.

```python
from cacao import Component

class Component:
    def __init__(self) -> None:
        """Initialize a component with unique ID."""
        self.id: int
        self.component_type: str

    def render(self, ui_state: dict = None) -> dict:
        """
        Render the component to a UI dictionary.

        Args:
            ui_state: Optional client-side state

        Returns:
            Dictionary representing the UI structure
        """
```

## UI Components

### cacao.ui.Table

```python
from cacao.ui import Table

class Table:
    def __init__(
        self,
        headers: List[str],
        rows: List[List[Any]],
        **kwargs
    ) -> None:
        """
        Create a table component.

        Args:
            headers: Column header labels
            rows: List of row data (list of lists)
        """

    def render(self, ui_state: dict = None) -> dict:
        """Render the table."""
```

### cacao.ui.Slider

```python
from cacao.ui import Slider

class Slider:
    def __init__(
        self,
        min_value: float = 0,
        max_value: float = 100,
        step: float = 1,
        value: float = None,
        **kwargs
    ) -> None:
        """
        Create a slider input component.

        Args:
            min_value: Minimum slider value
            max_value: Maximum slider value
            step: Step increment
            value: Initial value
        """
```

## Theme API

```python
from cacao.core import set_theme, get_theme, get_color, reset_theme

def set_theme(theme: dict) -> None:
    """
    Set or update the global theme.

    Args:
        theme: Theme configuration dictionary
    """

def get_theme() -> dict:
    """Get the current theme configuration."""

def get_color(name: str, default: str = None) -> str:
    """
    Get a color from the current theme.

    Args:
        name: Color name (e.g., "primary", "background")
        default: Default value if color not found

    Returns:
        Color value string
    """

def reset_theme() -> None:
    """Reset theme to defaults."""
```

## Icon Registry

```python
import cacao

# Access the global icon registry
cacao.icon_registry.register_icon(name: str, svg_content: str) -> bool
cacao.icon_registry.register_icon_from_file(name: str, file_path: str) -> bool
cacao.icon_registry.load_icons_from_directory(directory: str) -> int
cacao.icon_registry.process_content(content: str) -> str
cacao.icon_registry.get_icon(prefix: str, name: str, params: str = None) -> str
cacao.icon_registry.get_all_icon_names() -> dict
cacao.icon_registry.clear_cache() -> None
```

## Server

```python
from cacao.core.server import CacaoServer

class CacaoServer:
    def __init__(
        self,
        host: str = "localhost",
        http_port: int = 1634,
        ws_port: int = 1633,
        verbose: bool = False,
        enable_pwa: bool = False
    ) -> None:
        """
        Create a Cacao server instance.

        Args:
            host: Host to bind to
            http_port: HTTP server port
            ws_port: WebSocket server port
            verbose: Enable verbose logging
            enable_pwa: Enable PWA features
        """

    def run(self) -> None:
        """Start the server."""
```

## Decorators

```python
from cacao.core.decorators import mix, ROUTES, EVENT_HANDLERS

# Global route registry
ROUTES: Dict[str, Callable]

# Global event handler registry
EVENT_HANDLERS: Dict[str, Callable]
```

## Type Definitions

### UI Element Structure

```python
UIElement = {
    "type": str,                    # Element type (required)
    "component_type": str,          # Component identifier (optional)
    "props": {
        "content": str,             # Text content
        "style": dict,              # CSS styles (camelCase)
        "children": List[UIElement], # Child elements
        "action": str,              # Event handler name
        "data": dict,               # Data to pass with action
        # ... other element-specific props
    },
    "children": List[UIElement]     # Alternative to props.children
}
```

### Theme Structure

```python
Theme = {
    "colors": {
        "primary": str,
        "secondary": str,
        "background": str,
        "text": str,
        "accent": str,
        "sidebar_bg": str,
        "sidebar_header_bg": str,
        "sidebar_text": str,
        "content_bg": str,
        "card_bg": str,
        "border_color": str,
    }
}
```

## See Also

- [Core Concepts](guide/concepts.md) - Understanding Cacao architecture
- [State Management](guide/state.md) - Working with reactive state
- [Components](guide/components.md) - Building UI components
