"""
Avatar component for representing a user or entity with an image or icon.
"""

from typing import Any, Dict
from ...base import Component


class Avatar(Component):
    """
    Represents a user or entity with an image or icon.
    """
    def __init__(
        self,
        src = None,
        icon = None,
        shape = "circle",
        size = "default",
        **kwargs
    ) -> None:
        self.src = src
        self.icon = icon
        self.shape = shape
        self.size = size
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "avatar",
            "props": {
                "src": self.src,
                "icon": self.icon,
                "shape": self.shape,
                "size": self.size,
                **self.extra_props
            }
        }