"""
Layout module for UI components in the Cacao framework.
Provides layout components like Grid and Column for organizing UI elements.
"""

from typing import List, Dict, Any
from .base import Component

class Grid(Component):
    """
    A grid layout component to arrange child components in a grid.
    """
    def __init__(self, children: List[Component], columns: int = 3) -> None:
        self.children = children
        self.columns = columns

    def render(self) -> Dict[str, Any]:
        return {
            "type": "grid",
            "props": {
                "columns": self.columns,
                "children": [child.render() for child in self.children]
            }
        }

class Column(Component):
    """
    A column layout component to arrange child components vertically.
    """
    def __init__(self, children: List[Component]) -> None:
        self.children = children

    def render(self) -> Dict[str, Any]:
        return {
            "type": "column",
            "props": {
                "children": [child.render() for child in self.children]
            }
        }
