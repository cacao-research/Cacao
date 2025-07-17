"""
Menu Component Python Integration
"""

from typing import Dict, Any, Optional, List
from ...base import Component

class Menu(Component):
    """
    Server-side logic for menu component
    """
    
    def __init__(self, items: List[Dict[str, Any]] = None, mode: str = "horizontal", 
                 theme: str = "light", default_selected: str = None, 
                 collapsed: bool = False, **kwargs):
        """
        Initialize menu component
        
        Args:
            items: List of menu items
            mode: Menu mode (horizontal, vertical, inline)
            theme: Menu theme (light, dark)
            default_selected: Default selected item key
            collapsed: Whether menu is collapsed
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.items = items or []
        self.mode = mode
        self.theme = theme
        self.default_selected = default_selected
        self.collapsed = collapsed
        self.selected_key = default_selected
    
    def validate(self) -> bool:
        """
        Validate menu configuration
        
        Returns:
            bool: True if validation passes
        """
        # Validate mode
        valid_modes = ["horizontal", "vertical", "inline"]
        if self.mode not in valid_modes:
            return False
            
        # Validate theme
        valid_themes = ["light", "dark"]
        if self.theme not in valid_themes:
            return False
            
        return True
    
    def add_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add item to menu
        
        Args:
            item: Menu item to add
            
        Returns:
            Dict containing response data
        """
        required_keys = ["key", "label"]
        if not all(key in item for key in required_keys):
            return {
                "success": False,
                "message": f"Item must contain keys: {required_keys}"
            }
        
        self.items.append(item)
        
        return {
            "success": True,
            "items_count": len(self.items),
            "added_item": item
        }
    
    def remove_item(self, key: str) -> Dict[str, Any]:
        """
        Remove item from menu by key
        
        Args:
            key: Key of item to remove
            
        Returns:
            Dict containing response data
        """
        original_count = len(self.items)
        self.items = [item for item in self.items if item.get("key") != key]
        
        return {
            "success": True,
            "removed": original_count != len(self.items),
            "items_count": len(self.items)
        }
    
    def select_item(self, key: str) -> Dict[str, Any]:
        """
        Select menu item by key
        
        Args:
            key: Key of item to select
            
        Returns:
            Dict containing response data
        """
        # Check if item exists
        item_exists = any(item.get("key") == key for item in self.items)
        if not item_exists:
            return {
                "success": False,
                "message": f"Item with key '{key}' not found"
            }
        
        old_selected = self.selected_key
        self.selected_key = key
        
        return {
            "success": True,
            "selected_key": self.selected_key,
            "previous_selected": old_selected
        }
    
    def set_mode(self, mode: str) -> Dict[str, Any]:
        """
        Set menu mode
        
        Args:
            mode: New menu mode
            
        Returns:
            Dict containing response data
        """
        valid_modes = ["horizontal", "vertical", "inline"]
        if mode not in valid_modes:
            return {
                "success": False,
                "message": f"Invalid mode. Valid modes: {valid_modes}"
            }
        
        old_mode = self.mode
        self.mode = mode
        
        return {
            "success": True,
            "mode": self.mode,
            "previous_mode": old_mode
        }
    
    def toggle_collapse(self) -> Dict[str, Any]:
        """
        Toggle menu collapse state
        
        Returns:
            Dict containing response data
        """
        old_collapsed = self.collapsed
        self.collapsed = not self.collapsed
        
        return {
            "success": True,
            "collapsed": self.collapsed,
            "previous_collapsed": old_collapsed
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "items": self.items,
            "mode": self.mode,
            "theme": self.theme,
            "selectedKey": self.selected_key,
            "collapsed": self.collapsed,
            **self.get_base_props()
        }
            
        return {
            "type": "menu",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Menu':
        """
        Create menu component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Menu instance
        """
        return Menu(
            items=data.get('items', []),
            mode=data.get('mode', 'horizontal'),
            theme=data.get('theme', 'light'),
            default_selected=data.get('default_selected'),
            collapsed=data.get('collapsed', False)
        )

def create_menu(items: List[Dict[str, Any]] = None, mode: str = "horizontal", 
                theme: str = "light", default_selected: str = None, 
                collapsed: bool = False, **kwargs) -> Dict[str, Any]:
    """Create a menu component"""
    component = Menu(items, mode, theme, default_selected, collapsed, **kwargs)
    return component.to_dict()