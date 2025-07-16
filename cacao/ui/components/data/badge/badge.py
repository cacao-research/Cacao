"""
Badge component for adding small indicators to elements.
"""

from typing import Any, Dict
from ...base import Component


class Badge(Component):
    """
    Adds a small indicator (e.g., a number or dot) to an element.
    """
    def __init__(
        self,
        count = None,
        children = None,
        dot = False,
        show_zero = False,
        **kwargs
    ) -> None:
        self.count = count
        self.children = children
        self.dot = dot
        self.show_zero = show_zero
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "badge",
            "props": {
                "count": self.count,
                "children": self.children.render() if self.children else None,
                "dot": self.dot,
                "showZero": self.show_zero,
                **self.extra_props
            }
        }