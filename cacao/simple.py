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
from .server.ui import (
    col as _ui_col,
)
from .server.ui import (
    row as _ui_row,
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
            debug=_global_config.get("debug", False),
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
            _global_app.theme = theme  # type: ignore[assignment]
        if branding is not None:
            _global_app.branding = branding  # type: ignore[assignment]
        if debug is not None:
            _global_app.debug = debug


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


def use(middleware: Any = None) -> Any:
    """
    Add middleware to the event processing chain.

    Middleware intercepts events before they reach handlers. Useful for
    logging, authentication, rate limiting, validation, and more.

    Can be used as a decorator or called directly.

    Example:
        @c.use
        async def log_events(ctx, next):
            print(f"Event: {ctx.event_name}")
            await next(ctx)

    Args:
        middleware: The middleware function

    Returns:
        The middleware function (for decorator use)
    """
    app = _get_app()
    return app.use(middleware)


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
        with _ui_col(gap=4, width=width):
            yield

    @contextmanager
    def main(self) -> Generator[None, None, None]:
        """Main content region."""
        with _ui_col(gap=0):
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
        with _ui_col(gap=4, flex=str(left_flex)):
            yield

    @contextmanager
    def right(self) -> Generator[None, None, None]:
        """Right pane of a split layout."""
        _, right_flex = self._parse_ratio()
        with _ui_col(gap=4, flex=str(right_flex)):
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
        with _ui_row(gap=gap, align="start", wrap=False, **props):
            yield helper
    elif preset == "centered":
        from .server.ui import container as _container

        with _container(size="md", **props):
            yield helper
    elif preset == "split":
        with _ui_row(gap=gap, align="stretch", wrap=False, **props):
            yield helper
    elif preset == "dashboard":
        from .server.ui import grid as _grid

        with _grid(cols=12, gap=gap, **props):
            yield helper
    else:
        with _ui_row(gap=gap, **props):
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
    result: dict[str, Any] = {
        "pages": app.get_all_pages(),
        "metadata": {
            "title": app.title,
            "theme": app.theme,
            "branding": app.branding,
        },
        "signals": {s.name: s.default for s in Signal.get_all_signals().values()},
        "static_handlers": dict(_static_handlers),
        "static_scripts": list(_static_scripts),
    }
    return result


# =============================================================================
# Plugin Registry
# =============================================================================


def register_plugin(
    name: str,
    *,
    version: str = "0.0.0",
    description: str = "",
    author: str = "",
    config_schema: dict[str, Any] | None = None,
    **metadata: Any,
) -> Any:
    """
    Register a Cacao plugin.

    Plugins can register lifecycle hooks, inject UI into slots,
    and add middleware for event interception.

    Args:
        name: Unique plugin name (e.g. "cacaodocs")
        version: Plugin version
        description: Short description
        author: Plugin author
        config_schema: Expected config keys in cacao.yaml
        **metadata: Additional metadata

    Returns:
        Plugin instance with .on(), .inject(), .add_middleware() methods

    Example:
        plugin = c.register_plugin(
            "cacaodocs",
            version="0.1.19",
            description="Documentation generator for Cacao apps",
        )
        plugin.on("on_ready", lambda: print("CacaoDocs ready!"))
    """
    from .server.plugin import get_registry

    return get_registry().register(
        name,
        version=version,
        description=description,
        author=author,
        config_schema=config_schema,
        **metadata,
    )


def get_plugins() -> dict[str, Any]:
    """
    Get all registered plugins.

    Returns:
        Dict of plugin name -> Plugin instance
    """
    from .server.plugin import get_registry

    return get_registry().all()


def get_plugin(name: str) -> Any:
    """
    Get a specific registered plugin by name.

    Returns:
        Plugin instance or None
    """
    from .server.plugin import get_registry

    return get_registry().get(name)


# =============================================================================
# Keyboard Shortcuts
# =============================================================================


def shortcut(combo: str, handler: Callable[..., Any], description: str = "") -> None:
    """
    Register a keyboard shortcut.

    The shortcut triggers a server-side event handler when pressed.

    Args:
        combo: Key combination (e.g., "mod+s", "mod+shift+p")
        handler: Async function(session, event) to call
        description: Human-readable description

    Example:
        @c.on("save_shortcut")
        async def save(session, event):
            print("Save triggered!")

        c.shortcut("mod+s", save, "Save")
    """
    app = _get_app()
    # Generate a unique event name for this shortcut
    event_name = f"shortcut:{combo.replace('+', '_')}"
    app._shortcuts.append(
        {
            "combo": combo,
            "event_name": event_name,
            "description": description,
        }
    )
    # Register the handler for this event
    app.events.register(event_name, handler)


# =============================================================================
# Theme API
# =============================================================================


def register_theme(name: str, variables: dict[str, str]) -> None:
    """
    Register a custom theme.

    Themes are CSS custom property overrides applied via `data-theme` attribute.
    Use `c.config(theme="name")` to set the default, or let users toggle via AppShell.

    Args:
        name: Theme name (e.g., "ocean", "sunset")
        variables: CSS variable overrides (e.g., {"bg-primary": "#0a1628", "primary": "#4fc3f7"})

    Example:
        c.register_theme("ocean", {
            "bg-primary": "#0a1628",
            "primary": "#4fc3f7",
            "text-primary": "#e0f7fa",
        })
    """
    app = _get_app()
    app._custom_themes[name] = variables


# =============================================================================
# Notifications
# =============================================================================


def notify(
    message: str,
    title: str = "",
    variant: str = "info",
    *,
    session: Any = None,
    broadcast: bool = False,
) -> None:
    """
    Send a persistent notification to the client.

    Unlike toasts, notifications persist in a notification center panel
    until dismissed by the user.

    Args:
        message: Notification message
        title: Optional title
        variant: One of 'info', 'success', 'warning', 'error'
        session: Specific session to notify (required if not broadcast)
        broadcast: Send to all connected sessions

    Example:
        c.notify("Build complete", "3 docs updated", variant="success", broadcast=True)
    """
    import asyncio

    app = _get_app()
    msg = {
        "type": "notification",
        "title": title,
        "message": message,
        "variant": variant,
    }

    if broadcast:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(app.sessions.broadcast(msg))
        except RuntimeError:
            pass
    elif session is not None:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(session.send(msg))
        except RuntimeError:
            pass


# =============================================================================
# IPC / Cross-Plugin Messaging
# =============================================================================


def emit(topic: str, data: Any = None) -> None:
    """
    Emit an event on the server-side event bus.

    Used for inter-plugin communication. Never touches WebSocket.

    Args:
        topic: Event topic (e.g., "docs:updated")
        data: Arbitrary data payload

    Example:
        c.emit("docs:updated", {"count": 42})
    """
    from .server.plugin import get_event_bus

    get_event_bus().emit(topic, data)


def listen(topic: str, handler: Callable[..., Any]) -> Callable[[], None]:
    """
    Listen for events on the server-side event bus.

    Returns an unlisten function.

    Args:
        topic: Event topic to listen for
        handler: Function to call with event data

    Returns:
        Unlisten function

    Example:
        def on_docs_updated(data):
            print(f"Updated {data['count']} docs")

        unlisten = c.listen("docs:updated", on_docs_updated)
    """
    from .server.plugin import get_event_bus

    return get_event_bus().listen(topic, handler)


# =============================================================================
# Auth & Permissions
# =============================================================================


def require_auth(
    provider: Any = None,
    *,
    users: dict[str, dict[str, Any]] | None = None,
    public_events: set[str] | None = None,
) -> None:
    """
    Enable authentication for the app.

    Either pass a custom AuthProvider or use the simple username/password mode.

    Args:
        provider: AuthProvider instance (optional)
        users: Dict of username -> {"password": "...", "permissions": [...]} for simple auth
        public_events: Event names that don't require auth

    Example:
        c.require_auth(users={
            "admin": {"password": "secret", "permissions": ["admin"]},
            "user": {"password": "pass123"},
        })
    """
    from .server.auth import SimpleAuthProvider, set_auth_provider

    if provider is None and users:
        provider = SimpleAuthProvider(users)

    if provider:
        set_auth_provider(provider, public_events)


def permission(perm: str) -> Callable[..., Any]:
    """
    Decorator to require a permission on an event handler.

    Args:
        perm: Required permission name

    Example:
        @c.on("delete_user")
        @c.permission("admin")
        async def delete_user(session, event):
            ...
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(session: Any, data: dict[str, Any]) -> None:
            if perm not in session.permissions:
                await session.send(
                    {
                        "type": "error",
                        "message": f"Permission required: {perm}",
                        "code": "PERMISSION_DENIED",
                    }
                )
                return
            await func(session, data)

        return wrapper

    return decorator


# =============================================================================
# Interface (Function Wrapping)
# =============================================================================


def interface(
    fn: Callable[..., Any],
    *,
    title: str | None = None,
    description: str | None = None,
    submit_label: str = "Submit",
    layout: Literal["auto", "horizontal", "vertical"] = "auto",
    examples: list[list[Any]] | None = None,
    cache: bool = False,
    flagging: bool = False,
    flagging_dir: str = "./flags/",
    live: bool = False,
    timeout: float = 60.0,
) -> Component:
    """
    Wrap a Python function into a full interactive UI.

    Inspects type hints, defaults, and docstring to auto-generate
    input fields and output displays. Fully composable.

    Example:
        def greet(name: str, excited: bool = False) -> str:
            greeting = f"Hello, {name}!"
            return greeting.upper() if excited else greeting

        c.interface(greet)

    Args:
        fn: The function to wrap
        title: Display title (default: from function name)
        description: Description (default: from docstring)
        submit_label: Submit button text
        layout: "auto", "horizontal", or "vertical"
        examples: List of example input lists
        cache: Cache results per session
        flagging: Enable output flagging
        flagging_dir: Directory for flagged data
        live: Auto-submit on input change
        timeout: Max execution time in seconds
    """
    _ensure_context()
    from .server.interface import interface as _interface_fn

    return _interface_fn(
        fn,
        title=title,
        description=description,
        submit_label=submit_label,
        layout=layout,
        examples=examples,
        cache=cache,
        flagging=flagging,
        flagging_dir=flagging_dir,
        live=live,
        timeout=timeout,
    )


def parallel(
    *fns: Callable[..., Any],
    titles: list[str] | None = None,
    **kwargs: Any,
) -> Component:
    """Run multiple functions side-by-side."""
    _ensure_context()
    from .server.interface import parallel as _parallel_fn
    return _parallel_fn(*fns, titles=titles, **kwargs)


def series(
    *fns: Callable[..., Any],
    titles: list[str] | None = None,
    **kwargs: Any,
) -> Component:
    """Chain functions — output of each feeds into the next."""
    _ensure_context()
    from .server.interface import series as _series_fn
    return _series_fn(*fns, titles=titles, **kwargs)


def compare(
    *fns: Callable[..., Any],
    titles: list[str] | None = None,
    **kwargs: Any,
) -> Component:
    """Run same inputs through multiple functions, compare outputs."""
    _ensure_context()
    from .server.interface import compare as _compare_fn
    return _compare_fn(*fns, titles=titles, **kwargs)


# =============================================================================
# Chat (LLM Integration)
# =============================================================================


def chat(
    signal: Signal[list[Any]] | None = None,
    on_send: Callable[..., Any] | str | None = None,
    on_clear: Callable[..., Any] | str | None = None,
    placeholder: str = "Type a message...",
    title: str | None = None,
    height: str = "500px",
    show_clear: bool = False,
    provider: str | None = None,
    model: str | None = None,
    system_prompt: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    tools: list[Any] | None = None,
    tool_handlers: dict[str, Callable[..., Any]] | None = None,
    max_history: int = 100,
    max_cost: float | None = None,
    max_budget_tokens: int | None = None,
    fallback_model: str | None = None,
    **props: Any,
) -> Component:
    """
    Interactive chat component with optional LLM streaming.

    Without ``provider``, works as a manual chat (use ``on_send`` handler).
    With ``provider``, automatically streams LLM responses.

    Supports all Prompture providers: openai, anthropic/claude, google/gemini,
    groq, grok/xai, ollama, lmstudio, azure, openrouter, and more.

    Example (auto LLM):
        c.chat(provider="openai", model="gpt-4o", system_prompt="You are helpful.")

    Example (with budget):
        c.chat(provider="openai", model="gpt-4o", max_cost=1.00, fallback_model="gpt-4o-mini")

    Args:
        provider: LLM provider name (15+ supported via Prompture)
        model: Model name (e.g. "gpt-4o", "claude-sonnet-4-20250514")
        system_prompt: System message for the LLM
        api_key: API key (or set via environment variable)
        tools: List of ToolSpec for function calling
        tool_handlers: Dict mapping tool names to handler functions
        max_cost: Maximum USD cost per session before stopping.
        max_budget_tokens: Maximum total tokens per session.
        fallback_model: Cheaper model to auto-degrade to at 80% budget.
    """
    _ensure_context()
    from .server.ui import chat as _ui_chat

    return _ui_chat(
        signal=signal,
        on_send=on_send,
        on_clear=on_clear,
        placeholder=placeholder,
        title=title,
        height=height,
        show_clear=show_clear,
        provider=provider,
        model=model,
        system_prompt=system_prompt,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=tools,
        tool_handlers=tool_handlers,
        max_history=max_history,
        max_cost=max_cost,
        max_budget_tokens=max_budget_tokens,
        fallback_model=fallback_model,
        **props,
    )


# =============================================================================
# Stream wrapper
# =============================================================================


def stream(
    fn: Callable[..., Any],
    *,
    signal: Signal[list[Any]] | None = None,
    title: str | None = None,
    placeholder: str = "Type a message...",
    height: str = "500px",
    show_clear: bool = False,
    **props: Any,
) -> Component:
    """
    Stream a function's output token-by-token into a chat UI.

    The function should be a generator or async generator that yields
    string chunks. The first positional argument receives the user's text.

    Example:
        def my_llm(prompt: str):
            for token in call_api(prompt):
                yield token

        c.stream(my_llm, title="My Streaming App")
    """
    _ensure_context()
    from .server.llm import stream_to_chat
    from .server.ui import chat as _ui_chat

    # Create signal for this stream instance
    from .server.signal import Signal as _Signal

    sig_name = f"stream_{id(fn)}"
    if signal is None:
        signal = _Signal([], name=sig_name)

    # Register the streaming function as the on_send handler
    async def _handle_stream(session: Any, data: dict[str, Any]) -> None:
        text = data.get("text", "")
        if not text:
            return
        # Add user message first
        history = list(signal.get(session))
        history.append({"role": "user", "content": text})
        signal.set(session, history)
        # Stream the function
        await stream_to_chat(session, signal, fn, text)

    # Use the event system
    event_name = f"Chat:on_send_{sig_name}"
    app = _get_app()
    app.events.register(event_name, _handle_stream)

    return _ui_chat(
        signal=signal,
        on_send=event_name,
        placeholder=placeholder,
        title=title,
        height=height,
        show_clear=show_clear,
        **props,
    )


# =============================================================================
# Structured Extraction
# =============================================================================


def extract(
    schema: dict[str, Any] | None = None,
    *,
    pydantic_model: Any = None,
    provider: str = "openai",
    model: str = "gpt-4o",
    api_key: str | None = None,
    title: str = "Extract",
    description: str = "",
    submit_label: str = "Extract",
    height: str = "400px",
    **props: Any,
) -> Component:
    """
    Structured extraction UI — paste text and extract structured data.

    Uses Prompture to extract data matching a JSON Schema or Pydantic model.

    Example:
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }
        c.extract(schema, provider="openai", model="gpt-4o")

    Args:
        schema: JSON Schema for desired output.
        pydantic_model: A Pydantic BaseModel class (alternative to schema).
        provider: LLM provider name.
        model: Model name.
    """
    _ensure_context()
    from .server.ui import extract as _ui_extract

    return _ui_extract(
        schema=schema,
        pydantic_model=pydantic_model,
        provider=provider,
        model=model,
        api_key=api_key,
        title=title,
        description=description,
        submit_label=submit_label,
        height=height,
        **props,
    )


# =============================================================================
# Cost Dashboard
# =============================================================================


def cost_dashboard(
    *,
    title: str = "Usage & Costs",
    show_budget: bool = True,
    show_breakdown: bool = True,
    compact: bool = False,
    **props: Any,
) -> Component:
    """
    Cost tracking dashboard — per-session token counts, USD costs, model comparison.

    Example:
        c.cost_dashboard(title="API Usage")
    """
    _ensure_context()
    from .server.ui import cost_dashboard as _ui_cost_dashboard

    return _ui_cost_dashboard(
        title=title,
        show_budget=show_budget,
        show_breakdown=show_breakdown,
        compact=compact,
        **props,
    )


# =============================================================================
# Document Upload
# =============================================================================


def document_upload(
    *,
    schema: dict[str, Any] | None = None,
    provider: str = "openai",
    model: str = "gpt-4o",
    api_key: str | None = None,
    title: str = "Document Upload",
    accept: str = ".pdf,.docx,.csv,.xlsx,.md,.txt,.html",
    show_preview: bool = True,
    extract_on_upload: bool = False,
    **props: Any,
) -> Component:
    """
    Document ingestion — upload PDF, DOCX, CSV, etc. and extract structured data.

    Example:
        schema = {"type": "object", "properties": {"summary": {"type": "string"}}}
        c.document_upload(schema=schema, extract_on_upload=True)
    """
    _ensure_context()
    from .server.ui import document_upload as _ui_document_upload

    return _ui_document_upload(
        schema=schema,
        provider=provider,
        model=model,
        api_key=api_key,
        title=title,
        accept=accept,
        show_preview=show_preview,
        extract_on_upload=extract_on_upload,
        **props,
    )


# =============================================================================
# Model Picker
# =============================================================================


def model_picker(
    *,
    signal: Signal[str] | None = None,
    label: str = "Model",
    grouped: bool = True,
    default: str | None = None,
    **props: Any,
) -> Component:
    """
    Model discovery picker — auto-detect available providers/models.

    Example:
        model = c.signal("openai/gpt-4o", name="selected_model")
        c.model_picker(signal=model)
    """
    _ensure_context()
    from .server.ui import model_picker as _ui_model_picker

    return _ui_model_picker(
        signal=signal,
        label=label,
        grouped=grouped,
        default=default,
        **props,
    )


# =============================================================================
# Agent Components (Phase 8.4)
# =============================================================================


def agent(
    *,
    provider: str = "openai",
    model: str = "gpt-4o",
    system_prompt: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    tools: list[Any] | None = None,
    tool_handlers: dict[str, Callable[..., Any]] | None = None,
    max_iterations: int = 10,
    max_cost: float | None = None,
    max_budget_tokens: int | None = None,
    fallback_model: str | None = None,
    title: str | None = None,
    placeholder: str = "Ask the agent...",
    height: str = "600px",
    show_steps: bool = True,
    show_cost: bool = True,
    **props: Any,
) -> Component:
    """
    Wrap a Prompture Agent with ReAct loop visualization.

    Example:
        c.agent(provider="openai", model="gpt-4o", system_prompt="You are helpful.")

    Example (with tools):
        from cacao.server.llm import ToolSpec
        tool = ToolSpec(name="search", description="Search the web", parameters={...})
        c.agent(provider="openai", model="gpt-4o", tools=[tool], tool_handlers={"search": fn})
    """
    _ensure_context()
    from .server.ui import agent as _ui_agent

    return _ui_agent(
        provider=provider,
        model=model,
        system_prompt=system_prompt,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=tools,
        tool_handlers=tool_handlers,
        max_iterations=max_iterations,
        max_cost=max_cost,
        max_budget_tokens=max_budget_tokens,
        fallback_model=fallback_model,
        title=title,
        placeholder=placeholder,
        height=height,
        show_steps=show_steps,
        show_cost=show_cost,
        **props,
    )


def multi_agent(
    *,
    mode: str = "debate",
    agents: list[dict[str, Any]] | None = None,
    agent_names: list[str] | None = None,
    rounds: int = 3,
    router_prompt: str | None = None,
    title: str | None = None,
    height: str = "600px",
    **props: Any,
) -> Component:
    """
    Multi-agent UI — debate view, router dashboard, or pipeline monitor.

    Example:
        c.multi_agent(
            mode="debate",
            agents=[
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "Optimistic."},
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "Skeptical."},
            ],
            agent_names=["Optimist", "Skeptic"],
        )
    """
    _ensure_context()
    from .server.ui import multi_agent as _ui_multi_agent

    return _ui_multi_agent(
        mode=mode,
        agents=agents,
        agent_names=agent_names,
        rounds=rounds,
        router_prompt=router_prompt,
        title=title,
        height=height,
        **props,
    )


def tool_timeline(
    *,
    agent_id: str | None = None,
    title: str = "Tool Call Timeline",
    height: str = "400px",
    show_args: bool = True,
    show_results: bool = True,
    show_cost: bool = True,
    compact: bool = False,
    **props: Any,
) -> Component:
    """
    Visual trace of agent reasoning steps and tool invocations.

    Example:
        c.tool_timeline(agent_id="my_agent")
    """
    _ensure_context()
    from .server.ui import tool_timeline as _ui_tool_timeline

    return _ui_tool_timeline(
        agent_id=agent_id,
        title=title,
        height=height,
        show_args=show_args,
        show_results=show_results,
        show_cost=show_cost,
        compact=compact,
        **props,
    )


def budget_gauge(
    *,
    max_cost: float | None = None,
    max_tokens: int | None = None,
    warn_threshold: float = 0.8,
    title: str = "Budget",
    show_breakdown: bool = True,
    compact: bool = False,
    **props: Any,
) -> Component:
    """
    Real-time cost/token usage widget with threshold alerts.

    Example:
        c.budget_gauge(max_cost=5.00, max_tokens=100000)
    """
    _ensure_context()
    from .server.ui import budget_gauge as _ui_budget_gauge

    return _ui_budget_gauge(
        max_cost=max_cost,
        max_tokens=max_tokens,
        warn_threshold=warn_threshold,
        title=title,
        show_breakdown=show_breakdown,
        compact=compact,
        **props,
    )


# Re-export I/O marker types for use in function signatures
from .server.interface import Audio, Code, DataFrame, File, Image, Markdown, Plot, Video  # noqa: E402

# Re-export LLM types for tool calling
from .server.llm import ChatConfig, ToolSpec  # noqa: E402


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
    "chat",
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
    # Plugin registry
    "register_plugin",
    "get_plugins",
    "get_plugin",
    # Middleware
    "use",
    # Shortcuts
    "shortcut",
    # Themes
    "register_theme",
    # Notifications
    "notify",
    # IPC
    "emit",
    "listen",
    # Auth
    "require_auth",
    "permission",
    # Interface
    "interface",
    "parallel",
    "series",
    "compare",
    # AI / Prompture
    "extract",
    "cost_dashboard",
    "document_upload",
    "model_picker",
    # Agent Components
    "agent",
    "multi_agent",
    "tool_timeline",
    "budget_gauge",
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
        def _make_cm_wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
            @contextmanager
            @wraps(fn)
            def wrapper(*args: Any, **kwargs: Any) -> Generator[Any, None, None]:
                _ensure_context()
                with fn(*args, **kwargs) as comp:
                    yield comp

            return wrapper

        setattr(_this_module, _name, _make_cm_wrapper(_fn))
    else:
        # Create a plain function wrapper
        def _make_wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(fn)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
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
    # Middleware
    "use",
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
    # Plugin registry
    "register_plugin",
    "get_plugins",
    "get_plugin",
    # Shortcuts
    "shortcut",
    # Themes
    "register_theme",
    # Notifications
    "notify",
    # IPC
    "emit",
    "listen",
    # Auth
    "require_auth",
    "permission",
    # Interface
    "interface",
    "parallel",
    "series",
    "compare",
    # Chat & LLM
    "chat",
    "stream",
    "ChatConfig",
    "ToolSpec",
    # AI / Prompture
    "extract",
    "cost_dashboard",
    "document_upload",
    "model_picker",
    # Tukuy Skills
    "skill",
    "skill_browser",
    "chain_builder",
    "safety_policy",
    # Agent Components
    "agent",
    "multi_agent",
    "tool_timeline",
    "budget_gauge",
    "DataFrame",
    "Image",
    "Audio",
    "Video",
    "Code",
    "Markdown",
    "Plot",
    "File",
    # Auto-discovered UI components (from ui.py)
    *_auto_discovered,
]
