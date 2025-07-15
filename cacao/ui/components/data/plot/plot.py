"""
Plot component for displaying charts and graphs.
"""

from typing import Any, Dict
from ...base import Component


class Plot(Component):
    """
    A plot component for displaying charts and graphs.
    """
    def __init__(self, data, title = "") -> None:
        self.data = data
        self.title = title

    def render(self) -> Dict[str, Any]:
        return {
            "type": "plot",
            "props": {
                "data": self.data,
                "title": self.title
            }
        }