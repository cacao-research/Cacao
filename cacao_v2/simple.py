"""
Simplified Cacao API.

This module provides a Streamlit-like API where you can write:

    import cacao_v2 as c

    c.title("Hello World")
    with c.row():
        c.metric("Users", 100)
        c.metric("Revenue", "$5K")

No App(), no page(), no boilerplate. Just write components.

For more control, use the full API from cacao_v2.server.ui.
"""

from __future__ import annotations

from typing import Any, Literal, Callable, TypeVar
from contextlib import contextmanager

from .server.signal import Signal, Computed
from .server.ui import (
    App as _App,
    Component,
    # Layout components (context managers)
    row as _row,
    col as _col,
    grid as _grid,
    card as _card,
    sidebar as _sidebar,
    tabs as _tabs,
    tab as _tab,
    # Typography (leaf components)
    title as _title,
    text as _text,
    code as _code,
    divider as _divider,
    spacer as _spacer,
    # Data display
    metric as _metric,
    table as _table,
    json_view as _json_view,
    progress as _progress,
    badge as _badge,
    alert as _alert,
    # Form components
    button as _button,
    input_field as _input_field,
    select as _select,
    checkbox as _checkbox,
    switch as _switch,
    slider as _slider,
    date_picker as _date_picker,
    file_upload as _file_upload,
    # Internal
    _current_container,
    _component_stack,
)

T = TypeVar("T")

# =============================================================================
# Global State
# =============================================================================

# The implicit global app instance (lazily created)
_global_app: _App | None = None

# Configuration set via config()
_global_config: dict[str, Any] = {
    "title": "Cacao App",
    "theme": "dark",
    "host": "127.0.0.1",
    "port": 8000,
}

# Whether we're in "simple mode" (implicit app)
_simple_mode: bool = False


def _get_app() -> _App:
    """Get or create the global app instance."""
    global _global_app, _simple_mode

    if _global_app is None:
        _global_app = _App(
            title=_global_config["title"],
            theme=_global_config["theme"],
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
    theme: Literal["light", "dark", "auto"] | None = None,
    host: str | None = None,
    port: int | None = None,
    debug: bool | None = None,
) -> None:
    """
    Configure the application.

    Call this before any components to set app-level options.

    Example:
        import cacao_v2 as c

        c.config(title="My Dashboard", theme="dark", port=3000)

        c.title("Hello!")

    Args:
        title: Application title (shown in browser tab)
        theme: Color theme - "light", "dark", or "auto"
        host: Host to bind server to (default: 127.0.0.1)
        port: Port for server (default: 8000)
        debug: Enable debug mode with verbose logging
    """
    global _global_config, _global_app

    if title is not None:
        _global_config["title"] = title
    if theme is not None:
        _global_config["theme"] = theme
    if host is not None:
        _global_config["host"] = host
    if port is not None:
        _global_config["port"] = port
    if debug is not None:
        _global_config["debug"] = debug

    # If app already created, update it
    if _global_app is not None:
        if title is not None:
            _global_app.title = title
        if theme is not None:
            _global_app.theme = theme
        if debug is not None:
            _global_app.debug = debug


# =============================================================================
# Signals (State Management)
# =============================================================================

def signal(default: T, *, name: str) -> Signal[T]:
    """
    Create a reactive signal.

    Signals hold state that can change over time. When a signal's value
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

def on(event_name: str):
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
def page(path: str = "/"):
    """
    Define a page at the given path.

    For simple single-page apps, you don't need this - components go to "/" automatically.

    Example:
        import cacao_v2 as c

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
# Layout Components
# =============================================================================

@contextmanager
def row(
    gap: int = 4,
    align: Literal["start", "center", "end", "stretch"] = "center",
    justify: Literal["start", "center", "end", "between", "around"] = "start",
    wrap: bool = False,
    **props: Any,
):
    """
    Horizontal row layout.

    Example:
        with c.row(gap=4):
            c.metric("Users", 100)
            c.metric("Revenue", "$5k")
    """
    _ensure_context()
    with _row(gap=gap, align=align, justify=justify, wrap=wrap, **props) as comp:
        yield comp


@contextmanager
def col(
    span: int | None = None,
    gap: int = 4,
    align: Literal["start", "center", "end", "stretch"] = "stretch",
    **props: Any,
):
    """
    Vertical column layout.

    Example:
        with c.row():
            with c.col(span=8):
                c.chart(...)
            with c.col(span=4):
                c.text("Sidebar")
    """
    _ensure_context()
    with _col(span=span, gap=gap, align=align, **props) as comp:
        yield comp


@contextmanager
def grid(cols: int = 12, gap: int = 4, **props: Any):
    """CSS Grid layout."""
    _ensure_context()
    with _grid(cols=cols, gap=gap, **props) as comp:
        yield comp


@contextmanager
def card(title: str | None = None, subtitle: str | None = None, **props: Any):
    """
    Card container.

    Example:
        with c.card("User Stats"):
            c.metric("Active", 234)
    """
    _ensure_context()
    with _card(title=title, subtitle=subtitle, **props) as comp:
        yield comp


@contextmanager
def sidebar(**props: Any):
    """
    Sidebar container.

    Example:
        with c.sidebar():
            c.select("Filter", ["All", "Active", "Inactive"])
    """
    _ensure_context()
    with _sidebar(**props) as comp:
        yield comp


@contextmanager
def tabs(default: str | None = None, **props: Any):
    """
    Tab container.

    Example:
        with c.tabs(default="overview"):
            with c.tab("overview", "Overview"):
                c.text("Overview content")
            with c.tab("details", "Details"):
                c.text("Details content")
    """
    _ensure_context()
    with _tabs(default=default, **props) as comp:
        yield comp


@contextmanager
def tab(key: str, label: str, icon: str | None = None, **props: Any):
    """Individual tab within tabs()."""
    _ensure_context()
    with _tab(key=key, label=label, icon=icon, **props) as comp:
        yield comp


# =============================================================================
# Typography Components
# =============================================================================

def title(text: str, level: int = 1, **props: Any) -> Component:
    """
    Title/heading.

    Example:
        c.title("Welcome to My App")
        c.title("Section", level=2)
    """
    _ensure_context()
    return _title(text, level=level, **props)


def text(content: str, size: str = "md", color: str | None = None, **props: Any) -> Component:
    """
    Body text.

    Example:
        c.text("Hello world")
        c.text("Muted text", color="muted", size="sm")
    """
    _ensure_context()
    return _text(content, size=size, color=color, **props)


def code(content: str, language: str = "python", **props: Any) -> Component:
    """Syntax-highlighted code block."""
    _ensure_context()
    return _code(content, language=language, **props)


def divider(**props: Any) -> Component:
    """Horizontal divider line."""
    _ensure_context()
    return _divider(**props)


def spacer(size: int = 4, **props: Any) -> Component:
    """Vertical spacer."""
    _ensure_context()
    return _spacer(size=size, **props)


# =============================================================================
# Data Display Components
# =============================================================================

def metric(
    label: str,
    value: Any,
    trend: str | None = None,
    trend_direction: Literal["up", "down", "neutral"] | None = None,
    prefix: str | None = None,
    suffix: str | None = None,
    **props: Any,
) -> Component:
    """
    KPI metric card.

    Example:
        c.metric("Revenue", "$45,231", trend="+20.1%", trend_direction="up")
    """
    _ensure_context()
    return _metric(
        label=label, value=value, trend=trend, trend_direction=trend_direction,
        prefix=prefix, suffix=suffix, **props
    )


def table(
    data: list[dict[str, Any]] | Any,
    columns: list[str] | list[dict[str, Any]] | None = None,
    searchable: bool = False,
    sortable: bool = True,
    paginate: bool = True,
    page_size: int = 10,
    **props: Any,
) -> Component:
    """
    Interactive data table.

    Example:
        c.table(users, columns=["name", "email"], searchable=True)
    """
    _ensure_context()
    return _table(
        data=data, columns=columns, searchable=searchable,
        sortable=sortable, paginate=paginate, page_size=page_size, **props
    )


def json(data: Any, expanded: bool = True, **props: Any) -> Component:
    """
    JSON tree viewer.

    Example:
        c.json({"name": "John", "age": 30})
    """
    _ensure_context()
    return _json_view(data=data, expanded=expanded, **props)


# Alias for backwards compatibility
json_view = json


def progress(
    value: int | float,
    max_value: int | float = 100,
    label: str | None = None,
    show_value: bool = True,
    variant: Literal["line", "circle"] = "line",
    **props: Any,
) -> Component:
    """Progress bar."""
    _ensure_context()
    return _progress(
        value=value, max_value=max_value, label=label,
        show_value=show_value, variant=variant, **props
    )


def badge(
    text: str,
    color: Literal["default", "primary", "success", "warning", "danger", "info"] = "default",
    **props: Any,
) -> Component:
    """Badge/tag."""
    _ensure_context()
    return _badge(text=text, color=color, **props)


def alert(
    message: str,
    type: Literal["info", "success", "warning", "error"] = "info",
    title: str | None = None,
    dismissible: bool = False,
    **props: Any,
) -> Component:
    """Alert message."""
    _ensure_context()
    return _alert(message=message, type=type, title=title, dismissible=dismissible, **props)


# =============================================================================
# Form Components
# =============================================================================

def button(
    label: str,
    on_click: Callable[[], Any] | str | None = None,
    variant: Literal["primary", "secondary", "danger", "ghost", "outline"] = "primary",
    size: Literal["sm", "md", "lg"] = "md",
    disabled: bool = False,
    loading: bool = False,
    icon: str | None = None,
    **props: Any,
) -> Component:
    """
    Button.

    Example:
        c.button("Submit", on_click="submit")
        c.button("Delete", variant="danger")
    """
    _ensure_context()
    return _button(
        label=label, on_click=on_click, variant=variant, size=size,
        disabled=disabled, loading=loading, icon=icon, **props
    )


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
    return _input_field(
        label=label, signal=signal, placeholder=placeholder,
        type=type, disabled=disabled, **props
    )


# Aliases
input_field = input
field = input


def select(
    label: str,
    options: list[str] | list[dict[str, Any]],
    signal: Signal[str] | None = None,
    placeholder: str = "Select...",
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Select dropdown.

    Example:
        c.select("Category", ["All", "Tech", "Finance"])
    """
    _ensure_context()
    return _select(
        label=label, options=options, signal=signal,
        placeholder=placeholder, disabled=disabled, **props
    )


def checkbox(
    label: str,
    signal: Signal[bool] | None = None,
    description: str | None = None,
    disabled: bool = False,
    **props: Any,
) -> Component:
    """Checkbox."""
    _ensure_context()
    return _checkbox(
        label=label, signal=signal, description=description,
        disabled=disabled, **props
    )


def switch(
    label: str,
    signal: Signal[bool] | None = None,
    disabled: bool = False,
    **props: Any,
) -> Component:
    """Toggle switch."""
    _ensure_context()
    return _switch(label=label, signal=signal, disabled=disabled, **props)


def slider(
    label: str,
    signal: Signal[int | float] | None = None,
    min: int | float = 0,
    max: int | float = 100,
    step: int | float = 1,
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Range slider.

    Example:
        volume = c.signal(50, name="volume")
        c.slider("Volume", signal=volume, min=0, max=100)
    """
    _ensure_context()
    return _slider(
        label=label, signal=signal, min_value=min, max_value=max,
        step=step, disabled=disabled, **props
    )


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
    return _date_picker(
        label=label, signal=signal, placeholder=placeholder,
        disabled=disabled, **props
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
    return _file_upload(
        label=label, on_upload=on_upload, accept=accept,
        multiple=multiple, **props
    )


# Alias
file_upload = upload


# =============================================================================
# Charts (re-export from chart module)
# =============================================================================

def _lazy_chart_import():
    """Lazy import chart functions to avoid circular imports."""
    from .server import chart as _chart_module
    return _chart_module


def line(data, x: str, y: str | list[str], **props):
    """Line chart."""
    _ensure_context()
    return _lazy_chart_import().line(data, x=x, y=y, **props)


def bar(data, x: str, y: str | list[str], **props):
    """Bar chart."""
    _ensure_context()
    return _lazy_chart_import().bar(data, x=x, y=y, **props)


def pie(data, values: str, names: str, **props):
    """Pie chart."""
    _ensure_context()
    return _lazy_chart_import().pie(data, values=values, names=names, **props)


def area(data, x: str, y: str | list[str], **props):
    """Area chart."""
    _ensure_context()
    return _lazy_chart_import().area(data, x=x, y=y, **props)


def scatter(data, x: str, y: str, **props):
    """Scatter chart."""
    _ensure_context()
    return _lazy_chart_import().scatter(data, x=x, y=y, **props)


def gauge(value: float, **props):
    """Gauge chart."""
    _ensure_context()
    return _lazy_chart_import().gauge(value, **props)


# =============================================================================
# Data Utilities (re-export from data module)
# =============================================================================

def _lazy_data_import():
    """Lazy import data functions."""
    from .server import data as _data_module
    return _data_module


def load_csv(path: str):
    """Load data from CSV file."""
    return _lazy_data_import().load_csv(path)


def load_json(path: str):
    """Load data from JSON file."""
    return _lazy_data_import().load_json(path)


def sample_sales_data():
    """Get sample sales data for demos."""
    return _lazy_data_import().sample_sales_data()


def sample_users_data():
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
        import cacao_v2 as c

        c.title("Hello")
        c.run(port=3000)

    Args:
        host: Host to bind to (default: from config or 127.0.0.1)
        port: Port to listen on (default: from config or 8000)
        reload: Enable hot reload
    """
    app = _get_app()

    # Use config values as defaults
    final_host = host or _global_config.get("host", "127.0.0.1")
    final_port = port or _global_config.get("port", 8000)

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
    _global_app = None
    _simple_mode = False
    _global_config = {
        "title": "Cacao App",
        "theme": "dark",
        "host": "127.0.0.1",
        "port": 8000,
    }


# =============================================================================
# Exports
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
    # Layout
    "row",
    "col",
    "grid",
    "card",
    "sidebar",
    "tabs",
    "tab",
    # Typography
    "title",
    "text",
    "code",
    "divider",
    "spacer",
    # Data Display
    "metric",
    "table",
    "json",
    "json_view",
    "progress",
    "badge",
    "alert",
    # Forms
    "button",
    "input",
    "input_field",
    "field",
    "select",
    "checkbox",
    "switch",
    "slider",
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
]
