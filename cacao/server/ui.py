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
def container(
    size: Literal["sm", "md", "lg", "xl", "full"] = "lg",
    padding: bool = True,
    center: bool = True,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Centered max-width content wrapper.

    Example:
        with container(size="md"):
            title("Welcome")
            text("Centered, readable content.")
    """
    component = Component(
        type="Container",
        props={"size": size, "padding": padding, "center": center, **props},
    )
    with _container_context(component):
        yield component


@contextmanager
def stack(
    direction: Literal["vertical", "horizontal"] = "vertical",
    gap: int = 4,
    divider: bool = False,
    align: Literal["start", "center", "end", "stretch"] | None = None,
    justify: Literal["start", "center", "end", "between", "around"] | None = None,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Stack layout with optional dividers between items.

    Example:
        with stack(gap=4, divider=True):
            text("Item 1")
            text("Item 2")
            text("Item 3")
    """
    component = Component(
        type="Stack",
        props={
            "direction": direction,
            "gap": gap,
            "divider": divider,
            "align": align,
            "justify": justify,
            **props,
        },
    )
    with _container_context(component):
        yield component


@contextmanager
def split(
    direction: Literal["horizontal", "vertical"] = "horizontal",
    default_size: int = 50,
    min_size: int = 20,
    max_size: int = 80,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Two-pane resizable layout with draggable divider.

    Place exactly two children inside. The first goes in the left/top pane,
    the second in the right/bottom pane.

    Example:
        with split(default_size=40):
            with col():
                code(source_code, language="python")
            with col():
                text("Output here")
    """
    component = Component(
        type="Split",
        props={
            "direction": direction,
            "defaultSize": default_size,
            "minSize": min_size,
            "maxSize": max_size,
            **props,
        },
    )
    with _container_context(component):
        yield component


@contextmanager
def hero(
    title: str | None = None,
    subtitle: str | None = None,
    background: str | None = None,
    image: str | None = None,
    height: str = "400px",
    align: Literal["center", "left", "right"] = "center",
    gradient: str | None = None,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Full-width hero/banner section.

    Example:
        with hero(title="My App", subtitle="Build amazing things",
                  gradient="135deg, #667eea, #764ba2", height="300px"):
            button("Get Started", variant="primary")
    """
    component = Component(
        type="Hero",
        props={
            "title": title,
            "subtitle": subtitle,
            "background": background,
            "image": image,
            "height": height,
            "align": align,
            "gradient": gradient,
            **props,
        },
    )
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


def code(
    content: str,
    language: str = "python",
    line_numbers: bool = False,
    highlight_lines: str | list[int] | None = None,
    **props: Any,
) -> Component:
    """
    Syntax-highlighted code block with copy button, line numbers, and language badge.

    Args:
        content: The code string to display
        language: Programming language for syntax highlighting
        line_numbers: Show line numbers (auto-enabled for >10 lines)
        highlight_lines: Lines to highlight, e.g. "1,3,5-8" or [1, 3, 5]

    Example:
        code("print('Hello')", language="python", line_numbers=True)
        code(long_code, highlight_lines="5-10,15")
    """
    return _add_to_current_container(
        Component(
            type="Code",
            props={
                "content": content,
                "language": language,
                "line_numbers": line_numbers,
                "highlight_lines": highlight_lines,
                **props,
            },
        )
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
    Interactive chat component with streaming support.

    Renders a message list with user/assistant bubbles, a text input,
    and supports real-time streaming of responses via WebSocket.

    When ``provider`` is set, messages are automatically sent to the LLM
    and streamed back. Otherwise, use ``on_send`` for custom handling.

    Supports all Prompture providers: openai, anthropic/claude, google/gemini,
    groq, grok/xai, ollama, lmstudio, azure, openrouter, and more.

    The signal should hold a list of messages: [{"role": "user"|"assistant", "content": "..."}]

    Example (manual handler):
        messages = app.signal([], name="chat_messages")
        chat(signal=messages, on_send=handle_send, title="AI Chat")

    Example (auto LLM):
        chat(provider="openai", model="gpt-4o", system_prompt="You are helpful.")

    Example (with budget):
        chat(
            provider="openai", model="gpt-4o",
            max_cost=1.00,
            fallback_model="gpt-4o-mini",
        )

    Example (with tools):
        from cacao.server.llm import ToolSpec
        weather_tool = ToolSpec(
            name="get_weather",
            description="Get weather for a city",
            parameters={"type": "object", "properties": {"city": {"type": "string"}}},
        )
        chat(
            provider="openai", model="gpt-4o",
            tools=[weather_tool],
            tool_handlers={"get_weather": get_weather_fn},
        )

    Args:
        max_cost: Maximum USD cost per session. Stops responding when exceeded.
        max_budget_tokens: Maximum total tokens per session.
        fallback_model: Cheaper model to auto-degrade to when 80% of budget is used.
    """
    # Auto-create signal if provider is set and no signal given
    if provider and signal is None:
        from .signal import Signal as _Signal

        sig_name = f"chat_{id(provider)}_{id(model)}"
        signal = _Signal([], name=sig_name)

    # Register LLM config if provider is specified
    if provider and signal is not None:
        from .llm import ChatConfig, register_chat

        config = ChatConfig(
            provider=provider,
            model=model or "gpt-4o",
            system_prompt=system_prompt,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_handlers=tool_handlers or {},
            max_history=max_history,
            max_cost=max_cost,
            max_budget_tokens=max_budget_tokens,
            fallback_model=fallback_model,
        )
        register_chat(signal.name, config)

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
                "llm_enabled": provider is not None,
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


@contextmanager
def subnav(
    searchable: bool = False,
    placeholder: str = "Search...",
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Scrollable sidebar navigation with groups, search, and badges.

    Example:
        with subnav(searchable=True):
            subnav_group("Models")
            subnav_item("User", badge="3", target="section_user")
            subnav_group("API")
            subnav_item("/users", tag="GET", tag_color="success", target="ep_users")
    """
    component = Component(
        type="SubNav",
        props={"searchable": searchable, "placeholder": placeholder, **props},
    )
    with _container_context(component):
        yield component


def subnav_group(
    label: str,
    **props: Any,
) -> Component:
    """Group header within a subnav."""
    return _add_to_current_container(Component(type="SubNavGroup", props={"label": label, **props}))


def subnav_item(
    label: str,
    badge: str | None = None,
    tag: str | None = None,
    tag_color: str | None = None,
    target: str | None = None,
    href: str | None = None,
    **props: Any,
) -> Component:
    """
    Navigation item within a subnav.

    Args:
        label: Display text
        badge: Optional count/badge on the right side
        tag: Optional colored tag on the left (e.g. HTTP method)
        tag_color: Tag color variant: success, info, warning, danger, primary
        target: Element ID to scroll into view on click
        href: URL to navigate to (alternative to target)
    """
    return _add_to_current_container(
        Component(
            type="SubNavItem",
            props={
                "label": label,
                "badge": badge,
                "tag": tag,
                "tag_color": tag_color,
                "target": target,
                "href": href,
                **props,
            },
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
        link_card("Getting Started", description="Learn the basics",
            href="/docs/start", icon="book")
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


@contextmanager
def panel(
    title: str = "Panel",
    width: str = "400px",
    height: str = "300px",
    draggable: bool = True,
    resizable: bool = True,
    closable: bool = True,
    minimizable: bool = True,
    maximizable: bool = True,
    x: int | None = None,
    y: int | None = None,
    **props: Any,
) -> Generator[Component, None, None]:
    """
    Floating panel (window) with drag, resize, minimize/maximize/close.

    Example:
        with panel(title="Inspector", width="400px", height="300px"):
            text("Panel content here")
    """
    component = Component(
        type="Panel",
        props={
            "title": title,
            "width": width,
            "height": height,
            "draggable": draggable,
            "resizable": resizable,
            "closable": closable,
            "minimizable": minimizable,
            "maximizable": maximizable,
            "x": x,
            "y": y,
            **props,
        },
    )
    with _container_context(component):
        yield component


def virtual_list(
    signal: Signal[list[Any]] | str | None = None,
    row_height: int = 40,
    height: str = "400px",
    render_as: str = "Card",
    buffer: int = 5,
    gap: int = 0,
    **props: Any,
) -> Component:
    """
    Virtual list with windowed rendering for large datasets.

    Only renders visible items + buffer for performance.

    Args:
        signal: Signal containing the list of items
        row_height: Height of each row in pixels
        height: Container height
        render_as: Component type to render each item as
        buffer: Number of off-screen items to render
        gap: Gap between items in pixels

    Example:
        items = c.signal(list(range(10000)), name="items")
        c.virtual_list(signal=items, row_height=40, render_as="Card")
    """
    sig_name = signal.name if signal is not None and hasattr(signal, "name") else signal
    return _add_to_current_container(
        Component(
            type="VirtualList",
            props={
                "signal": sig_name,
                "row_height": row_height,
                "height": height,
                "render_as": render_as,
                "buffer": buffer,
                "gap": gap,
                **props,
            },
        )
    )


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

    Use as context manager with timeline_item(), or pass items list.

    Example:
        with timeline():
            timeline_item("v1.0", "Initial release", date="2024-01-01")
            timeline_item("v1.1", "Bug fixes", date="2024-02-01")

        # Or with items list:
        timeline(items=[
            {"title": "v1.0", "description": "Initial release", "date": "2024-01-01"},
        ])
    """
    component = Component(
        type="Timeline",
        props={"items": items, "alternate": alternate, **props},
    )
    with _container_context(component):
        yield component


def timeline_item(
    title: str,
    description: str | None = None,
    date: str | None = None,
    icon: str | None = None,
    color: Literal["primary", "success", "warning", "danger"] | None = None,
    **props: Any,
) -> Component:
    """
    Individual timeline entry. Must be used inside timeline().

    Example:
        timeline_item("v1.0", "Initial release", date="2024-01-01", color="success")
    """
    return _add_to_current_container(
        Component(
            type="TimelineItem",
            props={
                "title": title,
                "description": description,
                "date": date,
                "icon": icon,
                "color": color,
                **props,
            },
        )
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
    Video embed with auto-detection for YouTube, Vimeo, or direct files.

    Example:
        video("https://youtube.com/watch?v=abc123", title="Demo")
        video("intro.mp4", poster="thumb.jpg", controls=True)
    """
    return _add_to_current_container(
        Component(
            type="Video",
            props={
                "src": src,
                "title": title,
                "width": width,
                "height": height,
                "aspect": aspect,
                "poster": poster,
                "autoplay": autoplay,
                "controls": controls,
                "loop": loop,
                "muted": muted,
                **props,
            },
        )
    )


def diff(
    old_code: str,
    new_code: str,
    language: str = "",
    mode: Literal["unified", "side-by-side"] = "unified",
    **props: Any,
) -> Component:
    """
    Code diff comparison view.

    Example:
        diff("def foo():\\n    pass", "def foo():\\n    return 1", language="python")
    """
    return _add_to_current_container(
        Component(
            type="Diff",
            props={
                "old_code": old_code,
                "new_code": new_code,
                "language": language,
                "mode": mode,
                **props,
            },
        )
    )


# =============================================================================
# Search & Deep Linking
# =============================================================================


def search_input(
    placeholder: str = "Search...",
    signal: Signal[str] | None = None,
    debounce: int = 300,
    size: Literal["sm", "md", "lg"] = "md",
    clearable: bool = True,
    on_search: Callable[..., Any] | None = None,
    **props: Any,
) -> Component:
    """
    Search input with debounce, clear button, and signal binding.

    Ideal for filtering lists, tables, or documentation content.

    Args:
        placeholder: Placeholder text
        signal: Signal to bind the search value to
        debounce: Debounce delay in ms before emitting value
        size: Input size variant
        clearable: Show clear button when value is non-empty
        on_search: Event handler called with search value

    Example:
        query = app.signal("", name="query")
        search_input("Search docs...", signal=query)
    """
    return _add_to_current_container(
        Component(
            type="SearchInput",
            props={
                "placeholder": placeholder,
                "signal": signal,
                "debounce": debounce,
                "size": size,
                "clearable": clearable,
                "on_search": on_search,
                **props,
            },
        )
    )


def anchor(
    id: str,
    offset: int = 0,
    **props: Any,
) -> Component:
    """
    Invisible anchor point for deep linking.

    Creates a target that can be scrolled to via URL hash (#id).
    Auto-scrolls on page load if the hash matches.

    Args:
        id: Unique anchor identifier (used in URL as #id)
        offset: Pixel offset from top when scrolling (for fixed headers)

    Example:
        anchor("api-users")
        title("Users API")
        # Link to this with href="#api-users"
    """
    return _add_to_current_container(
        Component(
            type="Anchor",
            props={"id": id, "offset": offset, **props},
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

    def get_used_categories(self) -> set[str]:
        """Analyze all pages and return the set of component categories used."""
        types: set[str] = set()
        for components in self._pages.values():
            for comp in components:
                _collect_types(comp, types)
        return _types_to_categories(types)


def _collect_types(component: Component, types: set[str]) -> None:
    """Recursively collect all component types from a tree."""
    types.add(component.type)
    for child in component.children:
        _collect_types(child, types)


# Component type → category mapping
_CATEGORY_MAP: dict[str, str] = {}

_LAYOUT_TYPES = {
    "Row",
    "Col",
    "Grid",
    "Sidebar",
    "AppShell",
    "NavSidebar",
    "NavGroup",
    "NavItem",
    "ShellContent",
    "NavPanel",
    "Container",
    "Stack",
    "Split",
    "Hero",
    "Panel",
}
_TYPOGRAPHY_TYPES = {
    "Title",
    "Text",
    "Html",
    "RawHtml",
    "Markdown",
    "Code",
    "Spacer",
    "Divider",
}
_DISPLAY_TYPES = {
    "Card",
    "Metric",
    "Table",
    "Alert",
    "Progress",
    "Gauge",
    "JsonView",
    "Badge",
    "Accordion",
    "AccordionItem",
    "Steps",
    "Step",
    "FileTree",
    "LinkCard",
    "Modal",
    "Tooltip",
    "Breadcrumb",
    "Image",
    "Timeline",
    "TimelineItem",
    "Video",
    "Diff",
    "Anchor",
    "VirtualList",
}
_FORM_TYPES = {
    "Button",
    "Input",
    "Textarea",
    "Select",
    "Checkbox",
    "Switch",
    "Slider",
    "DatePicker",
    "FileUpload",
    "Chat",
    "Tabs",
    "Tab",
    "SearchInput",
    "Interface",
}
_CHART_TYPES = {
    "LineChart",
    "BarChart",
    "PieChart",
    "AreaChart",
    "ScatterChart",
    "RadarChart",
    "GaugeChart",
    "FunnelChart",
    "HeatmapChart",
    "TreemapChart",
}

for _t in _LAYOUT_TYPES:
    _CATEGORY_MAP[_t] = "layout"
for _t in _TYPOGRAPHY_TYPES:
    _CATEGORY_MAP[_t] = "typography"
for _t in _DISPLAY_TYPES:
    _CATEGORY_MAP[_t] = "display"
for _t in _FORM_TYPES:
    _CATEGORY_MAP[_t] = "form"
for _t in _CHART_TYPES:
    _CATEGORY_MAP[_t] = "charts"


def _types_to_categories(types: set[str]) -> set[str]:
    """Map component types to their categories."""
    categories: set[str] = set()
    for t in types:
        cat = _CATEGORY_MAP.get(t)
        if cat:
            categories.add(cat)
    return categories


# =============================================================================
# AI / Prompture Components
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

    Uses Prompture to extract data matching a JSON Schema or Pydantic model
    from user-provided text.

    Example:
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "email": {"type": "string"},
            },
        }
        extract(schema, provider="openai", model="gpt-4o")

    Args:
        schema: JSON Schema for the desired output structure.
        pydantic_model: A Pydantic BaseModel class (alternative to schema).
        provider: LLM provider name.
        model: Model name.
        api_key: Optional API key override.
        title: Component title.
        description: Description text shown below title.
        submit_label: Text for the submit button.
        height: Component height.
    """
    from .signal import Signal as _Signal

    sig_name = f"extract_{id(schema)}_{id(pydantic_model)}"
    result_signal = _Signal({}, name=f"{sig_name}_result")

    # Serialize schema for the frontend
    schema_display = schema
    if pydantic_model is not None:
        try:
            schema_display = pydantic_model.model_json_schema()
        except Exception:
            schema_display = {"note": "Pydantic model (schema not displayable)"}

    return _add_to_current_container(
        Component(
            type="Extract",
            props={
                "schema": schema_display,
                "pydantic_model_name": pydantic_model.__name__ if pydantic_model else None,
                "provider": provider,
                "model": model,
                "title": title,
                "description": description,
                "submit_label": submit_label,
                "height": height,
                "result_signal": result_signal,
                **props,
            },
        )
    )


def cost_dashboard(
    *,
    title: str = "Usage & Costs",
    show_budget: bool = True,
    show_breakdown: bool = True,
    compact: bool = False,
    **props: Any,
) -> Component:
    """
    Cost tracking dashboard — shows per-session token counts, USD costs,
    and model comparison.

    Reads from the session's cost tracker and updates in real-time.

    Example:
        c.cost_dashboard(title="API Usage", compact=True)

    Args:
        title: Dashboard title.
        show_budget: Show budget gauge if budget is configured.
        show_breakdown: Show per-model cost breakdown table.
        compact: Use compact layout (single row of metrics).
    """
    from .signal import Signal as _Signal

    sig_name = f"cost_dashboard_{id(title)}"
    cost_signal = _Signal({}, name=sig_name)

    return _add_to_current_container(
        Component(
            type="CostDashboard",
            props={
                "title": title,
                "show_budget": show_budget,
                "show_breakdown": show_breakdown,
                "compact": compact,
                "cost_signal": cost_signal,
                **props,
            },
        )
    )


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
    Document ingestion component — upload PDF, DOCX, CSV, etc. and extract
    structured data via Prompture.

    Example:
        schema = {"type": "object", "properties": {"summary": {"type": "string"}}}
        c.document_upload(schema=schema, extract_on_upload=True)

    Args:
        schema: JSON Schema for extraction (optional). If not provided,
                shows raw parsed text only.
        provider: LLM provider for extraction.
        model: Model name for extraction.
        api_key: Optional API key override.
        title: Component title.
        accept: Accepted file types (comma-separated).
        show_preview: Show parsed text preview.
        extract_on_upload: Automatically extract when file is uploaded.
    """
    from .signal import Signal as _Signal

    sig_name = f"docupload_{id(schema)}_{id(title)}"
    doc_signal = _Signal({}, name=f"{sig_name}_doc")

    return _add_to_current_container(
        Component(
            type="DocumentUpload",
            props={
                "schema": schema,
                "provider": provider,
                "model": model,
                "title": title,
                "accept": accept,
                "show_preview": show_preview,
                "extract_on_upload": extract_on_upload,
                "doc_signal": doc_signal,
                **props,
            },
        )
    )


def model_picker(
    *,
    signal: Signal[str] | None = None,
    label: str = "Model",
    grouped: bool = True,
    default: str | None = None,
    **props: Any,
) -> Component:
    """
    Model discovery picker — auto-detects available providers and models,
    displays them in a searchable select component.

    Example:
        model = c.signal("openai/gpt-4o", name="selected_model")
        c.model_picker(signal=model)

    Args:
        signal: Signal to bind the selected model string to.
        label: Label for the picker.
        grouped: Group models by provider.
        default: Default model selection.
    """
    from .signal import Signal as _Signal

    if signal is None:
        sig_name = f"model_picker_{id(label)}"
        signal = _Signal(default or "", name=sig_name)

    return _add_to_current_container(
        Component(
            type="ModelPicker",
            props={
                "signal": signal,
                "label": label,
                "grouped": grouped,
                "default": default,
                **props,
            },
        )
    )


# =============================================================================
# Tukuy Skills Integration
# =============================================================================


def skill(
    fn: Any = None,
    *,
    title: str | None = None,
    description: str | None = None,
    show_metadata: bool = True,
    show_timing: bool = True,
    height: str = "auto",
    **props: Any,
) -> Component:
    """
    Wrap a Tukuy ``@skill`` decorated function into an interactive component.

    Automatically generates input fields from the skill's input schema and
    displays results with timing and metadata.

    Example:
        from tukuy import skill as tukuy_skill

        @tukuy_skill(name="parse_date", description="Parse a date string")
        def parse_date(text: str) -> str:
            from dateutil import parser
            return parser.parse(text).isoformat()

        c.skill(parse_date)

    Args:
        fn: A Tukuy ``@skill``-decorated function or ``Skill`` object.
        title: Override the skill's name as display title.
        description: Override the skill's description.
        show_metadata: Show skill metadata (category, tags, risk level).
        show_timing: Show execution duration after invocation.
        height: Container height.
    """
    # Extract skill descriptor
    skill_obj = None
    descriptor: dict[str, Any] = {}

    if fn is not None:
        # Check if it's a @skill-decorated function (has __skill__ attribute)
        if hasattr(fn, "__skill__"):
            skill_obj = fn.__skill__
        # Or it's a Skill instance directly
        elif hasattr(fn, "descriptor"):
            skill_obj = fn

    if skill_obj is not None:
        desc = skill_obj.descriptor
        descriptor = {
            "name": desc.name,
            "description": desc.description,
            "version": getattr(desc, "version", "0.1.0"),
            "category": getattr(desc, "category", ""),
            "tags": list(getattr(desc, "tags", [])),
            "input_schema": getattr(desc, "input_schema", {}),
            "output_schema": getattr(desc, "output_schema", {}),
            "risk_level": str(getattr(desc, "risk_level", "AUTO")),
            "idempotent": getattr(desc, "idempotent", False),
            "side_effects": getattr(desc, "side_effects", True),
            "requires_network": getattr(desc, "requires_network", False),
            "requires_filesystem": getattr(desc, "requires_filesystem", False),
            "config_params": [
                {"name": p.name, "type": str(p.type), "default": p.default, "description": p.description}
                for p in getattr(desc, "config_params", [])
            ],
        }

    display_title = title or descriptor.get("name", "Skill")
    display_description = description or descriptor.get("description", "")

    return _add_to_current_container(
        Component(
            type="SkillRunner",
            props={
                "skill_name": descriptor.get("name", ""),
                "title": display_title,
                "description": display_description,
                "descriptor": descriptor,
                "show_metadata": show_metadata,
                "show_timing": show_timing,
                "height": height,
                **props,
            },
        )
    )


def skill_browser(
    *,
    title: str = "Skill Browser",
    show_search: bool = True,
    show_categories: bool = True,
    compact: bool = False,
    on_select: str | None = None,
    height: str = "500px",
    **props: Any,
) -> Component:
    """
    Skill discovery widget showing all registered Tukuy skills with search.

    Browses all available skills from Tukuy's plugin system, grouped by
    category. Click a skill to see details and optionally run it.

    Example:
        c.skill_browser()
        c.skill_browser(compact=True, height="300px")

    Args:
        title: Widget title.
        show_search: Show the search input.
        show_categories: Group skills by category/plugin.
        compact: Compact display mode.
        on_select: Event name to fire when a skill is selected.
        height: Container height.
    """
    return _add_to_current_container(
        Component(
            type="SkillBrowser",
            props={
                "title": title,
                "show_search": show_search,
                "show_categories": show_categories,
                "compact": compact,
                "on_select": on_select,
                "height": height,
                **props,
            },
        )
    )


def chain_builder(
    *,
    title: str = "Chain Builder",
    initial_steps: list[dict[str, Any]] | None = None,
    show_output: bool = True,
    height: str = "600px",
    **props: Any,
) -> Component:
    """
    Visual chain builder for Tukuy Chain/Branch/Parallel composition.

    Drag-and-drop interface for composing Tukuy skills and transformers
    into processing chains. Supports sequential chains, conditional branches,
    and parallel execution.

    Example:
        c.chain_builder()
        c.chain_builder(initial_steps=[
            {"type": "transformer", "name": "strip"},
            {"type": "transformer", "name": "lowercase"},
        ])

    Args:
        title: Widget title.
        initial_steps: Pre-configured chain steps.
        show_output: Show output panel for chain results.
        height: Container height.
    """
    return _add_to_current_container(
        Component(
            type="ChainBuilder",
            props={
                "title": title,
                "initial_steps": initial_steps or [],
                "show_output": show_output,
                "height": height,
                **props,
            },
        )
    )


def safety_policy(
    *,
    title: str = "Safety Policy",
    preset: str | None = None,
    show_presets: bool = True,
    show_advanced: bool = True,
    compact: bool = False,
    **props: Any,
) -> Component:
    """
    Safety policy configuration UI for Tukuy skill execution.

    Allows configuring which imports, network access, and filesystem access
    are permitted during skill execution for the current session.

    Example:
        c.safety_policy()
        c.safety_policy(preset="restrictive")

    Args:
        title: Widget title.
        preset: Initial preset (restrictive, permissive, network_only, filesystem_only).
        show_presets: Show preset selection buttons.
        show_advanced: Show advanced configuration (custom imports, paths).
        compact: Compact display mode.
    """
    return _add_to_current_container(
        Component(
            type="SafetyPolicy",
            props={
                "title": title,
                "preset": preset,
                "show_presets": show_presets,
                "show_advanced": show_advanced,
                "compact": compact,
                **props,
            },
        )
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

    Creates an interactive agent UI that shows the agent's reasoning steps,
    tool calls, and responses in real-time. The agent follows the ReAct
    (Reasoning + Acting) pattern with visual trace of each step.

    Example (basic agent):
        c.agent(
            provider="openai",
            model="gpt-4o",
            system_prompt="You are a helpful research assistant.",
        )

    Example (with tools):
        from cacao.server.llm import ToolSpec

        weather_tool = ToolSpec(
            name="get_weather",
            description="Get weather for a city",
            parameters={"type": "object", "properties": {"city": {"type": "string"}}},
        )
        c.agent(
            provider="openai", model="gpt-4o",
            tools=[weather_tool],
            tool_handlers={"get_weather": get_weather_fn},
            max_iterations=5,
        )

    Example (with budget):
        c.agent(
            provider="openai", model="gpt-4o",
            max_cost=2.00, fallback_model="gpt-4o-mini",
        )

    Args:
        provider: LLM provider name (15+ supported via Prompture).
        model: Model name.
        system_prompt: System message for the agent.
        api_key: API key (or set via environment variable).
        temperature: Sampling temperature.
        max_tokens: Max tokens per LLM call.
        tools: List of ToolSpec for function calling.
        tool_handlers: Dict mapping tool names to handler functions.
        max_iterations: Maximum ReAct loop iterations.
        max_cost: Maximum USD cost per session.
        max_budget_tokens: Maximum total tokens per session.
        fallback_model: Cheaper model to degrade to at 80% budget.
        title: Component title.
        placeholder: Input placeholder text.
        height: Component height.
        show_steps: Show the step-by-step trace panel.
        show_cost: Show cost/token usage inline.
    """
    import uuid as _uuid

    from .agent import AgentConfig, register_agent

    agent_id = f"agent_{_uuid.uuid4().hex[:8]}"

    config = AgentConfig(
        provider=provider,
        model=model,
        system_prompt=system_prompt,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=tools,
        tool_handlers=tool_handlers or {},
        max_iterations=max_iterations,
        max_cost=max_cost,
        max_budget_tokens=max_budget_tokens,
        fallback_model=fallback_model,
    )
    register_agent(agent_id, config)

    return _add_to_current_container(
        Component(
            type="Agent",
            props={
                "agent_id": agent_id,
                "title": title,
                "placeholder": placeholder,
                "height": height,
                "show_steps": show_steps,
                "show_cost": show_cost,
                "has_tools": tools is not None and len(tools) > 0,
                "model": model,
                "provider": provider,
                **props,
            },
        )
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
    Multi-agent UI — debate view, router dashboard, or sequential pipeline.

    Supports three modes:
    - ``debate``: Agents take turns responding to a prompt, building on each other.
    - ``router``: A router agent decides which specialist handles the request.
    - ``pipeline``: Agents process sequentially, each receiving the previous output.

    Example (debate):
        c.multi_agent(
            mode="debate",
            agents=[
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "You are optimistic."},
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "You are skeptical."},
            ],
            agent_names=["Optimist", "Skeptic"],
            rounds=3,
        )

    Example (router):
        c.multi_agent(
            mode="router",
            agents=[
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "Expert in Python."},
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "Expert in JavaScript."},
            ],
            agent_names=["Python Expert", "JS Expert"],
        )

    Example (pipeline):
        c.multi_agent(
            mode="pipeline",
            agents=[
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "Translate to French."},
                {"provider": "openai", "model": "gpt-4o", "system_prompt": "Summarize in one sentence."},
            ],
            agent_names=["Translator", "Summarizer"],
        )

    Args:
        mode: Multi-agent mode — "debate", "router", or "pipeline".
        agents: List of agent config dicts (provider, model, system_prompt, etc.).
        agent_names: Display names for each agent.
        rounds: Number of debate rounds (debate mode only).
        router_prompt: Custom routing prompt (router mode only).
        title: Component title.
        height: Component height.
    """
    import uuid as _uuid

    from .agent import AgentConfig, MultiAgentConfig, register_multi_agent

    multi_id = f"multi_{_uuid.uuid4().hex[:8]}"
    agents_raw = agents or []
    names = agent_names or [f"Agent {i + 1}" for i in range(len(agents_raw))]

    agent_configs = [
        AgentConfig(
            provider=a.get("provider", "openai"),
            model=a.get("model", "gpt-4o"),
            system_prompt=a.get("system_prompt"),
            api_key=a.get("api_key"),
            base_url=a.get("base_url"),
            temperature=a.get("temperature", 0.7),
            max_tokens=a.get("max_tokens", 4096),
        )
        for a in agents_raw
    ]

    config = MultiAgentConfig(
        mode=mode,
        agents=agent_configs,
        agent_names=names,
        rounds=rounds,
        router_prompt=router_prompt,
    )
    register_multi_agent(multi_id, config)

    return _add_to_current_container(
        Component(
            type="MultiAgent",
            props={
                "multi_id": multi_id,
                "mode": mode,
                "agent_names": names,
                "rounds": rounds,
                "title": title,
                "height": height,
                **props,
            },
        )
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

    Displays a timeline view of all steps in an agent's ReAct loop,
    including thinking, tool calls (with arguments and results),
    and final responses. Can be used standalone or paired with ``c.agent()``.

    Example (standalone):
        c.tool_timeline(agent_id="my_agent_id")

    Example (paired with agent):
        agent_comp = c.agent(provider="openai", model="gpt-4o", tools=[...])
        c.tool_timeline(agent_id=agent_comp.props["agent_id"])

    Args:
        agent_id: The agent ID to track. If None, tracks all agents.
        title: Widget title.
        height: Container height.
        show_args: Show tool call arguments.
        show_results: Show tool call results.
        show_cost: Show per-step cost/tokens.
        compact: Compact display mode.
    """
    return _add_to_current_container(
        Component(
            type="ToolTimeline",
            props={
                "agent_id": agent_id,
                "title": title,
                "height": height,
                "show_args": show_args,
                "show_results": show_results,
                "show_cost": show_cost,
                "compact": compact,
                **props,
            },
        )
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

    Displays a visual gauge showing current spending against budget limits,
    with color-coded warnings when approaching thresholds. Updates
    automatically as the agent or chat components consume tokens.

    Example:
        c.budget_gauge(max_cost=5.00, max_tokens=100000)

    Example (compact):
        c.budget_gauge(max_cost=1.00, compact=True)

    Args:
        max_cost: Maximum USD budget. If None, shows usage without limit.
        max_tokens: Maximum token budget. If None, shows usage without limit.
        warn_threshold: Fraction (0-1) at which to show warning color (default 0.8).
        title: Widget title.
        show_breakdown: Show per-model cost breakdown table.
        compact: Compact single-line display mode.
    """
    return _add_to_current_container(
        Component(
            type="BudgetGauge",
            props={
                "max_cost": max_cost,
                "max_tokens": max_tokens,
                "warn_threshold": warn_threshold,
                "title": title,
                "show_breakdown": show_breakdown,
                "compact": compact,
                **props,
            },
        )
    )


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
    "container",
    "stack",
    "split",
    "hero",
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
    # Nice-to-Have
    "timeline",
    "timeline_item",
    "video",
    "diff",
    # Search & Deep Linking
    "search_input",
    "anchor",
    # Toast
    "toast",
    # Virtual List
    "virtual_list",
    # Panel
    "panel",
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
]
