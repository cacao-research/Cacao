"""
Tag component for labeling content with keywords or categories.
"""

from typing import Any, Dict
from ...base import Component


class Tag(Component):
    """
    Labels content with keywords or categories.
    """
    def __init__(
        self,
        content,
        color = None,
        closable = False,
        **kwargs
    ) -> None:
        self.content = content
        self.color = color
        self.closable = closable
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "tag",
            "props": {
                "content": self.content,
                "color": self.color,
                "closable": self.closable,
                **self.extra_props
            }
        }