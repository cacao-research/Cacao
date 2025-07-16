"""
Popover component for displaying more complex content than tooltips.
"""

from typing import Any, Dict
from ...base import Component


class Popover(Component):
    """
    Similar to tooltip but can contain more complex content.
    """
    def __init__(
        self,
        content,
        children,
        title = "",
        placement = "top",
        trigger = "click",
        **kwargs
    ) -> None:
        self.content = content
        self.children = children
        self.title = title
        self.placement = placement
        self.trigger = trigger
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "popover",
            "props": {
                "content": self.content,
                "children": self.children.render(),
                "title": self.title,
                "placement": self.placement,
                "trigger": self.trigger,
                **self.extra_props
            }
        }