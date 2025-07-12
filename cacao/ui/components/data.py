"""
Data module for UI components in the Cacao framework.
Provides components for displaying data such as tables and plots.
"""

from typing import Any, Dict
from .base import Component

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

class Tooltip(Component):
    """
    A small popup with additional information that appears on hover.
    """
    def __init__(
        self,
        content,
        children,
        placement = "top",
        **kwargs
    ) -> None:
        self.content = content
        self.children = children
        self.placement = placement
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "tooltip",
            "props": {
                "content": self.content,
                "children": self.children.render(),
                "placement": self.placement,
                **self.extra_props
            }
        }

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

class Card(Component):
    """
    A container for displaying related information in a concise format.
    """
    def __init__(
        self,
        children,
        title = "",
        bordered = True,
        extra = None,
        **kwargs
    ) -> None:
        self.children = children
        self.title = title
        self.bordered = bordered
        self.extra = extra
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "card",
            "props": {
                "children": self.children,
                "title": self.title,
                "bordered": self.bordered,
                "extra": self.extra,
                **self.extra_props
            }
        }

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

class Badge(Component):
    """
    Adds a small indicator (e.g., a number or dot) to an element.
    """
    def __init__(
        self,
        count = None,
        children = None,
        dot = False,
        show_zero = False,
        **kwargs
    ) -> None:
        self.count = count
        self.children = children
        self.dot = dot
        self.show_zero = show_zero
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "badge",
            "props": {
                "count": self.count,
                "children": self.children.render() if self.children else None,
                "dot": self.dot,
                "showZero": self.show_zero,
                **self.extra_props
            }
        }

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
