"""
List component for presenting data in a vertical sequence.
"""

from typing import Any, Dict
from ...base import Component


class List(Component):
    """
    Presents data in a vertical sequence (simple, bordered, with actions).
    """
    def __init__(
        self,
        items,
        bordered = False,
        size = "default",
        **kwargs
    ) -> None:
        self.items = items
        self.bordered = bordered
        self.size = size
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "list",
            "props": {
                "items": self.items,
                "bordered": self.bordered,
                "size": self.size,
                **self.extra_props
            }
        }