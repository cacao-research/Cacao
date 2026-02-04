"""
Public API for UI components in the Cacao framework.
Provides a unified namespace for building interactive UI elements.
"""

from .components.base import Component as UIComponent
from .components.form_components import Form
from .components.data import Plot
from .components.layout import Grid, Column
from .components.react import ReactComponent

# Fluent component builders
from .builders import (
    # Layout
    div, span, section, main, aside, nav,
    # Text
    h1, h2, h3, h4, p, pre, label,
    # Form
    button, input, textarea, select, checkbox, range_input,
    # Composites
    labeled, labeled_value, result_row, icon, link, img,
    # Layout helpers
    flex, flex_center, grid,
    # Tool patterns
    tool_container, dual_pane, mode_toggle, stat_card,
)

__all__ = [
    # Class-based components
    "UIComponent",
    "Form",
    "Plot",
    "Grid",
    "Column",
    "ReactComponent",
    # Fluent builders - Layout
    "div", "span", "section", "main", "aside", "nav",
    # Fluent builders - Text
    "h1", "h2", "h3", "h4", "p", "pre", "label",
    # Fluent builders - Form
    "button", "input", "textarea", "select", "checkbox", "range_input",
    # Fluent builders - Composites
    "labeled", "labeled_value", "result_row", "icon", "link", "img",
    # Fluent builders - Layout helpers
    "flex", "flex_center", "grid",
    # Fluent builders - Tool patterns
    "tool_container", "dual_pane", "mode_toggle", "stat_card",
]
