"""
Fluent UI Builder for Cacao v2.

A Streamlit-like API for building dashboards with Python.
Uses context managers for intuitive nesting and composition.

Example:
    from cacao.ui import App, row, card, metric, button

    app = App(title="My Dashboard")

    count = app.signal(0, name="count")

    with app.page("/"):
        with row():
            metric("Count", count)
            button("+1", on_click=lambda: count.update(lambda x: x + 1))

    app.run()
"""

from __future__ import annotations

from collections.abc import Callable, Generator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Literal, TypeVar

from .app import App as BaseApp
from .signal import Signal

T = TypeVar("T")

# Context variable to track the current component tree
_current_container: ContextVar[list[Component]] = ContextVar("current_container", default=[])
_component_stack: ContextVar[list[list[Component]]] = ContextVar("component_stack", default=[])


@dataclass
class Component:
    """Base class for all UI components."""

    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list[Component] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        result: dict[str, Any] = {
            "type": self.type,
            "props": self._serialize_props(self.props),
        }
        if self.children:
            result["children"] = [c.to_dict() for c in self.children]
        return result

    def _serialize_props(self, props: dict[str, Any]) -> dict[str, Any]:
        """Serialize props, handling special types."""
        result = {}
        for key, value in props.items():
            if isinstance(value, Signal):
                result[key] = {"__signal__": value.name}
            elif callable(value) and key.startswith("on_"):
                # Event handlers become event names
                result[key] = {"__event__": f"{self.type}:{key}"}
            else:
                result[key] = value
        return result


def _add_to_current_container(component: Component) -> Component:
    """Add a component to the current container."""
    container = _current_container.get()
    container.append(component)
    return component


@contextmanager
def _container_context(component: Component) -> Generator[Component, None, None]:
    """Context manager that makes component the current container."""
    # Save current container to stack
    stack = _component_stack.get()
    current = _current_container.get()
    stack.append(current)
    _component_stack.set(stack)

    # Create new container for children
    children: list[Component] = []
    _current_container.set(children)

    try:
        yield component
    finally:
        # Restore previous container
        stack = _component_stack.get()
        previous = stack.pop()
        _component_stack.set(stack)
        _current_container.set(previous)

        # Set children on component
        component.children = children

        # Add component to parent container
        previous.append(component)


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
        with row(gap=4):
            metric("Users", 100)
            metric("Revenue", "$5k")
    """
    component = Component(
        type="Row", props={"gap": gap, "align": align, "justify": justify, "wrap": wrap, **props}
    )
    with _container_context(component):
        yield component


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
        with row():
            with col(span=8):
                chart(...)
            with col(span=4):
                sidebar_content()
    """
    component = Component(type="Col", props={"span": span, "gap": gap, "align": align, **props})
    with _container_context(component):
        yield component


@contextmanager
def grid(
    cols: int = 12,
    gap: int = 4,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    CSS Grid layout.

    Example:
        with grid(cols=3, gap=4):
            card("Card 1")
            card("Card 2")
            card("Card 3")
    """
    component = Component(type="Grid", props={"cols": cols, "gap": gap, **props})
    with _container_context(component):
        yield component


@contextmanager
def card(
    title: str | None = None,
    subtitle: str | None = None,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Card container.

    Example:
        with card("User Stats"):
            metric("Active", 234)
            metric("New", 45)
    """
    component = Component(type="Card", props={"title": title, "subtitle": subtitle, **props})
    with _container_context(component):
        yield component


@contextmanager
def sidebar(**props: Any) -> Generator[Component, None, None]:
    """
    Sidebar container.

    Example:
        with sidebar():
            select("Category", options=["All", "Tech", "Finance"])
            date_picker("Date Range")
    """
    component = Component(type="Sidebar", props=props)
    with _container_context(component):
        yield component


@contextmanager
def tabs(default: str | None = None, **props: Any) -> Generator[Component, None, None]:
    """
    Tab container.

    Example:
        with tabs(default="overview"):
            with tab("overview", "Overview"):
                overview_content()
            with tab("details", "Details"):
                details_content()
    """
    component = Component(type="Tabs", props={"default": default, **props})
    with _container_context(component):
        yield component


@contextmanager
def tab(
    key: str, label: str, icon: str | None = None, **props: Any
) -> Generator[Component, None, None]:
    """
    Individual tab.

    Must be used inside a tabs() context.
    """
    component = Component(type="Tab", props={"tabKey": key, "label": label, "icon": icon, **props})
    with _container_context(component):
        yield component


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
        with app_shell(brand="My App", default="dashboard",
                       theme_dark="dark", theme_light="light"):
            with nav_sidebar():
                with nav_group("Tools", icon="wrench"):
                    nav_item("Dashboard", key="dashboard", icon="home")
                    nav_item("Settings", key="settings", icon="cog")
            with shell_content():
                with nav_panel("dashboard"):
                    title("Dashboard")
    """
    component = Component(
        type="AppShell",
        props={
            "brand": brand,
            "logo": logo,
            "default": default,
            "themeDark": theme_dark,
            "themeLight": theme_light,
            **props,
        },
    )
    with _container_context(component):
        yield component


@contextmanager
def nav_sidebar(**props: Any) -> Generator[Component, None, None]:
    """
    Navigation sidebar for app_shell.

    Contains nav_group and nav_item components.
    """
    component = Component(type="NavSidebar", props=props)
    with _container_context(component):
        yield component


@contextmanager
def nav_group(
    label: str,
    icon: str | None = None,
    default_open: bool = True,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Collapsible navigation group.

    Contains nav_item components.

    Example:
        with nav_group("Encoders", icon="code"):
            nav_item("Base64", key="base64")
            nav_item("URL", key="url")
    """
    component = Component(
        type="NavGroup", props={"label": label, "icon": icon, "defaultOpen": default_open, **props}
    )
    with _container_context(component):
        yield component


def nav_item(
    label: str,
    key: str,
    icon: str | None = None,
    badge: str | None = None,
    **props: Any,
) -> Component:
    """
    Navigation item (link/button).

    Example:
        nav_item("Base64 Encoder", key="base64", icon="code")
    """
    return _add_to_current_container(
        Component(
            type="NavItem",
            props={"label": label, "itemKey": key, "icon": icon, "badge": badge, **props},
        )
    )


@contextmanager
def shell_content(**props: Any) -> Generator[Component, None, None]:
    """
    Main content area of app_shell.

    This is where the active tool/page content is rendered.
    """
    component = Component(type="ShellContent", props=props)
    with _container_context(component):
        yield component


@contextmanager
def nav_panel(key: str, **props: Any) -> Generator[Component, None, None]:
    """
    Content panel that shows when the nav_item with matching key is active.

    Use inside shell_content to define content for each navigation item.

    Example:
        with shell_content():
            with nav_panel("dashboard"):
                title("Dashboard")
            with nav_panel("settings"):
                title("Settings")
    """
    component = Component(type="NavPanel", props={"panelKey": key, **props})
    with _container_context(component):
        yield component


# =============================================================================
# Typography Components
# =============================================================================


def title(text: str, level: int = 1, **props: Any) -> Component:
    """
    Title/heading text.

    Example:
        title("Dashboard", level=1)
    """
    return _add_to_current_container(
        Component(type="Title", props={"text": text, "level": level, **props})
    )


def text(content: str, size: str = "md", color: str | None = None, **props: Any) -> Component:
    """
    Body text.

    Example:
        text("Welcome to the dashboard", size="lg")
    """
    return _add_to_current_container(
        Component(type="Text", props={"content": content, "size": size, "color": color, **props})
    )


def html(content: str, **props: Any) -> Component:
    """
    Render pre-rendered HTML with prose styling.

    Applies full prose typography (headings, lists, tables, code blocks).
    For raw HTML injection without styling, use raw_html().
    For rendering markdown source, use markdown().

    Example:
        html("<h1>Hello</h1><p>World</p>")
    """
    return _add_to_current_container(Component(type="Html", props={"content": content, **props}))


def raw_html(content: str, **props: Any) -> Component:
    """
    Render raw HTML content with zero styling.

    Use for embedding widgets, iframes, or custom HTML that manages its own styling.

    Example:
        raw_html('<iframe src="https://example.com"></iframe>')
    """
    return _add_to_current_container(Component(type="RawHtml", props={"content": content, **props}))


def markdown(content: str, toc: bool = False, **props: Any) -> Component:
    """
    Render markdown content with full prose styling.

    Parses raw markdown on the frontend and renders with:
    - Prose typography (headings, paragraphs, lists, blockquotes)
    - Code blocks with syntax highlighting and copy button
    - GFM tables, task lists, strikethrough
    - Callout blocks ([!NOTE], [!WARNING], [!TIP], [!IMPORTANT], [!CAUTION])
    - Mermaid diagrams (fenced code blocks with ``mermaid`` language)
    - KaTeX math ($inline$ and $$block$$)
    - Auto-linking URLs
    - Image sizing via ![alt|WxH](url)

    Args:
        content: Raw markdown string.
        toc: If True, generates a floating sidebar table of contents from headings.

    Example:
        markdown("# Hello\\n\\nThis is **bold** text.")
        markdown(doc_content, toc=True)
    """
    return _add_to_current_container(
        Component(type="Markdown", props={"content": content, "toc": toc, **props})
    )


def code(content: str, language: str = "python", **props: Any) -> Component:
    """
    Syntax-highlighted code block.

    Example:
        code("print('Hello')", language="python")
    """
    return _add_to_current_container(
        Component(type="Code", props={"content": content, "language": language, **props})
    )


def divider(**props: Any) -> Component:
    """Horizontal divider line."""
    return _add_to_current_container(Component(type="Divider", props=props))


def spacer(size: int = 4, **props: Any) -> Component:
    """Vertical spacer."""
    return _add_to_current_container(Component(type="Spacer", props={"size": size, **props}))


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
        metric("Revenue", "$45,231", trend="+20.1%", trend_direction="up")
    """
    return _add_to_current_container(
        Component(
            type="Metric",
            props={
                "label": label,
                "value": value,
                "trend": trend,
                "trendDirection": trend_direction,
                "prefix": prefix,
                "suffix": suffix,
                **props,
            },
        )
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
        table(users, columns=["name", "email", "role"], searchable=True)
    """
    # Convert data if it's a pandas DataFrame
    if hasattr(data, "to_dict"):
        data = data.to_dict("records")

    return _add_to_current_container(
        Component(
            type="Table",
            props={
                "data": data,
                "columns": columns,
                "searchable": searchable,
                "sortable": sortable,
                "paginate": paginate,
                "pageSize": page_size,
                **props,
            },
        )
    )


def json_view(data: Any, expanded: bool = True, **props: Any) -> Component:
    """
    JSON tree viewer.

    Example:
        json_view({"name": "John", "age": 30})
    """
    return _add_to_current_container(
        Component(type="JsonView", props={"data": data, "expanded": expanded, **props})
    )


def progress(
    value: int | float,
    max_value: int | float = 100,
    label: str | None = None,
    show_value: bool = True,
    variant: Literal["line", "circle"] = "line",
    **props: Any,
) -> Component:
    """
    Progress bar.

    Example:
        progress(75, label="Completion")
    """
    return _add_to_current_container(
        Component(
            type="Progress",
            props={
                "value": value,
                "max": max_value,
                "label": label,
                "showValue": show_value,
                "variant": variant,
                **props,
            },
        )
    )


def badge(
    text: str,
    color: Literal["default", "primary", "success", "warning", "danger", "info"] = "default",
    **props: Any,
) -> Component:
    """
    Badge/tag.

    Example:
        badge("Active", color="success")
    """
    return _add_to_current_container(
        Component(type="Badge", props={"text": text, "color": color, **props})
    )


def alert(
    message: str,
    type: Literal["info", "success", "warning", "error"] = "info",
    title: str | None = None,
    dismissible: bool = False,
    **props: Any,
) -> Component:
    """
    Alert message.

    Example:
        alert("Operation completed", type="success")
    """
    return _add_to_current_container(
        Component(
            type="Alert",
            props={
                "message": message,
                "type": type,
                "title": title,
                "dismissible": dismissible,
                **props,
            },
        )
    )


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
        button("Submit", on_click=handle_submit, variant="primary")
    """
    return _add_to_current_container(
        Component(
            type="Button",
            props={
                "label": label,
                "on_click": on_click,
                "variant": variant,
                "size": size,
                "disabled": disabled,
                "loading": loading,
                "icon": icon,
                **props,
            },
        )
    )


def input_field(
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
        name = app.signal("", name="name")
        input_field("Name", signal=name, placeholder="Enter your name")
    """
    return _add_to_current_container(
        Component(
            type="Input",
            props={
                "label": label,
                "signal": signal,
                "placeholder": placeholder,
                "type": type,
                "disabled": disabled,
                **props,
            },
        )
    )


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
        content = app.signal("", name="content")
        textarea("Description", signal=content, rows=6)
    """
    return _add_to_current_container(
        Component(
            type="Textarea",
            props={
                "label": label,
                "signal": signal,
                "placeholder": placeholder,
                "rows": rows,
                "disabled": disabled,
                **props,
            },
        )
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
        category = app.signal("all", name="category")
        select("Category", ["All", "Tech", "Finance"], signal=category)
    """
    # Normalize options to list of dicts
    if options and isinstance(options[0], str):
        options = [{"label": o, "value": o} for o in options]

    return _add_to_current_container(
        Component(
            type="Select",
            props={
                "label": label,
                "options": options,
                "signal": signal,
                "placeholder": placeholder,
                "disabled": disabled,
                **props,
            },
        )
    )


def checkbox(
    label: str,
    signal: Signal[bool] | None = None,
    description: str | None = None,
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Checkbox.

    Example:
        agree = app.signal(False, name="agree")
        checkbox("I agree to terms", signal=agree)
    """
    return _add_to_current_container(
        Component(
            type="Checkbox",
            props={
                "label": label,
                "signal": signal,
                "description": description,
                "disabled": disabled,
                **props,
            },
        )
    )


def switch(
    label: str,
    signal: Signal[bool] | None = None,
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Toggle switch.

    Example:
        dark_mode = app.signal(True, name="dark_mode")
        switch("Dark Mode", signal=dark_mode)
    """
    return _add_to_current_container(
        Component(
            type="Switch", props={"label": label, "signal": signal, "disabled": disabled, **props}
        )
    )


def slider(
    label: str,
    signal: Signal[int | float] | None = None,
    min_value: int | float = 0,
    max_value: int | float = 100,
    step: int | float = 1,
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Range slider.

    Example:
        volume = app.signal(50, name="volume")
        slider("Volume", signal=volume, min_value=0, max_value=100)
    """
    return _add_to_current_container(
        Component(
            type="Slider",
            props={
                "label": label,
                "signal": signal,
                "min": min_value,
                "max": max_value,
                "step": step,
                "disabled": disabled,
                **props,
            },
        )
    )


def date_picker(
    label: str,
    signal: Signal[str] | None = None,
    placeholder: str = "Select date",
    disabled: bool = False,
    **props: Any,
) -> Component:
    """
    Date picker.

    Example:
        start_date = app.signal("", name="start_date")
        date_picker("Start Date", signal=start_date)
    """
    return _add_to_current_container(
        Component(
            type="DatePicker",
            props={
                "label": label,
                "signal": signal,
                "placeholder": placeholder,
                "disabled": disabled,
                **props,
            },
        )
    )


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

    The signal should hold a list of messages: [{"role": "user"|"assistant", "content": "..."}]

    Example:
        messages = app.signal([], name="chat_messages")
        chat(signal=messages, on_send=handle_send, title="AI Chat")
    """
    return _add_to_current_container(
        Component(
            type="Chat",
            props={
                "signal": signal,
                "on_send": on_send,
                "on_clear": on_clear,
                "placeholder": placeholder,
                "title": title,
                "height": height,
                "show_clear": show_clear,
                **props,
            },
        )
    )


def file_upload(
    label: str,
    on_upload: Callable[[bytes, str], Any] | None = None,
    accept: str | None = None,
    multiple: bool = False,
    **props: Any,
) -> Component:
    """
    File upload.

    Example:
        file_upload("Upload CSV", on_upload=handle_file, accept=".csv")
    """
    return _add_to_current_container(
        Component(
            type="FileUpload",
            props={
                "label": label,
                "on_upload": on_upload,
                "accept": accept,
                "multiple": multiple,
                **props,
            },
        )
    )


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

    Use as context manager for custom content, or pass items for simple text sections.

    Example:
        with accordion(mode="single"):
            with accordion_item("Section 1", default_open=True):
                text("Content 1")
            with accordion_item("Section 2"):
                text("Content 2")

        # Or with items list:
        accordion(items=[{"title": "FAQ 1", "content": "Answer 1"}])
    """
    component = Component(
        type="Accordion",
        props={"title": title, "items": items, "mode": mode, **props},
    )
    with _container_context(component):
        yield component


@contextmanager
def accordion_item(
    title: str,
    default_open: bool = False,
    icon: str | None = None,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Individual accordion item. Must be used inside accordion().

    Example:
        with accordion_item("Details", default_open=True):
            text("Some details here")
    """
    component = Component(
        type="AccordionItem",
        props={"title": title, "defaultOpen": default_open, "icon": icon, **props},
    )
    with _container_context(component):
        yield component


@contextmanager
def steps(
    direction: Literal["horizontal", "vertical"] = "horizontal",
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Step-by-step guide container.

    Example:
        with steps():
            step("Sign Up", status="complete")
            step("Verify Email", status="active")
            step("Complete Profile", status="pending")
    """
    component = Component(type="Steps", props={"direction": direction, **props})
    with _container_context(component):
        yield component


def step(
    title: str,
    description: str | None = None,
    status: Literal["pending", "active", "complete", "error"] = "pending",
    icon: str | None = None,
    **props: Any,
) -> Component:
    """
    Individual step. Must be used inside steps().

    Example:
        step("Sign Up", description="Create your account", status="complete")
    """
    return _add_to_current_container(
        Component(
            type="Step",
            props={
                "title": title,
                "description": description,
                "status": status,
                "icon": icon,
                **props,
            },
        )
    )


def file_tree(
    data: dict[str, Any] | str,
    highlight: str | None = None,
    **props: Any,
) -> Component:
    """
    File/directory tree display.

    Accepts a nested dict (folders as dicts, files as None) or a string (tree command output).

    Example:
        file_tree({
            "src": {
                "main.py": None,
                "utils": {"helper.py": None}
            },
            "README.md": None
        })
    """
    return _add_to_current_container(
        Component(
            type="FileTree",
            props={"data": data, "highlight": highlight, **props},
        )
    )


def link_card(
    title: str,
    description: str | None = None,
    href: str | None = None,
    icon: str | None = None,
    **props: Any,
) -> Component:
    """
    Clickable navigation card with title, description, and icon.

    Example:
        link_card("Getting Started", description="Learn the basics", href="/docs/start", icon="book")
    """
    return _add_to_current_container(
        Component(
            type="LinkCard",
            props={
                "title": title,
                "description": description,
                "href": href,
                "icon": icon,
                **props,
            },
        )
    )


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
        show = app.signal(False, name="show_modal")
        with modal(title="Confirm", signal=show):
            text("Are you sure?")
            button("Yes", on_click=handle_confirm)
    """
    component = Component(
        type="Modal",
        props={
            "title": title,
            "signal": signal,
            "size": size,
            "closeOnBackdrop": close_on_backdrop,
            "closeOnEscape": close_on_escape,
            **props,
        },
    )
    with _container_context(component):
        yield component


@contextmanager
def tooltip(
    text: str,
    position: Literal["top", "bottom", "left", "right"] = "top",
    delay: int = 200,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Tooltip wrapper. Wraps child elements with hover tooltip.

    Example:
        with tooltip("This button submits the form"):
            button("Submit")
    """
    component = Component(
        type="Tooltip",
        props={"text": text, "position": position, "delay": delay, **props},
    )
    with _container_context(component):
        yield component


def breadcrumb(
    items: list[dict[str, Any]],
    separator: str = "/",
    **props: Any,
) -> Component:
    """
    Breadcrumb navigation.

    Each item: {"label": "Home", "href": "/", "icon": "home"}
    The last item is treated as the current page (no link).

    Example:
        breadcrumb([
            {"label": "Home", "href": "/"},
            {"label": "Docs", "href": "/docs"},
            {"label": "API"}
        ])
    """
    return _add_to_current_container(
        Component(
            type="Breadcrumb",
            props={"items": items, "separator": separator, **props},
        )
    )


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
        image("photo.jpg", caption="Figure 1", lightbox=True, width=300)
    """
    return _add_to_current_container(
        Component(
            type="Image",
            props={
                "src": src,
                "alt": alt,
                "caption": caption,
                "width": width,
                "height": height,
                "lightbox": lightbox,
                "lazy": lazy,
                **props,
            },
        )
    )


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

    This returns the toast data dict. To send it, use session.send_toast()
    or session_manager.broadcast_toast() from an event handler.

    Example:
        @app.on("save")
        async def handle_save(session):
            # ... do save ...
            await session.send_toast("Saved successfully!", variant="success")
    """
    return {
        "message": message,
        "variant": variant,
        "duration": duration,
    }


# =============================================================================
# Application Class
# =============================================================================


class App(BaseApp):
    """
    Fluent UI Application.

    Extends the base App with UI building capabilities.

    Example:
        app = App(title="My Dashboard")

        count = app.signal(0, name="count")

        with app.page("/"):
            metric("Count", count)
            button("+1", on_click=lambda: count.update(lambda x: x + 1))

        app.run()
    """

    def __init__(
        self,
        title: str = "Cacao App",
        theme: Literal["light", "dark", "auto"] = "dark",
        debug: bool = False,
        branding: bool | str | None = None,
        **kwargs: Any,
    ):
        super().__init__(debug=debug, **kwargs)
        self.title = title
        self.theme = theme
        self.branding = branding
        self._pages: dict[str, list[Component]] = {}
        self._current_page: str | None = None

    def signal(self, default: T, *, name: str) -> Signal[T]:
        """
        Create a signal for this app.

        Example:
            count = app.signal(0, name="count")
        """
        return Signal(default, name=name)

    @contextmanager
    def page(self, path: str = "/") -> Generator[None, None, None]:
        """
        Define a page at the given path.

        Example:
            with app.page("/"):
                title("Home")

            with app.page("/about"):
                title("About")
        """
        self._current_page = path

        # Initialize container for this page
        components: list[Component] = []
        _current_container.set(components)

        try:
            yield
        finally:
            self._pages[path] = components
            self._current_page = None

    def get_page_tree(self, path: str = "/") -> list[dict[str, Any]]:
        """Get the component tree for a page as JSON-serializable data."""
        components = self._pages.get(path, [])
        return [c.to_dict() for c in components]

    def get_all_pages(self) -> dict[str, list[dict[str, Any]]]:
        """Get all pages as JSON-serializable data."""
        return {path: [c.to_dict() for c in components] for path, components in self._pages.items()}


# =============================================================================
# Convenience exports
# =============================================================================

__all__ = [
    # App
    "App",
    "Component",
    # Layout
    "row",
    "col",
    "grid",
    "card",
    "sidebar",
    "tabs",
    "tab",
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
    "json_view",
    "progress",
    "badge",
    "alert",
    # Form
    "button",
    "input_field",
    "select",
    "checkbox",
    "switch",
    "slider",
    "date_picker",
    "chat",
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
    # Toast
    "toast",
]
