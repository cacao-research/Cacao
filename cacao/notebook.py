"""
Jupyter notebook integration for Cacao.

Provides:
- c.display() for rendering Cacao components inline in Jupyter
- Reactive mode for auto-updating outputs when signals change
- Notebook-to-app conversion utilities
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from .server.signal import Signal
from .server.ui import Component, _current_container


def _in_jupyter() -> bool:
    """Check if we're running inside a Jupyter notebook."""
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell is None:
            return False
        return shell.__class__.__name__ in (
            "ZMQInteractiveShell",
            "TerminalInteractiveShell",
        )
    except (ImportError, NameError):
        return False


def _in_ipython() -> bool:
    """Check if IPython is available."""
    try:
        from IPython import get_ipython

        return get_ipython() is not None
    except (ImportError, NameError):
        return False


def _get_frontend_assets() -> tuple[str, str]:
    """Load the bundled CSS and JS from frontend/dist."""
    dist_dir = Path(__file__).parent / "frontend" / "dist"

    css_content = ""
    js_content = ""

    css_path = dist_dir / "cacao.css"
    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")

    js_path = dist_dir / "cacao.js"
    if js_path.exists():
        js_content = js_path.read_text(encoding="utf-8")

    return css_content, js_content


# Cache assets so we only read from disk once per session
_cached_assets: tuple[str, str] | None = None


def _get_cached_assets() -> tuple[str, str]:
    """Get cached frontend assets."""
    global _cached_assets
    if _cached_assets is None:
        _cached_assets = _get_frontend_assets()
    return _cached_assets


def _serialize_components(components: list[Component]) -> list[dict[str, Any]]:
    """Serialize a list of components to JSON-serializable dicts."""
    return [c.to_dict() for c in components]


def _build_iframe_html(
    components_json: str,
    signals_json: str,
    *,
    theme: str = "dark",
    title: str = "Cacao",
    width: str = "100%",
    height: str = "400px",
    handlers_json: str = "{}",
) -> str:
    """Build an HTML iframe containing a self-contained Cacao render."""
    css_content, js_content = _get_cached_assets()
    frame_id = f"cacao-frame-{uuid.uuid4().hex[:8]}"

    # Use srcdoc for self-contained iframe
    inner_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css_content}</style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"><\\/script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"><\\/script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"><\\/script>
    <style>
        body {{ margin: 0; padding: 8px; background: transparent; }}
        .loading {{ display: flex; align-items: center; justify-content: center;
                    height: 100%; color: var(--text-secondary); }}
    </style>
</head>
<body>
    <div id="root"><div class="loading">Loading...</div></div>
    <script>
        window.__CACAO_STATIC__ = true;
        window.__CACAO_DEFER_MOUNT__ = true;
        window.__CACAO_PAGES__ = {{"pages": {{"/": {components_json}}}, "metadata": {{"title": "{title}", "theme": "{theme}"}}}};
        window.__CACAO_INITIAL_SIGNALS__ = {signals_json};
    <\\/script>
    <script>{js_content}<\\/script>
    <script>
        Cacao.initStatic({{
            pages: window.__CACAO_PAGES__,
            signals: window.__CACAO_INITIAL_SIGNALS__,
            handlers: {handlers_json}
        }});
        Cacao.mount();

        // Auto-resize iframe to fit content
        function notifyHeight() {{
            var h = document.documentElement.scrollHeight;
            window.parent.postMessage({{cacaoFrame: "{frame_id}", height: h}}, "*");
        }}
        new MutationObserver(notifyHeight).observe(document.body, {{childList: true, subtree: true}});
        setTimeout(notifyHeight, 100);
        setTimeout(notifyHeight, 500);
    <\\/script>
</body>
</html>"""

    # Escape for srcdoc attribute
    srcdoc = inner_html.replace("&", "&amp;").replace('"', "&quot;")

    return f"""<iframe id="{frame_id}" srcdoc="{srcdoc}"
    style="width: {width}; height: {height}; border: none; border-radius: 8px; overflow: hidden;"
    sandbox="allow-scripts allow-same-origin"></iframe>
<script>
window.addEventListener("message", function(e) {{
    if (e.data && e.data.cacaoFrame === "{frame_id}") {{
        var f = document.getElementById("{frame_id}");
        if (f) f.style.height = (e.data.height + 16) + "px";
    }}
}});
</script>"""


def display(
    *components: Component,
    theme: str | None = None,
    width: str = "100%",
    height: str = "400px",
) -> Any:
    """
    Render Cacao components inline in a Jupyter notebook.

    Takes one or more Component instances and renders them in an embedded
    iframe using the full Cacao frontend.

    Args:
        *components: Cacao Component instances to render. If none provided,
            renders the current page's components.
        theme: Theme override ("dark" or "light"). Defaults to app config.
        width: CSS width for the display area.
        height: CSS height (auto-resizes to content).

    Returns:
        IPython HTML display object.

    Example:
        import cacao as c

        # Display specific components
        c.display(c.title("Hello"), c.metric("Users", 42))

        # Display current page
        c.title("Hello")
        c.metric("Users", 42)
        c.display()
    """
    from IPython.display import HTML, display as ipython_display

    # Determine components to render
    if components:
        comp_list = list(components)
    else:
        # Use current container contents
        container = _current_container.get(None)
        if container:
            comp_list = list(container)
        else:
            comp_list = []

    if not comp_list:
        return ipython_display(HTML("<em>No components to display</em>"))

    # Serialize components
    components_json = json.dumps(_serialize_components(comp_list))

    # Gather signal values (use defaults since there's no session)
    all_signals = Signal.get_all_signals()
    signals_dict = {name: sig.default for name, sig in all_signals.items()}
    signals_json = json.dumps(signals_dict)

    # Determine theme
    if theme is None:
        try:
            from . import simple

            theme = simple._global_config.get("theme", "dark")
        except Exception:
            theme = "dark"

    # Gather static handlers
    try:
        from . import simple

        handlers = dict(simple._static_handlers)
    except Exception:
        handlers = {}

    handler_entries = [f'"{k}": {v}' for k, v in handlers.items()]
    handlers_js = "{" + ", ".join(handler_entries) + "}" if handler_entries else "{}"

    html = _build_iframe_html(
        components_json,
        signals_json,
        theme=theme,
        width=width,
        height=height,
        handlers_json=handlers_js,
    )

    return ipython_display(HTML(html))


# =========================================================================
# Reactive Mode
# =========================================================================

_reactive_displays: dict[str, dict[str, Any]] = {}
_reactive_mode: bool = False


def _enable_reactive_mode() -> None:
    """Enable Marimo-style reactive mode in notebooks.

    When active, signal changes auto-update any displayed components
    that reference those signals.
    """
    global _reactive_mode
    if _reactive_mode:
        return
    _reactive_mode = True


def _disable_reactive_mode() -> None:
    """Disable reactive mode."""
    global _reactive_mode
    _reactive_mode = False
    _reactive_displays.clear()


class ReactiveDisplay:
    """A display handle that auto-updates when signals change.

    Usage:
        rd = c.reactive(c.metric("Users", c.signal("count", 0)))
        # Later, changing the signal auto-updates the display:
        count.set(None, 42)  # re-renders in notebook
    """

    def __init__(
        self,
        components: list[Component],
        *,
        theme: str = "dark",
        width: str = "100%",
        height: str = "400px",
    ) -> None:
        self._components = components
        self._theme = theme
        self._width = width
        self._height = height
        self._display_id = f"cacao-reactive-{uuid.uuid4().hex[:8]}"
        self._display_handle: Any = None
        self._subscriptions: list[Any] = []
        self._setup_subscriptions()

    def _setup_subscriptions(self) -> None:
        """Subscribe to all signals referenced by components."""
        # Find all signals referenced in the component tree
        signal_names = self._find_signal_refs(self._components)
        all_signals = Signal.get_all_signals()

        for name in signal_names:
            if name in all_signals:
                sig = all_signals[name]
                unsub = sig.subscribe(lambda _name, _val, _sess: self._refresh())
                self._subscriptions.append(unsub)

    def _find_signal_refs(self, components: list[Component]) -> set[str]:
        """Recursively find signal references in component tree."""
        refs: set[str] = set()
        for comp in components:
            if comp.props:
                for _key, val in comp.props.items():
                    if isinstance(val, Signal):
                        refs.add(val.name)
                    elif isinstance(val, str) and val.startswith("$$signal:"):
                        refs.add(val.split(":", 1)[1])
            if comp.children:
                refs.update(self._find_signal_refs(comp.children))
        return refs

    def _render_html(self) -> str:
        """Generate current HTML."""
        components_json = json.dumps(_serialize_components(self._components))
        all_signals = Signal.get_all_signals()
        signals_dict = {name: sig.default for name, sig in all_signals.items()}
        signals_json = json.dumps(signals_dict)

        handler_entries = []
        try:
            from . import simple

            for k, v in simple._static_handlers.items():
                handler_entries.append(f'"{k}": {v}')
        except Exception:
            pass
        handlers_js = "{" + ", ".join(handler_entries) + "}" if handler_entries else "{}"

        return _build_iframe_html(
            components_json,
            signals_json,
            theme=self._theme,
            width=self._width,
            height=self._height,
            handlers_json=handlers_js,
        )

    def _refresh(self) -> None:
        """Re-render the display with current signal values."""
        if self._display_handle is not None:
            try:
                from IPython.display import HTML

                self._display_handle.update(HTML(self._render_html()))
            except Exception:
                pass

    def show(self) -> Any:
        """Display in the notebook and return the handle."""
        from IPython.display import HTML, display as ipython_display

        self._display_handle = ipython_display(
            HTML(self._render_html()), display_id=self._display_id
        )
        return self._display_handle

    def close(self) -> None:
        """Unsubscribe from signals and stop updates."""
        for unsub in self._subscriptions:
            if callable(unsub):
                unsub()
        self._subscriptions.clear()

    def _repr_html_(self) -> str:
        """Render when used as the last expression in a cell."""
        return self._render_html()


def reactive(
    *components: Component,
    theme: str | None = None,
    width: str = "100%",
    height: str = "400px",
) -> ReactiveDisplay:
    """
    Create a reactive display that auto-updates when signals change.

    Like c.display(), but the output re-renders whenever any referenced
    signal value changes — Marimo-style reactivity in Jupyter.

    Args:
        *components: Cacao Components to render.
        theme: Theme override.
        width: CSS width.
        height: CSS height.

    Returns:
        ReactiveDisplay handle. Call .show() to render, or use as
        the last expression in a cell.

    Example:
        import cacao as c

        count = c.signal("count", 0)
        rd = c.reactive(c.metric("Count", count))
        rd.show()

        # In another cell:
        count.set(None, 42)  # display auto-updates
    """
    _enable_reactive_mode()

    if theme is None:
        try:
            from . import simple

            theme = simple._global_config.get("theme", "dark")
        except Exception:
            theme = "dark"

    comp_list = list(components) if components else []
    if not comp_list:
        container = _current_container.get(None)
        if container:
            comp_list = list(container)

    rd = ReactiveDisplay(comp_list, theme=theme, width=width, height=height)
    rd.show()
    return rd


# =========================================================================
# Notebook-to-App Conversion
# =========================================================================


def convert_notebook(
    notebook_path: str | Path,
    output_path: str | Path | None = None,
    *,
    include_markdown: bool = True,
    include_outputs: bool = False,
) -> str:
    """
    Convert a Jupyter notebook to a Cacao app.

    Extracts Python code cells from a .ipynb file, filters for Cacao-relevant
    code, and generates a standalone app.py.

    Args:
        notebook_path: Path to the .ipynb file.
        output_path: Output .py file path. Defaults to same name with .py extension.
        include_markdown: Include markdown cells as c.markdown() components.
        include_outputs: Include output cells as comments.

    Returns:
        Path to the generated .py file.
    """
    notebook_path = Path(notebook_path)
    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    if not notebook_path.suffix == ".ipynb":
        raise ValueError(f"Not a notebook file: {notebook_path}")

    # Read notebook JSON
    with open(notebook_path, encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    if not cells:
        raise ValueError(f"Notebook has no cells: {notebook_path}")

    # First pass: scan all cells to extract imports and detect features
    all_imports: list[str] = []
    body_blocks: list[str] = []
    has_cacao_import = False
    has_config = False

    for cell in cells:
        cell_type = cell.get("cell_type", "")
        source = "".join(cell.get("source", []))

        if not source.strip():
            continue

        if cell_type == "markdown" and include_markdown:
            escaped = source.replace('"""', '\\"\\"\\"')
            body_blocks.append(f'c.markdown("""{escaped}""")')

        elif cell_type == "code":
            stripped = source.strip()
            if stripped in ("c.display()", "c.run()"):
                continue

            if "import cacao" in source or "from cacao" in source:
                has_cacao_import = True
            if "c.config(" in source or "cacao.config(" in source:
                has_config = True

            # Process lines: comment magics, skip display-only lines
            cell_lines = source.split("\n")
            import_part: list[str] = []
            code_part: list[str] = []

            for line in cell_lines:
                stripped_line = line.strip()
                if stripped_line.startswith("%") or stripped_line.startswith("!"):
                    import_part.append(f"# {line}")
                elif stripped_line == "c.display()":
                    continue
                elif stripped_line.startswith(("import ", "from ")) and not code_part:
                    # Collect top-of-cell imports
                    import_part.append(line)
                elif not stripped_line and not code_part:
                    # Blank line between imports
                    import_part.append(line)
                else:
                    code_part.append(line)

            # Outputs as comments
            if include_outputs:
                outputs = cell.get("outputs", [])
                for output in outputs:
                    if "text" in output:
                        text = "".join(output["text"])
                        for out_line in text.split("\n"):
                            code_part.insert(0, f"# Output: {out_line}")

            # Add imports to collection (skip duplicate cacao import)
            for imp_line in import_part:
                s = imp_line.strip()
                if s and s not in ("", "import cacao as c", "import cacao"):
                    if s not in all_imports:
                        all_imports.append(s)

            code = "\n".join(code_part).strip()
            if code:
                body_blocks.append(code)

    # Build final output
    lines: list[str] = []
    lines.append('"""')
    lines.append(f"Cacao app generated from {notebook_path.name}")
    lines.append('"""')
    lines.append("")
    lines.append("import cacao as c")

    # Add other imports
    if all_imports:
        lines.append("")
        for imp in all_imports:
            lines.append(imp)

    lines.append("")

    # Add config if not present
    if not has_config:
        lines.append('c.config(title="Converted Notebook")')
        lines.append("")

    # Add body blocks
    for block in body_blocks:
        lines.append(block)
        lines.append("")

    # Determine output path
    if output_path is None:
        output_path = notebook_path.with_suffix(".py")
    else:
        output_path = Path(output_path)

    # Write the app file
    content = "\n".join(lines).rstrip() + "\n"
    output_path.write_text(content, encoding="utf-8")

    return str(output_path)
