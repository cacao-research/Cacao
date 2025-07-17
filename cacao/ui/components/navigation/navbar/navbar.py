"""
Navbar Component Python Integration
"""

from typing import Dict, Any, Optional, List
from ...base import Component

class Navbar(Component):
    """
    Server-side logic for navbar component
    """
    
    def __init__(self, title: str = None, logo: str = None, items: List[Dict[str, Any]] = None, 
                 position: str = "top", theme: str = "light", sticky: bool = False, 
                 collapsed: bool = False, **kwargs):
        """
        Initialize navbar component
        
        Args:
            title: Navbar title text
            logo: Logo image URL or identifier
            items: List of navigation items
            position: Position of navbar (top, bottom, fixed)
            theme: Navbar theme (light, dark)
            sticky: Whether navbar is sticky
            collapsed: Whether navbar is collapsed (mobile)
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.title = title
        self.logo = logo
        self.items = items or []
        self.position = position
        self.theme = theme
        self.sticky = sticky
        self.collapsed = collapsed
    
    def validate(self) -> bool:
        """
        Validate navbar configuration
        
        Returns:
            bool: True if validation passes
        """
        # Validate position
        valid_positions = ["top", "bottom", "fixed"]
        if self.position not in valid_positions:
            return False
            
        # Validate theme
        valid_themes = ["light", "dark"]
        if self.theme not in valid_themes:
            return False
            
        return True
    
    def set_title(self, title: str) -> Dict[str, Any]:
        """
        Set navbar title
        
        Args:
            title: New title text
            
        Returns:
            Dict containing response data
        """
        old_title = self.title
        self.title = title
        
        return {
            "success": True,
            "title": self.title,
            "previous_title": old_title
        }
    
    def set_logo(self, logo: str) -> Dict[str, Any]:
        """
        Set navbar logo
        
        Args:
            logo: New logo URL or identifier
            
        Returns:
            Dict containing response data
        """
        old_logo = self.logo
        self.logo = logo
        
        return {
            "success": True,
            "logo": self.logo,
            "previous_logo": old_logo
        }
    
    def add_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add item to navbar
        
        Args:
            item: Navigation item to add
            
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
        Remove item from navbar by key
        
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
    
    def set_position(self, position: str) -> Dict[str, Any]:
        """
        Set navbar position
        
        Args:
            position: New position
            
        Returns:
            Dict containing response data
        """
        valid_positions = ["top", "bottom", "fixed"]
        if position not in valid_positions:
            return {
                "success": False,
                "message": f"Invalid position. Valid positions: {valid_positions}"
            }
        
        old_position = self.position
        self.position = position
        
        return {
            "success": True,
            "position": self.position,
            "previous_position": old_position
        }
    
    def set_theme(self, theme: str) -> Dict[str, Any]:
        """
        Set navbar theme
        
        Args:
            theme: New theme
            
        Returns:
            Dict containing response data
        """
        valid_themes = ["light", "dark"]
        if theme not in valid_themes:
            return {
                "success": False,
                "message": f"Invalid theme. Valid themes: {valid_themes}"
            }
        
        old_theme = self.theme
        self.theme = theme
        
        return {
            "success": True,
            "theme": self.theme,
            "previous_theme": old_theme
        }
    
    def set_sticky(self, sticky: bool) -> Dict[str, Any]:
        """
        Set navbar sticky state
        
        Args:
            sticky: New sticky state
            
        Returns:
            Dict containing response data
        """
        old_sticky = self.sticky
        self.sticky = sticky
        
        return {
            "success": True,
            "sticky": self.sticky,
            "previous_sticky": old_sticky
        }
    
    def toggle_collapse(self) -> Dict[str, Any]:
        """
        Toggle navbar collapse state (mobile)
        
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
            "position": self.position,
            "theme": self.theme,
            "sticky": self.sticky,
            "collapsed": self.collapsed,
            **self.get_base_props()
        }
        
        if self.title:
            props["title"] = self.title
            
        if self.logo:
            props["logo"] = self.logo
            
        return {
            "type": "navbar",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Navbar':
        """
        Create navbar component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Navbar instance
        """
        return Navbar(
            title=data.get('title'),
            logo=data.get('logo'),
            items=data.get('items', []),
            position=data.get('position', 'top'),
            theme=data.get('theme', 'light'),
            sticky=data.get('sticky', False),
            collapsed=data.get('collapsed', False)
        )

def create_navbar(title: str = None, logo: str = None, items: List[Dict[str, Any]] = None, 
                  position: str = "top", theme: str = "light", sticky: bool = False, 
                  collapsed: bool = False, **kwargs) -> Dict[str, Any]:
    """Create a navbar component"""
    component = Navbar(title, logo, items, position, theme, sticky, collapsed, **kwargs)
    return component.to_dict()