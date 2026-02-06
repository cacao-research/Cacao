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

from typing import Any, Callable, TypeVar, Generic, Literal, overload
from dataclasses import dataclass, field
from contextlib import contextmanager
from contextvars import ContextVar
import json
import asyncio

from .signal import Signal
from .app import App as BaseApp

T = TypeVar("T")

# Context variable to track the current component tree
_current_container: ContextVar[list["Component"]] = ContextVar("current_container", default=[])
_component_stack: ContextVar[list[list["Component"]]] = ContextVar("component_stack", default=[])


@dataclass
class Component:
    """Base class for all UI components."""

    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list["Component"] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        result = {
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
def _container_context(component: Component):
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
):
    """
    Horizontal row layout.

    Example:
        with row(gap=4):
            metric("Users", 100)
            metric("Revenue", "$5k")
    """
    component = Component(
        type="Row",
        props={"gap": gap, "align": align, "justify": justify, "wrap": wrap, **props}
    )
    with _container_context(component):
        yield component


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
        with row():
            with col(span=8):
                chart(...)
            with col(span=4):
                sidebar_content()
    """
    component = Component(
        type="Col",
        props={"span": span, "gap": gap, "align": align, **props}
    )
    with _container_context(component):
        yield component


@contextmanager
def grid(
    cols: int = 12,
    gap: int = 4,
    **props: Any,
):
    """
    CSS Grid layout.

    Example:
        with grid(cols=3, gap=4):
            card("Card 1")
            card("Card 2")
            card("Card 3")
    """
    component = Component(
        type="Grid",
        props={"cols": cols, "gap": gap, **props}
    )
    with _container_context(component):
        yield component


@contextmanager
def card(
    title: str | None = None,
    subtitle: str | None = None,
    **props: Any,
):
    """
    Card container.

    Example:
        with card("User Stats"):
            metric("Active", 234)
            metric("New", 45)
    """
    component = Component(
        type="Card",
        props={"title": title, "subtitle": subtitle, **props}
    )
    with _container_context(component):
        yield component


@contextmanager
def sidebar(**props: Any):
    """
    Sidebar container.

    Example:
        with sidebar():
            select("Category", options=["All", "Tech", "Finance"])
            date_picker("Date Range")
    """
    component = Component(
        type="Sidebar",
        props=props
    )
    with _container_context(component):
        yield component


@contextmanager
def tabs(default: str | None = None, **props: Any):
    """
    Tab container.

    Example:
        with tabs(default="overview"):
            with tab("overview", "Overview"):
                overview_content()
            with tab("details", "Details"):
                details_content()
    """
    component = Component(
        type="Tabs",
        props={"default": default, **props}
    )
    with _container_context(component):
        yield component


@contextmanager
def tab(key: str, label: str, icon: str | None = None, **props: Any):
    """
    Individual tab.

    Must be used inside a tabs() context.
    """
    component = Component(
        type="Tab",
        props={"tabKey": key, "label": label, "icon": icon, **props}
    )
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
    return _add_to_current_container(Component(
        type="Title",
        props={"text": text, "level": level, **props}
    ))


def text(content: str, size: str = "md", color: str | None = None, **props: Any) -> Component:
    """
    Body text.

    Example:
        text("Welcome to the dashboard", size="lg")
    """
    return _add_to_current_container(Component(
        type="Text",
        props={"content": content, "size": size, "color": color, **props}
    ))


def code(content: str, language: str = "python", **props: Any) -> Component:
    """
    Syntax-highlighted code block.

    Example:
        code("print('Hello')", language="python")
    """
    return _add_to_current_container(Component(
        type="Code",
        props={"content": content, "language": language, **props}
    ))


def divider(**props: Any) -> Component:
    """Horizontal divider line."""
    return _add_to_current_container(Component(type="Divider", props=props))


def spacer(size: int = 4, **props: Any) -> Component:
    """Vertical spacer."""
    return _add_to_current_container(Component(
        type="Spacer",
        props={"size": size, **props}
    ))


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
    return _add_to_current_container(Component(
        type="Metric",
        props={
            "label": label,
            "value": value,
            "trend": trend,
            "trendDirection": trend_direction,
            "prefix": prefix,
            "suffix": suffix,
            **props
        }
    ))


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
    if hasattr(data, 'to_dict'):
        data = data.to_dict('records')

    return _add_to_current_container(Component(
        type="Table",
        props={
            "data": data,
            "columns": columns,
            "searchable": searchable,
            "sortable": sortable,
            "paginate": paginate,
            "pageSize": page_size,
            **props
        }
    ))


def json_view(data: Any, expanded: bool = True, **props: Any) -> Component:
    """
    JSON tree viewer.

    Example:
        json_view({"name": "John", "age": 30})
    """
    return _add_to_current_container(Component(
        type="JsonView",
        props={"data": data, "expanded": expanded, **props}
    ))


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
    return _add_to_current_container(Component(
        type="Progress",
        props={
            "value": value,
            "max": max_value,
            "label": label,
            "showValue": show_value,
            "variant": variant,
            **props
        }
    ))


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
    return _add_to_current_container(Component(
        type="Badge",
        props={"text": text, "color": color, **props}
    ))


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
    return _add_to_current_container(Component(
        type="Alert",
        props={"message": message, "type": type, "title": title, "dismissible": dismissible, **props}
    ))


# =============================================================================
# Form Components
# =============================================================================

def button(
    label: str,
    on_click: Callable[[], Any] | None = None,
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
    return _add_to_current_container(Component(
        type="Button",
        props={
            "label": label,
            "on_click": on_click,
            "variant": variant,
            "size": size,
            "disabled": disabled,
            "loading": loading,
            "icon": icon,
            **props
        }
    ))


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
    return _add_to_current_container(Component(
        type="Input",
        props={
            "label": label,
            "signal": signal,
            "placeholder": placeholder,
            "type": type,
            "disabled": disabled,
            **props
        }
    ))


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

    return _add_to_current_container(Component(
        type="Select",
        props={
            "label": label,
            "options": options,
            "signal": signal,
            "placeholder": placeholder,
            "disabled": disabled,
            **props
        }
    ))


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
    return _add_to_current_container(Component(
        type="Checkbox",
        props={
            "label": label,
            "signal": signal,
            "description": description,
            "disabled": disabled,
            **props
        }
    ))


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
    return _add_to_current_container(Component(
        type="Switch",
        props={
            "label": label,
            "signal": signal,
            "disabled": disabled,
            **props
        }
    ))


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
    return _add_to_current_container(Component(
        type="Slider",
        props={
            "label": label,
            "signal": signal,
            "min": min_value,
            "max": max_value,
            "step": step,
            "disabled": disabled,
            **props
        }
    ))


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
    return _add_to_current_container(Component(
        type="DatePicker",
        props={
            "label": label,
            "signal": signal,
            "placeholder": placeholder,
            "disabled": disabled,
            **props
        }
    ))


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
    return _add_to_current_container(Component(
        type="FileUpload",
        props={
            "label": label,
            "on_upload": on_upload,
            "accept": accept,
            "multiple": multiple,
            **props
        }
    ))


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
        **kwargs: Any,
    ):
        super().__init__(debug=debug, **kwargs)
        self.title = title
        self.theme = theme
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
    def page(self, path: str = "/"):
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
        return {path: [c.to_dict() for c in components]
                for path, components in self._pages.items()}


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
    # Typography
    "title",
    "text",
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
    "file_upload",
]
