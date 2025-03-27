"""
Data module for UI components in the Cacao framework.
Provides components for displaying data such as tables and plots.
"""

from typing import Any, Dict, List
from .base import Component

class Table(Component):
    """
    A table component for displaying tabular data.
    """
    def __init__(self, headers: List[str], rows: List[List[Any]]) -> None:
        self.headers = headers
        self.rows = rows

    def render(self) -> Dict[str, Any]:
        return {
            "type": "table",
            "props": {
                "headers": self.headers,
                "rows": self.rows
            }
        }

class Plot(Component):
    """
    A plot component for displaying charts and graphs.
    """
    def __init__(self, data: Dict[str, List[Any]], title: str = "") -> None:
        self.data = data
        self.title = title

    def render(self) -> Dict[str, Any]:
        return {
            "type": "plot",
            "props": {
                "data": self.data,
                "title": self.title
            }
        }
