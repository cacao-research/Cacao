"""
Navigation module for UI components in the Cacao framework.
Provides implementations for navigation elements such as menus, breadcrumbs, tabs, etc.
"""

from typing import List, Dict, Any, Optional, Callable
from .base import Component

class Menu(Component):
    """
    Hierarchical navigation with submenus and different display modes.
    """
    def __init__(
        self,
        items: List[Dict[str, Any]],
        mode: str = "vertical",
        selected_keys: List[str] = None,
        on_select: Optional[Callable[[str], None]] = None,
        **kwargs
    ) -> None:
        self.items = items
        self.mode = mode
        self.selected_keys = selected_keys or []
        self.on_select = on_select
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "menu",
            "props": {
                "items": self.items,
                "mode": self.mode,
                "selectedKeys": self.selected_keys,
                **self.extra_props
            }
        }

class Breadcrumb(Component):
    """
    Shows the current page's location within the site hierarchy.
    """
    def __init__(
        self,
        items: List[Dict[str, Any]],
        separator: str = "/",
        **kwargs
    ) -> None:
        self.items = items
        self.separator = separator
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "breadcrumb",
            "props": {
                "items": self.items,
                "separator": self.separator,
                **self.extra_props
            }
        }

class Tabs(Component):
    """
    Organizes content into different sections accessible by clicking tabs.
    """
    def __init__(
        self,
        items: List[Dict[str, Any]],
        active_key: str = None,
        on_change: Optional[Callable[[str], None]] = None,
        **kwargs
    ) -> None:
        self.items = items
        self.active_key = active_key
        self.on_change = on_change
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "tabs",
            "props": {
                "items": self.items,
                "activeKey": self.active_key,
                **self.extra_props
            }
        }

class Dropdown(Component):
    """
    A toggleable menu that appears upon clicking an element.
    """
    def __init__(
        self,
        items: List[Dict[str, Any]],
        trigger: str = "click",
        placement: str = "bottomLeft",
        visible: bool = False,
        **kwargs
    ) -> None:
        self.items = items
        self.trigger = trigger
        self.placement = placement
        self.visible = visible
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "dropdown",
            "props": {
                "items": self.items,
                "trigger": self.trigger,
                "placement": self.placement,
                "visible": self.visible,
                **self.extra_props
            }
        }

class Pagination(Component):
    """
    Divides content into multiple pages for easier navigation.
    """
    def __init__(
        self,
        total: int,
        current: int = 1,
        page_size: int = 10,
        on_change: Optional[Callable[[int], None]] = None,
        **kwargs
    ) -> None:
        self.total = total
        self.current = current
        self.page_size = page_size
        self.on_change = on_change
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "pagination",
            "props": {
                "total": self.total,
                "current": self.current,
                "pageSize": self.page_size,
                **self.extra_props
            }
        }

class Steps(Component):
    """
    Guides users through a multi-step process.
    """
    def __init__(
        self,
        items: List[Dict[str, Any]],
        current: int = 0,
        direction: str = "horizontal",
        on_change: Optional[Callable[[int], None]] = None,
        **kwargs
    ) -> None:
        self.items = items
        self.current = current
        self.direction = direction
        self.on_change = on_change
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "steps",
            "props": {
                "items": self.items,
                "current": self.current,
                "direction": self.direction,
                **self.extra_props
            }
        }