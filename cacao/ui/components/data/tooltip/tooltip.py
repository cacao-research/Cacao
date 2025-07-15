"""
Tooltip component for displaying additional information on hover.
"""

from typing import Any, Dict
from ...base import Component


class Tooltip(Component):
    """
    A small popup with additional information that appears on hover.
    """
    def __init__(
        self,
        content,
        children,
        placement = "top",
        **kwargs
    ) -> None:
        self.content = content
        self.children = children
        self.placement = placement
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "tooltip",
            "props": {
                "content": self.content,
                "children": self.children.render(),
                "placement": self.placement,
                **self.extra_props
            }
        }