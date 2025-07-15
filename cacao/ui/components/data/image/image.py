"""
Image component for displaying images with optional captions and previews.
"""

from typing import Any, Dict
from ...base import Component


class Image(Component):
    """
    Displays images with optional captions and previews.
    """
    def __init__(
        self,
        src,
        alt = "",
        width = None,
        height = None,
        preview = True,
        **kwargs
    ) -> None:
        self.src = src
        self.alt = alt
        self.width = width
        self.height = height
        self.preview = preview
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "image",
            "props": {
                "src": self.src,
                "alt": self.alt,
                "width": self.width,
                "height": self.height,
                "preview": self.preview,
                **self.extra_props
            }
        }