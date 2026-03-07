"""
Interactive API Reference — self-hosted Cacao app.

Run with: cacao run docs/api_reference.py
"""
import inspect
import re
from typing import Any

import cacao as c
from cacao.server import ui as _ui_module
from cacao.server import chart as _chart_module

c.config(title="Cacao API Reference", theme="dark")

# ---------------------------------------------------------------------------
# Collect all public API functions
# ---------------------------------------------------------------------------

_CATEGORIES: dict[str, list[dict[str, Any]]] = {
    "Layout": [],
    "Typography": [],
    "Display": [],
    "Form": [],
    "Charts": [],
    "Navigation": [],
    "AI & LLM": [],
    "State & Events": [],
    "App & Config": [],
}

_CATEGORY_MAP: dict[str, str] = {
    # Layout
    "row": "Layout", "col": "Layout", "grid": "Layout", "container": "Layout",
    "stack": "Layout", "split": "Layout", "hero": "Layout", "card": "Layout",
    "app_shell": "Layout", "nav_sidebar": "Layout", "shell_content": "Layout",
    "panel": "Layout", "layout": "Layout", "modal": "Layout",
    # Typography
    "title": "Typography", "text": "Typography", "html": "Typography",
    "raw_html": "Typography", "markdown": "Typography", "code": "Typography",
    "divider": "Typography", "spacer": "Typography",
    # Display
    "metric": "Display", "table": "Display", "json": "Display",
    "json_view": "Display", "progress": "Display", "badge": "Display",
    "alert": "Display", "accordion": "Display", "steps": "Display",
    "file_tree": "Display", "timeline": "Display", "diff": "Display",
    "image": "Display", "video": "Display", "tooltip": "Display",
    "virtual_list": "Display",
    # Form
    "button": "Form", "input": "Form", "input_field": "Form",
    "textarea": "Form", "select": "Form", "checkbox": "Form",
    "switch": "Form", "slider": "Form", "date": "Form",
    "date_picker": "Form", "upload": "Form", "file_upload": "Form",
    "search_input": "Form",
    # Charts
    "line": "Charts", "bar": "Charts", "pie": "Charts",
    "area": "Charts", "scatter": "Charts", "gauge": "Charts",
    # Navigation
    "tabs": "Navigation", "tab": "Navigation", "breadcrumb": "Navigation",
    "sidebar": "Navigation", "subnav": "Navigation", "anchor": "Navigation",
    "link_card": "Navigation",
    # AI & LLM
    "chat": "AI & LLM", "stream": "AI & LLM", "interface": "AI & LLM",
    "parallel": "AI & LLM", "series": "AI & LLM", "compare": "AI & LLM",
    "extract": "AI & LLM", "agent": "AI & LLM", "multi_agent": "AI & LLM",
    "cost_dashboard": "AI & LLM", "document_upload": "AI & LLM",
    "model_picker": "AI & LLM", "tool_timeline": "AI & LLM",
    "budget_gauge": "AI & LLM",
    # State & Events
    "signal": "State & Events", "computed": "State & Events",
    "on": "State & Events", "bind": "State & Events",
    "use": "State & Events", "emit": "State & Events",
    "listen": "State & Events", "shortcut": "State & Events",
    # App & Config
    "config": "App & Config", "page": "App & Config", "run": "App & Config",
    "register_plugin": "App & Config", "register_theme": "App & Config",
    "require_auth": "App & Config", "permission": "App & Config",
    "notify": "App & Config", "static_handler": "App & Config",
    "static_script": "App & Config", "test": "App & Config",
    "export_static": "App & Config",
}


def _get_signature(fn: Any) -> str:
    """Get a clean function signature string."""
    try:
        sig = inspect.signature(fn)
        params = []
        for name, param in sig.parameters.items():
            if name in ("props", "kwargs"):
                params.append("**props")
                continue
            if param.kind == param.VAR_KEYWORD:
                params.append(f"**{name}")
                continue
            if param.kind == param.VAR_POSITIONAL:
                params.append(f"*{name}")
                continue

            annotation = ""
            if param.annotation != inspect.Parameter.empty:
                ann = param.annotation
                if hasattr(ann, "__name__"):
                    annotation = f": {ann.__name__}"
                else:
                    annotation = f": {ann}"

            default = ""
            if param.default != inspect.Parameter.empty:
                default = f" = {param.default!r}"

            if param.kind == param.KEYWORD_ONLY:
                params.append(f"{name}{annotation}{default}")
            else:
                params.append(f"{name}{annotation}{default}")

        return f"({', '.join(params)})"
    except (ValueError, TypeError):
        return "(...)"


def _get_docstring(fn: Any) -> str:
    """Get a cleaned-up docstring."""
    doc = inspect.getdoc(fn) or "No documentation available."
    return doc


def _extract_example(doc: str) -> str:
    """Extract example code from a docstring."""
    lines = doc.split("\n")
    in_example = False
    example_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("example"):
            in_example = True
            continue
        if in_example:
            if stripped.startswith("Args:") or stripped.startswith("Returns:"):
                break
            example_lines.append(line)

    code = "\n".join(example_lines).strip()
    # Remove leading indentation uniformly
    if code:
        code_lines = code.split("\n")
        min_indent = min(
            (len(l) - len(l.lstrip()) for l in code_lines if l.strip()),
            default=0,
        )
        code = "\n".join(l[min_indent:] for l in code_lines)
    return code


# Build the reference data
_simple_module = c
_seen: set[str] = set()

for func_name, category in _CATEGORY_MAP.items():
    if func_name in _seen:
        continue
    _seen.add(func_name)

    fn = getattr(_simple_module, func_name, None)
    if fn is None:
        continue

    sig = _get_signature(fn)
    doc = _get_docstring(fn)
    example = _extract_example(doc)

    _CATEGORIES[category].append({
        "name": func_name,
        "signature": sig,
        "docstring": doc,
        "example": example,
    })

# Sort each category alphabetically
for cat in _CATEGORIES:
    _CATEGORIES[cat].sort(key=lambda x: x["name"])

# ---------------------------------------------------------------------------
# Build the UI
# ---------------------------------------------------------------------------

with c.page("/"):
    c.title("Cacao API Reference", level=1)
    c.text("Interactive documentation for all Cacao components and functions.", color="muted")
    c.spacer()

    # Quick stats
    total = sum(len(v) for v in _CATEGORIES.values())
    with c.row():
        c.metric("Total Functions", str(total))
        c.metric("Categories", str(len(_CATEGORIES)))
        c.metric("Framework", "Cacao v2")

    c.spacer()

    # Category navigation
    with c.tabs(default="Layout"):
        for cat_name, entries in _CATEGORIES.items():
            if not entries:
                continue
            with c.tab(cat_name, label=f"{cat_name} ({len(entries)})"):
                c.spacer(2)
                for entry in entries:
                    with c.accordion():
                        with c.accordion_item(
                            f"c.{entry['name']}{entry['signature']}",
                        ):
                            # Docstring
                            doc_text = entry["docstring"]
                            # Split into summary and details
                            parts = doc_text.split("\n\n", 1)
                            c.text(parts[0], size="md")

                            if len(parts) > 1:
                                c.spacer(2)
                                c.markdown(parts[1])

                            # Example code
                            if entry["example"]:
                                c.spacer(2)
                                c.code(entry["example"], language="python")

for cat_name, entries in _CATEGORIES.items():
    if not entries:
        continue
    page_path = f"/{cat_name.lower().replace(' & ', '-').replace(' ', '-')}"
    with c.page(page_path):
        c.title(cat_name, level=1)
        c.text(f"All {cat_name.lower()} components and functions.", color="muted")
        c.spacer()

        for entry in entries:
            with c.card(f"c.{entry['name']}"):
                c.code(
                    f"c.{entry['name']}{entry['signature']}",
                    language="python",
                )
                c.spacer(2)
                c.markdown(entry["docstring"])
                if entry["example"]:
                    c.spacer(2)
                    c.text("Example", size="sm", color="muted")
                    c.code(entry["example"], language="python")
            c.spacer()
