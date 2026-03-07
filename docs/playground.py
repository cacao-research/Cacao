"""
Component Playground — Edit props live, see result.

Run with: cacao run docs/playground.py
"""
from typing import Any

import cacao as c

c.config(title="Cacao Playground", theme="dark")

# ---------------------------------------------------------------------------
# Signals for playground state
# ---------------------------------------------------------------------------
selected_component = c.signal("button", name="selected_component")

# -- Button props --
btn_label = c.signal("Click Me", name="btn_label")
btn_variant = c.signal("primary", name="btn_variant")
btn_size = c.signal("md", name="btn_size")
btn_disabled = c.signal(False, name="btn_disabled")

# -- Metric props --
met_label = c.signal("Revenue", name="met_label")
met_value = c.signal("$45,231", name="met_value")
met_trend = c.signal("+20.1%", name="met_trend")
met_direction = c.signal("up", name="met_direction")

# -- Alert props --
alert_message = c.signal("This is an alert message.", name="alert_message")
alert_variant = c.signal("info", name="alert_variant")
alert_title = c.signal("Heads up!", name="alert_title")

# -- Badge props --
badge_text = c.signal("New", name="badge_text")
badge_variant = c.signal("primary", name="badge_variant")

# -- Progress props --
progress_value = c.signal(65, name="progress_value")
progress_label = c.signal("Loading...", name="progress_label")
progress_variant = c.signal("primary", name="progress_variant")

# -- Text props --
text_content = c.signal("Hello, world!", name="text_content")
text_size = c.signal("md", name="text_size")
text_color = c.signal("", name="text_color")

# -- Title props --
title_text = c.signal("Page Title", name="title_text")
title_level = c.signal(1, name="title_level")

# -- Input props --
input_label = c.signal("Name", name="input_label")
input_placeholder = c.signal("Enter your name", name="input_placeholder")
input_type = c.signal("text", name="input_type")
input_disabled = c.signal(False, name="input_disabled")

# -- Slider props --
slider_label = c.signal("Volume", name="slider_label")
slider_min = c.signal(0, name="slider_min")
slider_max = c.signal(100, name="slider_max")
slider_step = c.signal(1, name="slider_step")

# -- Code props --
code_content = c.signal('print("Hello, Cacao!")', name="code_content")
code_language = c.signal("python", name="code_language")

# ---------------------------------------------------------------------------
# Component registry — maps component name to (props_builder, renderer, code_gen)
# ---------------------------------------------------------------------------

COMPONENTS: dict[str, dict[str, Any]] = {
    "button": {
        "label": "Button",
        "description": "Interactive button with variants and sizes.",
        "props": [
            {"signal": btn_label, "label": "Label", "type": "input"},
            {"signal": btn_variant, "label": "Variant", "type": "select",
             "options": ["primary", "secondary", "danger", "ghost"]},
            {"signal": btn_size, "label": "Size", "type": "select",
             "options": ["sm", "md", "lg"]},
            {"signal": btn_disabled, "label": "Disabled", "type": "checkbox"},
        ],
    },
    "metric": {
        "label": "Metric",
        "description": "Display a key metric value with optional trend.",
        "props": [
            {"signal": met_label, "label": "Label", "type": "input"},
            {"signal": met_value, "label": "Value", "type": "input"},
            {"signal": met_trend, "label": "Trend", "type": "input"},
            {"signal": met_direction, "label": "Direction", "type": "select",
             "options": ["up", "down"]},
        ],
    },
    "alert": {
        "label": "Alert",
        "description": "Status alert with message and variant.",
        "props": [
            {"signal": alert_title, "label": "Title", "type": "input"},
            {"signal": alert_message, "label": "Message", "type": "input"},
            {"signal": alert_variant, "label": "Variant", "type": "select",
             "options": ["info", "success", "warning", "error"]},
        ],
    },
    "badge": {
        "label": "Badge",
        "description": "Small label badge with color variants.",
        "props": [
            {"signal": badge_text, "label": "Text", "type": "input"},
            {"signal": badge_variant, "label": "Variant", "type": "select",
             "options": ["primary", "secondary", "success", "warning", "danger"]},
        ],
    },
    "progress": {
        "label": "Progress",
        "description": "Progress bar with value and label.",
        "props": [
            {"signal": progress_value, "label": "Value (0-100)", "type": "slider",
             "min": 0, "max": 100},
            {"signal": progress_label, "label": "Label", "type": "input"},
            {"signal": progress_variant, "label": "Variant", "type": "select",
             "options": ["primary", "success", "warning", "danger"]},
        ],
    },
    "text": {
        "label": "Text",
        "description": "Text display with size and color options.",
        "props": [
            {"signal": text_content, "label": "Content", "type": "input"},
            {"signal": text_size, "label": "Size", "type": "select",
             "options": ["xs", "sm", "md", "lg", "xl"]},
            {"signal": text_color, "label": "Color", "type": "input"},
        ],
    },
    "title": {
        "label": "Title",
        "description": "Heading element with level control.",
        "props": [
            {"signal": title_text, "label": "Text", "type": "input"},
            {"signal": title_level, "label": "Level (1-6)", "type": "slider",
             "min": 1, "max": 6},
        ],
    },
    "input": {
        "label": "Input",
        "description": "Text input field with label, placeholder, and type.",
        "props": [
            {"signal": input_label, "label": "Label", "type": "input"},
            {"signal": input_placeholder, "label": "Placeholder", "type": "input"},
            {"signal": input_type, "label": "Type", "type": "select",
             "options": ["text", "password", "email", "number"]},
            {"signal": input_disabled, "label": "Disabled", "type": "checkbox"},
        ],
    },
    "slider": {
        "label": "Slider",
        "description": "Range slider with min, max, and step.",
        "props": [
            {"signal": slider_label, "label": "Label", "type": "input"},
            {"signal": slider_min, "label": "Min", "type": "slider", "min": 0, "max": 100},
            {"signal": slider_max, "label": "Max", "type": "slider", "min": 0, "max": 1000},
            {"signal": slider_step, "label": "Step", "type": "slider", "min": 1, "max": 50},
        ],
    },
    "code": {
        "label": "Code",
        "description": "Syntax-highlighted code block.",
        "props": [
            {"signal": code_content, "label": "Content", "type": "input"},
            {"signal": code_language, "label": "Language", "type": "select",
             "options": ["python", "javascript", "html", "css", "json", "bash"]},
        ],
    },
}

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

c.title("Component Playground")
c.text("Edit props on the left, see the live result on the right.", color="muted")
c.spacer()

with c.layout("split", ratio="1:2") as l:
    with l.left():
        with c.card("Component"):
            c.select(
                "Select Component",
                options=list(COMPONENTS.keys()),
                signal=selected_component,
            )
        c.spacer()

        # Render props editors for each component (all are present, visibility
        # is controlled by the selected_component signal on the client)
        for comp_name, comp_info in COMPONENTS.items():
            with c.card(f"{comp_info['label']} Props", visible=f"${{selected_component}} === '{comp_name}'"):
                c.text(comp_info["description"], size="sm", color="muted")
                c.spacer(2)
                for prop in comp_info["props"]:
                    if prop["type"] == "input":
                        c.input(prop["label"], signal=prop["signal"])
                    elif prop["type"] == "select":
                        c.select(prop["label"], options=prop["options"], signal=prop["signal"])
                    elif prop["type"] == "checkbox":
                        c.checkbox(prop["label"], signal=prop["signal"])
                    elif prop["type"] == "slider":
                        c.slider(
                            prop["label"],
                            signal=prop["signal"],
                            min=prop.get("min", 0),
                            max=prop.get("max", 100),
                            step=prop.get("step", 1),
                        )

    with l.right():
        with c.card("Preview"):
            c.text("Live component preview", size="sm", color="muted")
            c.spacer()

            # Button preview
            c.button(
                btn_label,
                variant=btn_variant,
                size=btn_size,
                disabled=btn_disabled,
                visible=f"${{selected_component}} === 'button'",
            )

            # Metric preview
            c.metric(
                met_label,
                met_value,
                trend=met_trend,
                trend_direction=met_direction,
                visible=f"${{selected_component}} === 'metric'",
            )

            # Alert preview
            c.alert(
                alert_message,
                title=alert_title,
                variant=alert_variant,
                visible=f"${{selected_component}} === 'alert'",
            )

            # Badge preview
            c.badge(
                badge_text,
                variant=badge_variant,
                visible=f"${{selected_component}} === 'badge'",
            )

            # Progress preview
            c.progress(
                progress_value,
                label=progress_label,
                variant=progress_variant,
                visible=f"${{selected_component}} === 'progress'",
            )

            # Text preview
            c.text(
                text_content,
                size=text_size,
                color=text_color,
                visible=f"${{selected_component}} === 'text'",
            )

            # Title preview
            c.title(
                title_text,
                level=title_level,
                visible=f"${{selected_component}} === 'title'",
            )

            # Input preview
            c.input(
                input_label,
                placeholder=input_placeholder,
                type=input_type,
                disabled=input_disabled,
                visible=f"${{selected_component}} === 'input'",
            )

            # Slider preview
            c.slider(
                slider_label,
                min=slider_min,
                max=slider_max,
                step=slider_step,
                visible=f"${{selected_component}} === 'slider'",
            )

            # Code preview
            c.code(
                code_content,
                language=code_language,
                visible=f"${{selected_component}} === 'code'",
            )

        c.spacer()

        with c.card("Generated Code"):
            c.text("Copy this code into your app", size="sm", color="muted")
            c.spacer()
            # Show code for each component type
            c.code(
                'c.button("Click Me", variant="primary", size="md")',
                language="python",
                visible=f"${{selected_component}} === 'button'",
            )
            c.code(
                'c.metric("Revenue", "$45,231", trend="+20.1%", trend_direction="up")',
                language="python",
                visible=f"${{selected_component}} === 'metric'",
            )
            c.code(
                'c.alert("This is an alert.", title="Heads up!", variant="info")',
                language="python",
                visible=f"${{selected_component}} === 'alert'",
            )
            c.code(
                'c.badge("New", variant="primary")',
                language="python",
                visible=f"${{selected_component}} === 'badge'",
            )
            c.code(
                'c.progress(65, label="Loading...", variant="primary")',
                language="python",
                visible=f"${{selected_component}} === 'progress'",
            )
            c.code(
                'c.text("Hello, world!", size="md")',
                language="python",
                visible=f"${{selected_component}} === 'text'",
            )
            c.code(
                'c.title("Page Title", level=1)',
                language="python",
                visible=f"${{selected_component}} === 'title'",
            )
            c.code(
                'c.input("Name", placeholder="Enter your name", type="text")',
                language="python",
                visible=f"${{selected_component}} === 'input'",
            )
            c.code(
                'c.slider("Volume", min=0, max=100, step=1)',
                language="python",
                visible=f"${{selected_component}} === 'slider'",
            )
            c.code(
                'c.code("print(\\"Hello\\")", language="python")',
                language="python",
                visible=f"${{selected_component}} === 'code'",
            )
