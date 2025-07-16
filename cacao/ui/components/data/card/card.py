"""
Card component for displaying related information in a concise format.
"""

from typing import Any, Dict
from ...base import Component


class Card(Component):
    """
    A container for displaying related information in a concise format.
    """
    def __init__(
        self,
        children,
        title = "",
        bordered = True,
        extra = None,
        **kwargs
    ) -> None:
        self.children = children
        self.title = title
        self.bordered = bordered
        self.extra = extra
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "card",
            "props": {
                "children": self.children,
                "title": self.title,
                "bordered": self.bordered,
                "extra": self.extra,
                **self.extra_props
            }
        }