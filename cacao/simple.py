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

from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Any, Literal, TypeVar

from .server.signal import Computed, Signal
from .server.ui import (
    App as _App,
)
from .server.ui import (
    Component,
    _current_container,
)
from .server.ui import (
    alert as _alert,
)
from .server.ui import (
    # Admin layout components
    app_shell as _app_shell,
)
from .server.ui import (
    badge as _badge,
)
from .server.ui import (
    # Form components
    button as _button,
)
from .server.ui import (
    card as _card,
)
from .server.ui import (
    chat as _chat,
)
from .server.ui import (
    checkbox as _checkbox,
)
from .server.ui import (
    code as _code,
)
from .server.ui import (
    col as _col,
)
from .server.ui import (
    date_picker as _date_picker,
)
from .server.ui import (
    divider as _divider,
)
from .server.ui import (
    file_upload as _file_upload,
)
from .server.ui import (
    grid as _grid,
)
from .server.ui import (
    html as _html,
)
from .server.ui import (
    input_field as _input_field,
)
from .server.ui import (
    json_view as _json_view,
)
from .server.ui import (
    markdown as _markdown,
)
from .server.ui import (
    # Data display
    metric as _metric,
)
from .server.ui import (
    nav_group as _nav_group,
)
from .server.ui import (
    nav_item as _nav_item,
)
from .server.ui import (
    nav_panel as _nav_panel,
)
from .server.ui import (
    nav_sidebar as _nav_sidebar,
)
from .server.ui import (
    progress as _progress,
)
from .server.ui import (
    raw_html as _raw_html,
)
from .server.ui import (
    # Layout components (context managers)
    row as _row,
)
from .server.ui import (
    select as _select,
)
from .server.ui import (
    shell_content as _shell_content,
)
from .server.ui import (
    sidebar as _sidebar,
)
from .server.ui import (
    slider as _slider,
)
from .server.ui import (
    spacer as _spacer,
)
from .server.ui import (
    switch as _switch,
)
from .server.ui import (
    tab as _tab,
)
from .server.ui import (
    table as _table,
)
from .server.ui import (
    tabs as _tabs,
)
from .server.ui import (
    text as _text,
)
from .server.ui import (
    textarea as _textarea,
)
from .server.ui import (
    # Typography (leaf components)
    title as _title,
)
from .server.ui import (
    # Toast
    toast as _toast,
)
from .server.ui import (
    # Content components
    accordion as _accordion,
)
from .server.ui import (
    accordion_item as _accordion_item,
)
from .server.ui import (
    steps as _steps,
)
from .server.ui import (
    step as _step,
)
from .server.ui import (
    file_tree as _file_tree,
)
from .server.ui import (
    link_card as _link_card,
)
from .server.ui import (
    # General UI components
    modal as _modal,
)
from .server.ui import (
    tooltip as _tooltip,
)
from .server.ui import (
    breadcrumb as _breadcrumb,
)
from .server.ui import (
    image as _image,
)
from .server.ui import (
    # Nice-to-Have components
    timeline as _timeline,
)
from .server.ui import (
    timeline_item as _timeline_item,
)
from .server.ui import (
    video as _video,
)
from .server.ui import (
    diff as _diff,
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
    "port": 1502,  # 1502: Columbus encounters cacao in Honduras
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
    theme: Literal["light", "dark", "auto"] | None = None,
    host: str | None = None,
    port: int | None = None,
    debug: bool | None = None,
    branding: bool | str | None = None,
) -> None:
    """
    Configure the application.

    Call this before any components to set app-level options.

    Example:
        import cacao as c

        c.config(title="My Dashboard", theme="dark", port=3000)

        c.title("Hello!")

    Args:
        title: Application title (shown in browser tab)
        theme: Color theme - "light", "dark", or "auto"
        host: Host to bind server to (default: 127.0.0.1)
        port: Port for server (default: 1502 - historic chocolate year)
        debug: Enable debug mode with verbose logging
        branding: Show branding badge. True for default "Built with Cacao",
                  or a custom HTML string. False to disable.
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
    if branding is not None:
        _global_config["branding"] = branding

    # If app already created, update it
    if _global_app is not None:
        if title is not None:
            _global_app.title = title
        if theme is not None:
            _global_app.theme = theme
        if debug is not None:
            _global_app.debug = debug
        if branding is not None:
            _global_app.branding = branding


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
# Layout Components
# =============================================================================


@contextmanager
def row(
    gap: int = 4,
    align: Literal["start", "center", "end", "stretch"] = "center",
    justify: Literal["start", "center", "end", "between", "around"] = "start",
    wrap: bool = False,
    **props: Any,
) -> Generator[Component, None, None]:
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
) -> Generator[Component, None, None]:
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
def grid(cols: int = 12, gap: int = 4, **props: Any) -> Generator[Component, None, None]:
    """CSS Grid layout."""
    _ensure_context()
    with _grid(cols=cols, gap=gap, **props) as comp:
        yield comp


@contextmanager
def card(
    title: str | None = None, subtitle: str | None = None, **props: Any
) -> Generator[Component, None, None]:
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
def sidebar(**props: Any) -> Generator[Component, None, None]:
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
def tabs(default: str | None = None, **props: Any) -> Generator[Component, None, None]:
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
def tab(
    key: str, label: str, icon: str | None = None, **props: Any
) -> Generator[Component, None, None]:
    """Individual tab within tabs()."""
    _ensure_context()
    with _tab(key=key, label=label, icon=icon, **props) as comp:
        yield comp


# =============================================================================
# Admin Layout Components
# =============================================================================


@contextmanager
def app_shell(
    brand: str | None = None,
    logo: str | None = None,
    default: str | None = None,
    theme_dark: str | None = None,
    theme_light: str | None = None,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Admin-style application shell with sidebar navigation.

    Args:
        brand: Brand name shown in sidebar header.
        logo: URL to logo image.
        default: Default active nav item key.
        theme_dark: Dark theme name for the toggle (e.g. "tukuy").
        theme_light: Light theme name for the toggle (e.g. "tukuy-light").

    Example:
        with c.app_shell(brand="My App", default="dashboard",
                         theme_dark="dark", theme_light="light"):
            with c.nav_sidebar():
                with c.nav_group("Tools"):
                    c.nav_item("Dashboard", key="dashboard")
            with c.shell_content():
                with c.nav_panel("dashboard"):
                    c.title("Dashboard")
    """
    _ensure_context()
    with _app_shell(
        brand=brand,
        logo=logo,
        default=default,
        theme_dark=theme_dark,
        theme_light=theme_light,
        **props,
    ) as comp:
        yield comp


@contextmanager
def nav_sidebar(**props: Any) -> Generator[Component, None, None]:
    """Navigation sidebar for app_shell."""
    _ensure_context()
    with _nav_sidebar(**props) as comp:
        yield comp


@contextmanager
def nav_group(
    label: str,
    icon: str | None = None,
    default_open: bool = True,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Collapsible navigation group.

    Example:
        with c.nav_group("Encoders", icon="code"):
            c.nav_item("Base64", key="base64")
    """
    _ensure_context()
    with _nav_group(label=label, icon=icon, default_open=default_open, **props) as comp:
        yield comp


def nav_item(
    label: str,
    key: str,
    icon: str | None = None,
    badge: str | None = None,
    **props: Any,
) -> Component:
    """
    Navigation item.

    Example:
        c.nav_item("Base64 Encoder", key="base64", icon="code")
    """
    _ensure_context()
    return _nav_item(label=label, key=key, icon=icon, badge=badge, **props)


@contextmanager
def shell_content(**props: Any) -> Generator[Component, None, None]:
    """Main content area of app_shell."""
    _ensure_context()
    with _shell_content(**props) as comp:
        yield comp


@contextmanager
def nav_panel(key: str, **props: Any) -> Generator[Component, None, None]:
    """
    Content panel that shows when the nav_item with matching key is active.

    Example:
        with c.shell_content():
            with c.nav_panel("dashboard"):
                c.title("Dashboard")
    """
    _ensure_context()
    with _nav_panel(key=key, **props) as comp:
        yield comp


# =============================================================================
# Layout Presets
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
    max_width: str = "600px",
    ratio: str = "1:1",
    height: str = "calc(100vh - 4rem)",
    gap: int = 4,
    **props: Any,
) -> Generator[_LayoutHelper, None, None]:
    """
    Pre-built layout preset for common patterns.

    Presets:
        "sidebar"   - Side panel + main content, full viewport height
        "centered"  - Centered content with max-width (forms, login)
        "split"     - Two-pane split with custom ratio
        "dashboard" - Full viewport dashboard layout

    Example:
        # Sidebar layout (like the chat app)
        with c.layout("sidebar", sidebar_width="300px") as l:
            with l.side():
                c.card(title="Settings")
            with l.main():
                c.chat(...)

        # Centered form
        with c.layout("centered", max_width="500px"):
            c.title("Login")
            c.input("Email")

        # Split pane
        with c.layout("split", ratio="1:2") as l:
            with l.left():
                c.text("Editor")
            with l.right():
                c.text("Preview")
    """
    _ensure_context()
    helper = _LayoutHelper(preset, sidebar_width=sidebar_width, ratio=ratio)

    if preset == "sidebar":
        with row(gap=gap, wrap=False, height=height, **props):
            yield helper

    elif preset == "centered":
        with row(justify="center", gap=gap, height=height, **props):
            with col(
                gap=gap,
                max_width=max_width,
                width="100%",
                align="stretch",
            ):
                yield helper

    elif preset == "split":
        with row(gap=gap, wrap=False, height=height, **props):
            yield helper

    elif preset == "dashboard":
        with col(gap=gap, height=height, **props):
            yield helper

    else:
        raise ValueError(f"Unknown layout preset: {preset!r}")


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


def html(content: str, **props: Any) -> Component:
    """
    Render pre-rendered HTML with prose styling.

    Applies full prose typography. For raw HTML without styling, use raw_html().
    For rendering markdown source, use markdown().
    """
    _ensure_context()
    return _html(content, **props)


def raw_html(content: str, **props: Any) -> Component:
    """
    Render raw HTML with zero styling.

    For embedding widgets, iframes, or custom HTML that manages its own styling.
    """
    _ensure_context()
    return _raw_html(content, **props)


def markdown(content: str, toc: bool = False, **props: Any) -> Component:
    """
    Render markdown with full prose styling.

    Features: prose typography, code blocks with copy, GFM tables/task lists,
    callout blocks ([!NOTE], [!WARNING], [!TIP]), mermaid diagrams,
    KaTeX math, auto-linking, and optional table of contents.

    Example:
        c.markdown("# Hello\\n\\nThis is **bold** text.")
        c.markdown(doc_content, toc=True)
    """
    _ensure_context()
    return _markdown(content, toc=toc, **props)


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
        label=label,
        value=value,
        trend=trend,
        trend_direction=trend_direction,
        prefix=prefix,
        suffix=suffix,
        **props,
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
        data=data,
        columns=columns,
        searchable=searchable,
        sortable=sortable,
        paginate=paginate,
        page_size=page_size,
        **props,
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
        value=value,
        max_value=max_value,
        label=label,
        show_value=show_value,
        variant=variant,
        **props,
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
        label=label,
        on_click=on_click,
        variant=variant,
        size=size,
        disabled=disabled,
        loading=loading,
        icon=icon,
        **props,
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
        label=label, signal=signal, placeholder=placeholder, type=type, disabled=disabled, **props
    )


# Aliases
input_field = input
field = input


def textarea(
    label: str | None = None,
    signal: Signal[str] | None = None,
    placeholder: str = "",
    rows: int = 4,
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Multi-line text input.

    Example:
        c.textarea("Description", placeholder="Enter details...", rows=6)
    """
    _ensure_context()
    return _textarea(
        label=label, signal=signal, placeholder=placeholder, rows=rows, disabled=disabled, **props
    )


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
        label=label,
        options=options,
        signal=signal,
        placeholder=placeholder,
        disabled=disabled,
        **props,
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
        label=label, signal=signal, description=description, disabled=disabled, **props
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
        label=label,
        signal=signal,
        min_value=min,
        max_value=max,
        step=step,
        disabled=disabled,
        **props,
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
        label=label, signal=signal, placeholder=placeholder, disabled=disabled, **props
    )


# Alias
date_picker = date


def chat(
    signal: Signal[list[Any]] | None = None,
    on_send: Callable[..., Any] | str | None = None,
    on_clear: Callable[..., Any] | str | None = None,
    placeholder: str = "Type a message...",
    title: str | None = None,
    height: str = "500px",
    show_clear: bool = False,
    **props: Any,
) -> Component:
    """
    Interactive chat component with streaming support.

    Renders a message list with user/assistant bubbles, a text input,
    and supports real-time streaming of responses via WebSocket.

    The signal should hold a list of messages:
    [{"role": "user"|"assistant"|"error", "content": "..."}]

    Use with Prompture's AsyncConversation for AI-powered chat:

    Example:
        messages = c.signal([], name="chat_messages")
        c.chat(signal=messages, on_send="chat_send", title="AI Chat")

        @c.on("chat_send")
        async def handle_send(session, event):
            text = event["text"]
            # ... use Prompture to get response and stream back
    """
    _ensure_context()
    return _chat(
        signal=signal,
        on_send=on_send,
        on_clear=on_clear,
        placeholder=placeholder,
        title=title,
        height=height,
        show_clear=show_clear,
        **props,
    )


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
    return _file_upload(label=label, on_upload=on_upload, accept=accept, multiple=multiple, **props)


# Alias
file_upload = upload


# =============================================================================
# Content Components
# =============================================================================


@contextmanager
def accordion(
    title: str | None = None,
    items: list[dict[str, Any]] | None = None,
    mode: Literal["multiple", "single"] = "multiple",
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Collapsible accordion sections.

    Example:
        with c.accordion(mode="single"):
            with c.accordion_item("FAQ 1"):
                c.text("Answer 1")
    """
    _ensure_context()
    with _accordion(title=title, items=items, mode=mode, **props) as comp:
        yield comp


@contextmanager
def accordion_item(
    title: str,
    default_open: bool = False,
    icon: str | None = None,
    **props: Any,
) -> Generator[Component, None, None]:
    """Individual accordion item."""
    _ensure_context()
    with _accordion_item(title=title, default_open=default_open, icon=icon, **props) as comp:
        yield comp


@contextmanager
def steps(
    direction: Literal["horizontal", "vertical"] = "horizontal",
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Step-by-step guide container.

    Example:
        with c.steps():
            c.step("Sign Up", status="complete")
            c.step("Verify", status="active")
            c.step("Done", status="pending")
    """
    _ensure_context()
    with _steps(direction=direction, **props) as comp:
        yield comp


def step(
    title: str,
    description: str | None = None,
    status: Literal["pending", "active", "complete", "error"] = "pending",
    icon: str | None = None,
    **props: Any,
) -> Component:
    """Individual step within steps()."""
    _ensure_context()
    return _step(title=title, description=description, status=status, icon=icon, **props)


def file_tree(
    data: dict[str, Any] | str,
    highlight: str | None = None,
    **props: Any,
) -> Component:
    """
    File/directory tree display.

    Example:
        c.file_tree({"src": {"main.py": None}, "README.md": None})
    """
    _ensure_context()
    return _file_tree(data=data, highlight=highlight, **props)


def link_card(
    title: str,
    description: str | None = None,
    href: str | None = None,
    icon: str | None = None,
    **props: Any,
) -> Component:
    """
    Clickable navigation card.

    Example:
        c.link_card("Getting Started", description="Learn the basics", href="/docs", icon="book")
    """
    _ensure_context()
    return _link_card(title=title, description=description, href=href, icon=icon, **props)


# =============================================================================
# General UI Components
# =============================================================================


@contextmanager
def modal(
    title: str | None = None,
    signal: Signal[bool] | None = None,
    size: Literal["sm", "md", "lg", "full"] = "md",
    close_on_backdrop: bool = True,
    close_on_escape: bool = True,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Modal dialog overlay.

    Example:
        show = c.signal(False, name="show_modal")
        with c.modal(title="Confirm", signal=show):
            c.text("Are you sure?")
            c.button("Yes", on_click="confirm")
    """
    _ensure_context()
    with _modal(
        title=title,
        signal=signal,
        size=size,
        close_on_backdrop=close_on_backdrop,
        close_on_escape=close_on_escape,
        **props,
    ) as comp:
        yield comp


@contextmanager
def tooltip(
    text: str,
    position: Literal["top", "bottom", "left", "right"] = "top",
    delay: int = 200,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Tooltip wrapper.

    Example:
        with c.tooltip("Click to submit"):
            c.button("Submit")
    """
    _ensure_context()
    with _tooltip(text=text, position=position, delay=delay, **props) as comp:
        yield comp


def breadcrumb(
    items: list[dict[str, Any]],
    separator: str = "/",
    **props: Any,
) -> Component:
    """
    Breadcrumb navigation.

    Example:
        c.breadcrumb([{"label": "Home", "href": "/"}, {"label": "Docs"}, {"label": "API"}])
    """
    _ensure_context()
    return _breadcrumb(items=items, separator=separator, **props)


def image(
    src: str,
    alt: str = "",
    caption: str | None = None,
    width: int | str | None = None,
    height: int | str | None = None,
    lightbox: bool = False,
    lazy: bool = True,
    **props: Any,
) -> Component:
    """
    Image with optional caption and lightbox.

    Example:
        c.image("photo.jpg", caption="Figure 1", lightbox=True, width=300)
    """
    _ensure_context()
    return _image(
        src=src, alt=alt, caption=caption, width=width, height=height,
        lightbox=lightbox, lazy=lazy, **props,
    )


# =============================================================================
# Nice-to-Have Components
# =============================================================================


@contextmanager
def timeline(
    items: list[dict[str, Any]] | None = None,
    alternate: bool = False,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Vertical timeline for changelogs, events, history.

    Example:
        with c.timeline():
            c.timeline_item("v1.0", "Initial release", date="2024-01-01")

        # Or with items:
        c.timeline(items=[{"title": "v1.0", "description": "Release", "date": "2024-01-01"}])
    """
    _ensure_context()
    with _timeline(items=items, alternate=alternate, **props) as comp:
        yield comp


def timeline_item(
    title: str,
    description: str | None = None,
    date: str | None = None,
    icon: str | None = None,
    color: Literal["primary", "success", "warning", "danger"] | None = None,
    **props: Any,
) -> Component:
    """
    Individual timeline entry. Must be used inside c.timeline().

    Example:
        c.timeline_item("v1.0", "Initial release", date="2024-01-01", color="success")
    """
    _ensure_context()
    return _timeline_item(
        title=title, description=description, date=date, icon=icon, color=color, **props,
    )


def video(
    src: str,
    title: str = "",
    width: int | str | None = None,
    height: int | str | None = None,
    aspect: str = "16/9",
    poster: str | None = None,
    autoplay: bool = False,
    controls: bool = True,
    loop: bool = False,
    muted: bool = False,
    **props: Any,
) -> Component:
    """
    Video embed (YouTube, Vimeo, or direct file).

    Example:
        c.video("https://youtube.com/watch?v=abc123", title="Demo")
        c.video("intro.mp4", poster="thumb.jpg")
    """
    _ensure_context()
    return _video(
        src=src, title=title, width=width, height=height, aspect=aspect,
        poster=poster, autoplay=autoplay, controls=controls, loop=loop, muted=muted, **props,
    )


def diff(
    old_code: str,
    new_code: str,
    language: str = "",
    mode: Literal["unified", "side-by-side"] = "unified",
    **props: Any,
) -> Component:
    """
    Code diff comparison.

    Example:
        c.diff("def foo():\\n    pass", "def foo():\\n    return 1", language="python")
    """
    _ensure_context()
    return _diff(old_code=old_code, new_code=new_code, language=language, mode=mode, **props)


# =============================================================================
# Toast Notifications
# =============================================================================


def toast(
    message: str,
    variant: Literal["info", "success", "warning", "error"] = "info",
    duration: int = 4000,
) -> dict[str, Any]:
    """
    Create a toast notification payload.

    Use with session.send_toast() in event handlers to show transient messages.

    Example:
        @c.on("save")
        async def handle_save(session, event):
            await session.send_toast("Saved!", variant="success")
    """
    return _toast(message=message, variant=variant, duration=duration)


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
    _global_app = None
    _simple_mode = False
    _global_config = {
        "title": "Cacao App",
        "theme": "dark",
        "host": "127.0.0.1",
        "port": 1502,  # 1502: Columbus encounters cacao in Honduras
    }


def export_static() -> dict[str, Any]:
    """
    Export the app configuration for static builds.

    Returns a dictionary containing:
    - pages: Component tree for all pages
    - metadata: App metadata (title, theme)
    - signals: Default signal values

    Example:
        import cacao as c
        import json

        c.config(title="My App")
        c.title("Hello")

        data = c.export_static()
        print(json.dumps(data, indent=2))
    """
    app = _get_app()

    # Get pages
    pages = app.get_all_pages() if hasattr(app, "get_all_pages") else {"/": []}

    # Get metadata
    metadata = {
        "title": getattr(app, "title", _global_config["title"]),
        "theme": getattr(app, "theme", _global_config["theme"]),
    }
    branding = getattr(app, "branding", _global_config.get("branding"))
    if branding is not None:
        metadata["branding"] = branding

    # Get signal defaults
    from .server.signal import Signal

    signals = {}
    for name, signal in Signal.get_all_signals().items():
        if hasattr(signal, "_default"):
            signals[name] = signal._default

    return {
        "pages": pages,
        "metadata": metadata,
        "signals": signals,
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
    "layout",
    # Admin Layout
    "app_shell",
    "nav_sidebar",
    "nav_group",
    "nav_item",
    "shell_content",
    "nav_panel",
    # Typography
    "title",
    "text",
    "html",
    "raw_html",
    "markdown",
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
    "textarea",
    "select",
    "checkbox",
    "switch",
    "slider",
    "date",
    "date_picker",
    "chat",
    "upload",
    "file_upload",
    # Content
    "accordion",
    "accordion_item",
    "steps",
    "step",
    "file_tree",
    "link_card",
    # General UI
    "modal",
    "tooltip",
    "breadcrumb",
    "image",
    # Nice-to-Have
    "timeline",
    "timeline_item",
    "video",
    "diff",
    # Toast
    "toast",
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
]
