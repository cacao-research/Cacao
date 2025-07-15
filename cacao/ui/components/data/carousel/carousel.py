"""
Carousel component for cycling through a set of images or content.
"""

from typing import Any, Dict
from ...base import Component


class Carousel(Component):
    """
    Cycles through a set of images or content.
    """
    def __init__(
        self,
        items,
        auto_play = False,
        dots = True,
        effect = "scrollx",
        **kwargs
    ) -> None:
        self.items = items
        self.auto_play = auto_play
        self.dots = dots
        self.effect = effect
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "carousel",
            "props": {
                "items": self.items,
                "autoPlay": self.auto_play,
                "dots": self.dots,
                "effect": self.effect,
                **self.extra_props
            }
        }