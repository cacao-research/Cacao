"""
Fluent component builders for cleaner UI definitions.

Instead of deeply nested dicts, use these helpers:

    # Before (verbose):
    {
        "type": "div",
        "props": {
            "className": "container",
            "children": [
                {"type": "h1", "props": {"content": "Title"}},
                {"type": "button", "props": {"content": "Click", "onClick": "action"}}
            ]
        }
    }

    # After (clean):
    div(
        h1("Title"),
        button("Click", onClick="action"),
        className="container"
    )
"""

from typing import Any, Dict, List, Optional, Tuple, Union

# Type alias for component children
Child = Union[Dict[str, Any], str, None]


def _element(
    tag: str,
    children: Tuple[Child, ...] = (),
    className: Optional[str] = None,
    style: Optional[Dict[str, Any]] = None,
    **props: Any
) -> Dict[str, Any]:
    """Base element builder."""
    p: Dict[str, Any] = {}

    # Add props first
    p.update(props)

    # Add className and style
    if className:
        p["className"] = className
    if style:
        p["style"] = style

    # Process children
    if children:
        processed = []
        for child in children:
            if child is None:
                continue
            if isinstance(child, str):
                processed.append({"type": "span", "props": {"content": child}})
            else:
                processed.append(child)
        if processed:
            p["children"] = processed

    return {"type": tag, "props": p}


# Layout Components

def div(*children: Child, className: str = None, style: dict = None, **props) -> dict:
    """Create a div element."""
    return _element("div", children, className, style, **props)


def span(content: str = None, className: str = None, **props) -> dict:
    """Create a span element."""
    if content:
        props["content"] = content
    return _element("span", (), className, None, **props)


def section(*children: Child, className: str = None, **props) -> dict:
    """Create a section element."""
    return _element("section", children, className, None, **props)


def main(*children: Child, className: str = None, **props) -> dict:
    """Create a main element."""
    return _element("main", children, className, None, **props)


def aside(*children: Child, className: str = None, **props) -> dict:
    """Create an aside element."""
    return _element("aside", children, className, None, **props)


def nav(*children: Child, className: str = None, **props) -> dict:
    """Create a nav element."""
    return _element("nav", children, className, None, **props)


# Text Components

def h1(content: str, className: str = None, **props) -> dict:
    """Create an h1 heading."""
    return {"type": "h1", "props": {"content": content, "className": className, **props}}


def h2(content: str, className: str = None, **props) -> dict:
    """Create an h2 heading."""
    return {"type": "h2", "props": {"content": content, "className": className, **props}}


def h3(content: str, className: str = None, **props) -> dict:
    """Create an h3 heading."""
    return {"type": "h3", "props": {"content": content, "className": className, **props}}


def h4(content: str, className: str = None, **props) -> dict:
    """Create an h4 heading."""
    return {"type": "h4", "props": {"content": content, "className": className, **props}}


def p(content: str, className: str = None, **props) -> dict:
    """Create a paragraph."""
    return {"type": "p", "props": {"content": content, "className": className, **props}}


def pre(content: str, className: str = None, **props) -> dict:
    """Create a preformatted text block."""
    return {"type": "pre", "props": {"content": content, "className": className, **props}}


def label(content: str, className: str = None, **props) -> dict:
    """Create a label element."""
    return {"type": "label", "props": {"content": content, "className": className, **props}}


# Form Components

def button(
    content: str,
    onClick: str = None,
    className: str = None,
    disabled: bool = False,
    **props
) -> dict:
    """Create a button element."""
    return {
        "type": "button",
        "props": {
            "content": content,
            "onClick": onClick,
            "className": className,
            "disabled": disabled,
            **props
        }
    }


def input(
    type: str = "text",
    value: Any = None,
    onChange: str = None,
    placeholder: str = None,
    className: str = None,
    readOnly: bool = False,
    **props
) -> dict:
    """Create an input element."""
    p = {"type": type, "className": className, **props}
    if value is not None:
        p["value"] = value
    if onChange:
        p["onChange"] = onChange
    if placeholder:
        p["placeholder"] = placeholder
    if readOnly:
        p["readOnly"] = True
    return {"type": "input", "props": p}


def textarea(
    value: str = "",
    onChange: str = None,
    placeholder: str = None,
    className: str = None,
    rows: int = 4,
    readOnly: bool = False,
    **props
) -> dict:
    """Create a textarea element."""
    return {
        "type": "textarea",
        "props": {
            "value": value,
            "onChange": onChange,
            "placeholder": placeholder,
            "className": className,
            "rows": rows,
            "readOnly": readOnly,
            **props
        }
    }


def select(
    value: Any,
    onChange: str,
    options: List[Tuple[str, str]],
    className: str = None,
    **props
) -> dict:
    """
    Create a select dropdown with options.

    Args:
        value: Currently selected value
        onChange: Event name to fire on change
        options: List of (value, label) tuples
        className: CSS class name

    Usage:
        select(
            value=uuid_version.value,
            onChange="uuid:version",
            options=[("1", "UUID v1"), ("4", "UUID v4")]
        )
    """
    return {
        "type": "select",
        "props": {
            "value": value,
            "onChange": onChange,
            "className": className,
            "children": [
                {"type": "option", "props": {"value": v, "content": lbl}}
                for v, lbl in options
            ],
            **props
        }
    }


def checkbox(
    checked: bool = False,
    onChange: str = None,
    label_text: str = None,
    className: str = None,
    **props
) -> dict:
    """
    Create a checkbox, optionally with a label.

    Usage:
        checkbox(checked=True, onChange="toggle:feature", label_text="Enable feature")
    """
    checkbox_input = {
        "type": "input",
        "props": {
            "type": "checkbox",
            "checked": checked,
            "onChange": onChange,
            **props
        }
    }

    if label_text:
        return {
            "type": "label",
            "props": {
                "className": className or "checkbox-label",
                "children": [
                    checkbox_input,
                    span(label_text)
                ]
            }
        }

    return checkbox_input


def range_input(
    value: int,
    onChange: str,
    min: int = 0,
    max: int = 100,
    step: int = 1,
    className: str = None,
    **props
) -> dict:
    """Create a range/slider input."""
    return {
        "type": "input",
        "props": {
            "type": "range",
            "value": value,
            "onChange": onChange,
            "min": min,
            "max": max,
            "step": step,
            "className": className,
            **props
        }
    }


# Composite Helpers

def labeled(label_text: str, child: dict, className: str = "input-group") -> dict:
    """
    Wrap a component with a label.

    Usage:
        labeled("Password Length:", range_input(value=16, onChange="pwd:length"))
    """
    return div(
        label(label_text),
        child,
        className=className
    )


def labeled_value(label_text: str, value: Any, className: str = "input-group") -> dict:
    """
    Create a label that includes the current value.

    Usage:
        labeled_value("Length:", pwd_length.value)  # Shows "Length: 16"
    """
    return label(f"{label_text} {value}", className=className)


def result_row(
    label_text: str,
    value: str,
    copy_button: bool = True,
    className: str = "result-row"
) -> dict:
    """
    Create a result row with label, readonly input, and optional copy button.

    This is the common pattern used throughout cacao_tools.

    Usage:
        result_row("MD5", hash_results.value.get("md5", ""))
    """
    children = [
        label(label_text, className="result-label"),
        input(value=value, readOnly=True, className="result-value")
    ]

    if copy_button and value:
        children.append(
            button("Copy", onClick=f"copy:{value}", className="btn btn-sm")
        )

    return div(*children, className=className)


def icon(name: str, className: str = None) -> dict:
    """
    Create an icon element (Font Awesome style).

    Usage:
        icon("fa-solid fa-lock")
    """
    full_class = name if not className else f"{name} {className}"
    return {"type": "i", "props": {"className": full_class}}


def link(content: str, href: str, className: str = None, **props) -> dict:
    """Create a link element."""
    return {
        "type": "a",
        "props": {"content": content, "href": href, "className": className, **props}
    }


def img(src: str, alt: str = "", className: str = None, **props) -> dict:
    """Create an image element."""
    return {
        "type": "img",
        "props": {"src": src, "alt": alt, "className": className, **props}
    }


# Layout Helpers

def flex(*children: Child, direction: str = "row", gap: int = None, **props) -> dict:
    """
    Create a flex container.

    Usage:
        flex(button("A"), button("B"), gap=10)
        flex(child1, child2, direction="column")
    """
    style = {"display": "flex", "flexDirection": direction}
    if gap:
        style["gap"] = f"{gap}px"
    return div(*children, style=style, **props)


def flex_center(*children: Child, **props) -> dict:
    """Create a centered flex container."""
    style = {
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center"
    }
    return div(*children, style=style, **props)


def grid(*children: Child, columns: int = 2, gap: int = 16, **props) -> dict:
    """
    Create a CSS grid container.

    Usage:
        grid(card1, card2, card3, card4, columns=2, gap=20)
    """
    style = {
        "display": "grid",
        "gridTemplateColumns": f"repeat({columns}, 1fr)",
        "gap": f"{gap}px"
    }
    return div(*children, style=style, **props)


# Tool Container (common pattern in cacao_tools)

def tool_container(
    title: str,
    description: str,
    *body_children: Child,
    className: str = "tool-container"
) -> dict:
    """
    Create a standard tool container with header and body.

    This encapsulates the common pattern from cacao_tools.

    Usage:
        tool_container(
            "Hash Text",
            "Generate hashes using MD5, SHA1, SHA256, SHA512",
            textarea(value=hash_input.value, onChange="hash:input"),
            button("Generate", onClick="hash:generate"),
            div(*hash_results, className="hash-results")
        )
    """
    return div(
        div(
            h2(title),
            p(description),
            className="tool-header"
        ),
        div(*body_children, className="tool-body"),
        className=className
    )


def dual_pane(
    left_label: str,
    left_content: dict,
    right_label: str,
    right_content: dict,
    className: str = "dual-pane"
) -> dict:
    """
    Create a side-by-side dual pane layout.

    Common pattern for encode/decode, diff, etc.

    Usage:
        dual_pane(
            "Input", textarea(value=input_val, onChange="input"),
            "Output", textarea(value=output_val, readOnly=True)
        )
    """
    return div(
        div(label(left_label), left_content, className="pane"),
        div(label(right_label), right_content, className="pane"),
        className=className
    )


def mode_toggle(
    modes: List[Tuple[str, str, str]],
    current_mode: str,
    className: str = "mode-toggle"
) -> dict:
    """
    Create a mode toggle button group.

    Args:
        modes: List of (mode_value, label, event) tuples
        current_mode: Currently active mode value
        className: CSS class name

    Usage:
        mode_toggle(
            [("encode", "Encode", "b64:mode:encode"),
             ("decode", "Decode", "b64:mode:decode")],
            current_mode=b64_mode.value
        )
    """
    buttons = [
        button(
            lbl,
            onClick=evt,
            className=f"btn {'btn-primary' if mode == current_mode else 'btn-secondary'}"
        )
        for mode, lbl, evt in modes
    ]
    return div(*buttons, className=className)


def stat_card(
    label_text: str,
    value: Any,
    icon_class: str = None,
    className: str = "stat-card"
) -> dict:
    """
    Create a statistics card with icon, value, and label.

    Usage:
        stat_card("Words", 42, icon_class="fa-solid fa-font")
    """
    children = []
    if icon_class:
        children.append(icon(icon_class))
    children.extend([
        div(str(value), className="stat-value"),
        div(label_text, className="stat-label")
    ])
    return div(*children, className=className)
