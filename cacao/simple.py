"""
Simplified Cacao API.

This module provides a Streamlit-like API where you can write:

    import cacao as c

    c.title("Hello World")
    with c.row():
        c.metric("Users", 100)
        c.metric("Revenue", "$5K")

No App(), no page(), no boilerplate. Just write components.

For more control, use the full API from cacao.server.ui.
"""

from __future__ import annotations

import inspect
import sys
from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps
from typing import Any, Literal, TypeVar

from .server import ui as _ui_module
from .server.signal import Computed, Signal
from .server.ui import (
    App as _App,
)
from .server.ui import (
    Component,
    _current_container,
)

T = TypeVar("T")

# =============================================================================
# Global State
# =============================================================================

# The implicit global app instance (lazily created)
_global_app: _App | None = None

# Default configuration
_DEFAULT_CONFIG: dict[str, Any] = {
    "title": "Cacao App",
    "theme": "dark",
    "host": "127.0.0.1",
    "port": 1502,  # 1502: Columbus encounters cacao in Honduras
}

# Configuration set via config() — seeded from cacao.yaml then overridden by c.config()
_global_config: dict[str, Any] = _DEFAULT_CONFIG.copy()

# Track which keys were explicitly set via c.config() (these take priority over yaml)
_explicit_config_keys: set[str] = set()

# Whether we've loaded the yaml config yet
_yaml_config_loaded: bool = False

# The raw yaml data (full file, for plugins/CacaoDocs to access)
_yaml_raw_data: dict[str, Any] = {}

# Path to the loaded config file
_yaml_config_path: str | None = None

# Whether we're in "simple mode" (implicit app)
_simple_mode: bool = False

# Static build: custom JS handlers and scripts registered by the app
_static_handlers: dict[str, str] = {}
_static_scripts: list[str] = []


def _load_yaml_config() -> None:
    """Load cacao.yaml if not already loaded. Called lazily on first app creation."""
    global _yaml_config_loaded, _yaml_raw_data, _yaml_config_path

    if _yaml_config_loaded:
        return
    _yaml_config_loaded = True

    from .config import extract_app_config, find_config_file, load_config_file

    path = find_config_file()
    if path is None:
        return

    _yaml_config_path = str(path)
    _yaml_raw_data = load_config_file(path)
    app_config = extract_app_config(_yaml_raw_data)

    # Apply yaml values only for keys NOT explicitly set via c.config()
    for key, value in app_config.items():
        if key not in _explicit_config_keys:
            _global_config[key] = value


def _get_app() -> _App:
    """Get or create the global app instance."""
    global _global_app, _simple_mode

    if _global_app is None:
        # Load cacao.yaml before creating the app
        _load_yaml_config()

        _global_app = _App(
            title=_global_config["title"],
            theme=_global_config["theme"],
            branding=_global_config.get("branding"),
        )
        _simple_mode = True

        # Start the implicit "/" page context
        _start_implicit_page()

    return _global_app


def _start_implicit_page() -> None:
    """Start the implicit "/" page context."""
    global _global_app
    if _global_app is None:
        return

    # Set up the page context manually
    _global_app._current_page = "/"
    components: list[Component] = []
    _current_container.set(components)
    _global_app._pages["/"] = components


def _ensure_context() -> None:
    """Ensure we have a valid component context."""
    _get_app()  # This will create app and start implicit page if needed


# =============================================================================
# Configuration
# =============================================================================


def config(
    *,
    title: str | None = None,
    theme: str | None = None,
    host: str | None = None,
    port: int | None = None,
    debug: bool | None = None,
    branding: dict[str, Any] | None = None,
    **extra: Any,
) -> None:
    """
    Configure the application.

    Call before any UI components. Settings merge with cacao.yaml values,
    with c.config() taking priority.

    Example:
        c.config(title="My Dashboard", theme="dark", port=3000)
    """
    items = {
        "title": title,
        "theme": theme,
        "host": host,
        "port": port,
        "debug": debug,
        "branding": branding,
        **extra,
    }

    # Load yaml first so we know defaults
    _load_yaml_config()

    for key, value in items.items():
        if value is not None:
            _global_config[key] = value
            _explicit_config_keys.add(key)

    # If app already exists, update it
    if _global_app is not None:
        if title is not None:
            _global_app.title = title
        if theme is not None:
            _global_app.theme = theme
        if branding is not None:
            _global_app.branding = branding


# =============================================================================
# State Management
# =============================================================================


def signal(default: T, *, name: str) -> Signal[T]:
    """
    Create a reactive signal.

    Signals hold state that syncs between server and client. When a signal
    changes, any UI that depends on it updates automatically.

    Example:
        count = c.signal(0, name="count")

        @c.on("increment")
        async def increment(session, event):
            count.set(session, count.get(session) + 1)

    Args:
        default: Initial value
        name: Unique name for the signal (used for syncing with client)

    Returns:
        A new Signal instance
    """
    return Signal(default, name=name)


def computed(func: Callable[..., T], *, name: str | None = None) -> Computed[T]:
    """
    Create a computed signal (derived from other signals).

    Example:
        count = c.signal(0, name="count")
        doubled = c.computed(lambda s: count.get(s) * 2, name="doubled")
    """
    return Computed(func, name=name)


# =============================================================================
# Event Handlers
# =============================================================================


def on(event_name: str) -> Callable[..., Any]:
    """
    Decorator to register an event handler.

    Example:
        @c.on("submit")
        async def handle_submit(session, event):
            print("Form submitted!", event)

    Args:
        event_name: The event to handle (e.g., "click", "submit")

    Returns:
        Decorator function
    """
    app = _get_app()
    return app.on(event_name)


def bind(event_name: str, sig: Signal[T]) -> None:
    """
    Bind an event to automatically update a signal.

    Example:
        name = c.signal("", name="name")
        c.bind("name:input", name)  # Auto-updates signal on input

    Args:
        event_name: The event name (e.g., "name:input")
        signal: The signal to update
    """
    app = _get_app()
    app.bind(event_name, sig)


# =============================================================================
# Pages (Multi-page apps)
# =============================================================================


@contextmanager
def page(path: str = "/") -> Generator[None, None, None]:
    """
    Define a page at the given path.

    For simple single-page apps, you don't need this - components go to "/" automatically.

    Example:
        import cacao as c

        with c.page("/"):
            c.title("Home")

        with c.page("/about"):
            c.title("About Us")

    Args:
        path: URL path for this page (e.g., "/", "/dashboard")
    """
    app = _get_app()

    # End any implicit page context
    if app._current_page == "/" and path != "/":
        # Save implicit page components
        pass

    with app.page(path):
        yield


# =============================================================================
# Layout Presets (custom logic, not a simple wrapper)
# =============================================================================


class _LayoutHelper:
    """Helper object returned by layout() for accessing sub-regions."""

    def __init__(self, preset: str, **kwargs: Any):
        self.preset = preset
        self._kwargs = kwargs

    @contextmanager
    def side(self) -> Generator[None, None, None]:
        """Sidebar region of a sidebar/split layout."""
        width = self._kwargs.get("sidebar_width", "300px")
        with col(gap=4, width=width):
            yield

    @contextmanager
    def main(self) -> Generator[None, None, None]:
        """Main content region."""
        with col(gap=0):
            yield

    def _parse_ratio(self) -> tuple[int, int]:
        """Parse ratio string into (left, right) flex values."""
        ratio = self._kwargs.get("ratio", "1:1")
        parts = ratio.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid ratio '{ratio}': expected format 'N:M' (e.g. '1:1', '2:1')")
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            raise ValueError(
                f"Invalid ratio '{ratio}': both parts must be integers (e.g. '1:1', '2:1')"
            )

    @contextmanager
    def left(self) -> Generator[None, None, None]:
        """Left pane of a split layout."""
        left_flex, _ = self._parse_ratio()
        with col(gap=4, flex=str(left_flex)):
            yield

    @contextmanager
    def right(self) -> Generator[None, None, None]:
        """Right pane of a split layout."""
        _, right_flex = self._parse_ratio()
        with col(gap=4, flex=str(right_flex)):
            yield


@contextmanager
def layout(
    preset: Literal["sidebar", "centered", "split", "dashboard"] = "sidebar",
    *,
    sidebar_width: str = "300px",
    ratio: str = "1:1",
    gap: int = 4,
    **props: Any,
) -> Generator[_LayoutHelper, None, None]:
    """
    High-level layout preset.

    Example:
        with c.layout("sidebar", sidebar_width="300px") as l:
            with l.side():
                c.text("Sidebar content")
            with l.main():
                c.text("Main content")
    """
    _ensure_context()
    helper = _LayoutHelper(preset, sidebar_width=sidebar_width, ratio=ratio)

    if preset == "sidebar":
        with row(gap=gap, align="start", wrap=False, **props):
            yield helper
    elif preset == "centered":
        from .server.ui import container as _container

        with _container(size="md", **props):
            yield helper
    elif preset == "split":
        with row(gap=gap, align="stretch", wrap=False, **props):
            yield helper
    elif preset == "dashboard":
        from .server.ui import grid as _grid

        with _grid(cols=12, gap=gap, **props):
            yield helper
    else:
        with row(gap=gap, **props):
            yield helper


# =============================================================================
# Renamed / Aliased functions (name differs from ui.py)
# =============================================================================


def json(data: Any, expanded: bool = True, **props: Any) -> Component:
    """
    JSON tree viewer.

    Example:
        c.json({"name": "John", "age": 30})
    """
    _ensure_context()
    return _ui_module.json_view(data=data, expanded=expanded, **props)


# Alias for backwards compatibility
json_view = json


def input(
    label: str,
    signal: Signal[str] | None = None,
    placeholder: str = "",
    type: Literal["text", "password", "email", "number"] = "text",
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Text input field.

    Example:
        name = c.signal("", name="name")
        c.input("Name", signal=name, placeholder="Enter your name")
    """
    _ensure_context()
    return _ui_module.input_field(
        label=label, signal=signal, placeholder=placeholder, type=type, disabled=disabled, **props
    )


# Aliases
input_field = input
field = input


def date(
    label: str,
    signal: Signal[str] | None = None,
    placeholder: str = "Select date",
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Date picker.

    Example:
        start = c.signal("", name="start_date")
        c.date("Start Date", signal=start)
    """
    _ensure_context()
    return _ui_module.date_picker(
        label=label, signal=signal, placeholder=placeholder, disabled=disabled, **props
    )


# Alias
date_picker = date


def upload(
    label: str,
    on_upload: Callable[[bytes, str], Any] | None = None,
    accept: str | None = None,
    multiple: bool = False,
    **props: Any,
) -> Component:
    """
    File upload.

    Example:
        c.upload("Upload CSV", accept=".csv")
    """
    _ensure_context()
    return _ui_module.file_upload(
        label=label, on_upload=on_upload, accept=accept, multiple=multiple, **props
    )


# Alias
file_upload = upload


# =============================================================================
# Charts (re-export from chart module)
# =============================================================================


def _lazy_chart_import() -> Any:
    """Lazy import chart functions to avoid circular imports."""
    from .server import chart as _chart_module

    return _chart_module


def line(data: Any, x: str, y: str | list[str], **props: Any) -> Component:
    """Line chart."""
    _ensure_context()
    result: Component = _lazy_chart_import().line(data, x=x, y=y, **props)
    return result


def bar(data: Any, x: str, y: str | list[str], **props: Any) -> Component:
    """Bar chart."""
    _ensure_context()
    result: Component = _lazy_chart_import().bar(data, x=x, y=y, **props)
    return result


def pie(data: Any, values: str, names: str, **props: Any) -> Component:
    """Pie chart."""
    _ensure_context()
    result: Component = _lazy_chart_import().pie(data, values=values, names=names, **props)
    return result


def area(data: Any, x: str, y: str | list[str], **props: Any) -> Component:
    """Area chart."""
    _ensure_context()
    result: Component = _lazy_chart_import().area(data, x=x, y=y, **props)
    return result


def scatter(data: Any, x: str, y: str, **props: Any) -> Component:
    """Scatter chart."""
    _ensure_context()
    result: Component = _lazy_chart_import().scatter(data, x=x, y=y, **props)
    return result


def gauge(value: float, **props: Any) -> Component:
    """Gauge chart."""
    _ensure_context()
    result: Component = _lazy_chart_import().gauge(value, **props)
    return result


# =============================================================================
# Data Utilities (re-export from data module)
# =============================================================================


def _lazy_data_import() -> Any:
    """Lazy import data functions."""
    from .server import data as _data_module

    return _data_module


def load_csv(path: str) -> Any:
    """Load data from CSV file."""
    return _lazy_data_import().load_csv(path)


def load_json(path: str) -> Any:
    """Load data from JSON file."""
    return _lazy_data_import().load_json(path)


def sample_sales_data() -> Any:
    """Get sample sales data for demos."""
    return _lazy_data_import().sample_sales_data()


def sample_users_data() -> Any:
    """Get sample users data for demos."""
    return _lazy_data_import().sample_users_data()


# =============================================================================
# App Control
# =============================================================================


def run(
    *,
    host: str | None = None,
    port: int | None = None,
    reload: bool = False,
) -> None:
    """
    Run the application server.

    In simple mode, you usually don't need to call this - the CLI handles it.
    But you can call it explicitly for more control.

    Example:
        import cacao as c

        c.title("Hello")
        c.run(port=3000)

    Args:
        host: Host to bind to (default: from config or 127.0.0.1)
        port: Port to listen on (default: from config or 1502)
        reload: Enable hot reload
    """
    app = _get_app()

    # Use config values as defaults
    final_host = host or _global_config.get("host", "127.0.0.1")
    final_port = port or _global_config.get("port", 1502)

    app.run(host=final_host, port=final_port, reload=reload)


def get_app() -> _App:
    """
    Get the underlying App instance.

    Useful for advanced usage or when you need direct access to the app.
    """
    return _get_app()


def is_simple_mode() -> bool:
    """Check if we're running in simple mode (implicit app)."""
    return _simple_mode


def reset() -> None:
    """
    Reset global state.

    Mainly useful for testing. Clears the global app and config.
    """
    global _global_app, _simple_mode, _global_config
    global _yaml_config_loaded, _yaml_raw_data, _yaml_config_path
    _global_app = None
    _simple_mode = False
    _global_config = _DEFAULT_CONFIG.copy()
    _explicit_config_keys.clear()
    _yaml_config_loaded = False
    _yaml_raw_data = {}
    _yaml_config_path = None
    _static_handlers.clear()
    _static_scripts.clear()


def get_yaml_config() -> dict[str, Any]:
    """
    Get the raw parsed cacao.yaml data.

    Returns the full YAML dictionary, including keys that Cacao doesn't
    use directly (e.g. plugin-specific settings like CacaoDocs' doc_types).
    Useful for plugins that read their own config from the shared file.

    Returns:
        Full parsed YAML dictionary, or empty dict if no config file found.
    """
    _load_yaml_config()
    return _yaml_raw_data.copy()


def get_yaml_config_path() -> str | None:
    """
    Get the path to the loaded cacao.yaml file.

    Returns:
        Absolute path string, or None if no config file was found.
    """
    _load_yaml_config()
    return _yaml_config_path


def static_handler(event_name: str, js_code: str) -> None:
    """
    Register a JavaScript event handler for static builds.

    In static mode (GitHub Pages, etc.), there is no Python server.
    This lets apps define client-side JavaScript handlers that run
    when events are dispatched.

    The js_code should be a JavaScript function expression:
        async function(signals, event) { ... }

    Args:
        event_name: The event name (e.g. "chat_send").
        js_code: JavaScript function body.

    Example:
        c.static_handler("chat_send", '''async function(signals, event) {
            const text = event.text;
            const msgs = signals.get("messages") || [];
            signals.set("messages", [...msgs, {role: "user", content: text}]);
        }''')
    """
    _static_handlers[event_name] = js_code


def static_script(js_code: str) -> None:
    """
    Register a JavaScript snippet to be injected in static builds.

    The code runs once when the page loads. Use for initialization,
    registering global handlers, setting up client-side libraries, etc.

    Args:
        js_code: JavaScript code to inject.
    """
    _static_scripts.append(js_code)


def export_static() -> dict[str, Any]:
    """
    Export the app for static HTML generation.

    Returns the app's page structure plus any registered static handlers
    and scripts. Used by `cacao build` to generate standalone HTML.

    Returns:
        Dict with pages, static_handlers, and static_scripts.
    """
    app = _get_app()
    result = app.export_static()
    result["static_handlers"] = dict(_static_handlers)
    result["static_scripts"] = list(_static_scripts)
    return result


# =============================================================================
# Auto-discovery: wrap all ui.py component functions automatically
# =============================================================================

# Functions that are defined manually above or should NOT be auto-wrapped
_MANUAL_FUNCTIONS = {
    # Defined manually in this module (custom logic or renamed)
    "config",
    "signal",
    "computed",
    "on",
    "bind",
    "page",
    "layout",
    "json",
    "json_view",
    "input",
    "input_field",
    "field",
    "date",
    "date_picker",
    "upload",
    "file_upload",
    "line",
    "bar",
    "pie",
    "area",
    "scatter",
    "gauge",
    "load_csv",
    "load_json",
    "sample_sales_data",
    "sample_users_data",
    "run",
    "get_app",
    "is_simple_mode",
    "reset",
    "get_yaml_config",
    "get_yaml_config_path",
    "static_handler",
    "static_script",
    "export_static",
    # Internal ui.py helpers that shouldn't be exposed
    "_add_to_current_container",
    "_container_context",
    "_collect_types",
    "_types_to_categories",
    # Not UI functions (imported into ui.py but not components)
    "dataclass",
    "field",
}

# Collect auto-discovered function names for __all__
_auto_discovered: list[str] = []

_this_module = sys.modules[__name__]

for _name, _fn in inspect.getmembers(_ui_module, inspect.isfunction):
    # Skip private functions, already-defined functions, and non-ui classes
    if _name.startswith("_") or _name in _MANUAL_FUNCTIONS:
        continue
    # Skip if already defined in this module (e.g. from manual section above)
    if hasattr(_this_module, _name):
        continue

    # Detect if it's a context manager (decorated with @contextmanager)
    _is_cm = hasattr(_fn, "__wrapped__") and inspect.isgeneratorfunction(_fn.__wrapped__)

    if _is_cm:
        # Create a context manager wrapper
        def _make_cm_wrapper(fn):
            @contextmanager
            @wraps(fn)
            def wrapper(*args, **kwargs):
                _ensure_context()
                with fn(*args, **kwargs) as comp:
                    yield comp

            return wrapper

        setattr(_this_module, _name, _make_cm_wrapper(_fn))
    else:
        # Create a plain function wrapper
        def _make_wrapper(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                _ensure_context()
                return fn(*args, **kwargs)

            return wrapper

        setattr(_this_module, _name, _make_wrapper(_fn))

    _auto_discovered.append(_name)

# Clean up loop variables from module namespace
del _name, _fn, _is_cm

# =============================================================================
# __all__
# =============================================================================

__all__ = [
    # Config
    "config",
    # State
    "signal",
    "computed",
    "Signal",
    "Computed",
    # Events
    "on",
    "bind",
    # Pages
    "page",
    # Layout preset
    "layout",
    # Renamed / aliased
    "json",
    "json_view",
    "input",
    "input_field",
    "field",
    "date",
    "date_picker",
    "upload",
    "file_upload",
    # Charts
    "line",
    "bar",
    "pie",
    "area",
    "scatter",
    "gauge",
    # Data
    "load_csv",
    "load_json",
    "sample_sales_data",
    "sample_users_data",
    # App
    "run",
    "get_app",
    "is_simple_mode",
    "reset",
    "export_static",
    "static_handler",
    "static_script",
    "get_yaml_config",
    "get_yaml_config_path",
    # Auto-discovered UI components (from ui.py)
    *_auto_discovered,
]
