"""
Descriptions component for displaying key-value pairs of information.
"""

from typing import Any, Dict
from ...base import Component


class Descriptions(Component):
    """
    Displays key-value pairs of information.
    """
    def __init__(
        self,
        items,
        title = "",
        bordered = False,
        column = 3,
        **kwargs
    ) -> None:
        self.items = items
        self.title = title
        self.bordered = bordered
        self.column = column
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        print("[DEBUG] Descriptions.render - Title:", self.title)
        print("[DEBUG] Descriptions.render - Items:", self.items)
        print("[DEBUG] Descriptions.render - Column:", self.column)
        print("[DEBUG] Descriptions.render - Bordered:", self.bordered)
        
        rendered = {
            "type": "descriptions",
            "props": {
                "items": self.items,
                "title": self.title,
                "bordered": self.bordered,
                "column": self.column,
                **self.extra_props
            }
        }
        print("[DEBUG] Descriptions.render - Final output:", rendered)
        return rendered