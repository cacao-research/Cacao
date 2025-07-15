"""
Collapse component for hiding and showing content sections.
"""

from typing import Any, Dict
from ...base import Component


class Collapse(Component):
    """
    Hides and shows content sections.
    """
    def __init__(
        self,
        panels,
        accordion = False,
        active_key = None,
        **kwargs
    ) -> None:
        self.panels = panels
        self.accordion = accordion
        self.active_key = active_key if active_key is not None else []
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "collapse",
            "props": {
                "panels": self.panels,
                "accordion": self.accordion,
                "activeKey": self.active_key,
                **self.extra_props
            }
        }