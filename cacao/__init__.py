"""
Cacao v2 - Reactive web framework for Python.

Simple API (recommended):
    import cacao_v2 as c

    c.config(title="My App")
    c.title("Hello World")
    with c.row():
        c.metric("Users", 100)

Full API (for advanced usage):
    from cacao_v2.server.ui import App, row, metric

    app = App(title="My App")
    with app.page("/"):
        with row():
            metric("Users", 100)
    app.run()
"""

<<<<<<< Updated upstream
__version__ = "1.0.50.dev1"
=======
# Import everything from the simple module for easy access
from .simple import (
    # Config
    config,
    # State
    signal,
    computed,
    Signal,
    Computed,
    # Events
    on,
    bind,
    # Pages
    page,
    # Layout
    row,
    col,
    grid,
    card,
    sidebar,
    tabs,
    tab,
    # Typography
    title,
    text,
    code,
    divider,
    spacer,
    # Data Display
    metric,
    table,
    json,
    json_view,
    progress,
    badge,
    alert,
    # Forms
    button,
    input,
    input_field,
    field,
    select,
    checkbox,
    switch,
    slider,
    date,
    date_picker,
    upload,
    file_upload,
    # Charts
    line,
    bar,
    pie,
    area,
    scatter,
    gauge,
    # Data
    load_csv,
    load_json,
    sample_sales_data,
    sample_users_data,
    # App
    run,
    get_app,
    is_simple_mode,
    reset,
)
>>>>>>> Stashed changes

# Also expose the full server module for advanced usage
from . import server

# Keep App accessible at top level for those who want it
from .server.ui import App
from .server.session import Session

__all__ = [
    # Simple API
    "config",
    "signal",
    "computed",
    "Signal",
    "Computed",
    "on",
    "bind",
    "page",
    "row",
    "col",
    "grid",
    "card",
    "sidebar",
    "tabs",
    "tab",
    "title",
    "text",
    "code",
    "divider",
    "spacer",
    "metric",
    "table",
    "json",
    "json_view",
    "progress",
    "badge",
    "alert",
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
    # Full API
    "server",
    "App",
    "Session",
]

__version__ = "2.0.0-dev"
