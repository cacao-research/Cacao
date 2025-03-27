"""
Public API for UI components in the Cacao framework.
Provides a unified namespace for building interactive UI elements.
"""

from .components.base import Component as UIComponent
from .components.inputs import Slider, Form
from .components.data import Table, Plot
from .components.layout import Grid, Column

__all__ = [
    "UIComponent",
    "Slider",
    "Form",
    "Table",
    "Plot",
    "Grid",
    "Column",
]
