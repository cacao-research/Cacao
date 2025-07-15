"""
Timeline component for displaying a chronological sequence of events.
"""

from typing import Any, Dict
from ...base import Component


class Timeline(Component):
    """
    Displays a chronological sequence of events.
    """
    def __init__(
        self,
        items,
        mode = "left",
        reverse = False,
        **kwargs
    ) -> None:
        self.items = items
        self.mode = mode
        self.reverse = reverse
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "timeline",
            "props": {
                "items": self.items,
                "mode": self.mode,
                "reverse": self.reverse,
                **self.extra_props
            }
        }