"""
Text Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class Text(Component):
    """
    Server-side logic for text component
    """
    
    def __init__(self, text: str = "", element_type: str = "span", 
                 size: str = "medium", weight: str = "normal", 
                 color: str = "default", italic: bool = False, 
                 underline: bool = False, strikethrough: bool = False, 
                 **kwargs):
        """
        Initialize text component
        
        Args:
            text: Text content
            element_type: HTML element type (span, p, h1, h2, h3, h4, h5, h6, div)
            size: Text size (small, medium, large, extra-large)
            weight: Font weight (light, normal, bold, extra-bold)
            color: Text color (default, primary, secondary, success, warning, danger, info)
            italic: Whether text is italic
            underline: Whether text is underlined
            strikethrough: Whether text has strikethrough
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.text = text
        self.element_type = element_type
        self.size = size
        self.weight = weight
        self.color = color
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
    
    def validate(self) -> bool:
        """
        Validate text configuration
        
        Returns:
            bool: True if validation passes
        """
        # Validate element type
        valid_elements = ["span", "p", "h1", "h2", "h3", "h4", "h5", "h6", "div"]
        if self.element_type not in valid_elements:
            return False
            
        # Validate size
        valid_sizes = ["small", "medium", "large", "extra-large"]
        if self.size not in valid_sizes:
            return False
            
        # Validate weight
        valid_weights = ["light", "normal", "bold", "extra-bold"]
        if self.weight not in valid_weights:
            return False
            
        # Validate color
        valid_colors = ["default", "primary", "secondary", "success", "warning", "danger", "info"]
        if self.color not in valid_colors:
            return False
            
        return True
    
    def set_text(self, text: str) -> Dict[str, Any]:
        """
        Set text content
        
        Args:
            text: New text content
            
        Returns:
            Dict containing response data
        """
        old_text = self.text
        self.text = text
        
        return {
            "success": True,
            "text": self.text,
            "previous_text": old_text
        }
    
    def set_style(self, size: str = None, weight: str = None, 
                  color: str = None, italic: bool = None, 
                  underline: bool = None, strikethrough: bool = None) -> Dict[str, Any]:
        """
        Set text style properties
        
        Args:
            size: Text size
            weight: Font weight
            color: Text color
            italic: Italic state
            underline: Underline state
            strikethrough: Strikethrough state
            
        Returns:
            Dict containing response data
        """
        changes = {}
        
        if size is not None:
            valid_sizes = ["small", "medium", "large", "extra-large"]
            if size not in valid_sizes:
                return {
                    "success": False,
                    "message": f"Invalid size. Valid sizes: {valid_sizes}"
                }
            changes["size"] = {"old": self.size, "new": size}
            self.size = size
            
        if weight is not None:
            valid_weights = ["light", "normal", "bold", "extra-bold"]
            if weight not in valid_weights:
                return {
                    "success": False,
                    "message": f"Invalid weight. Valid weights: {valid_weights}"
                }
            changes["weight"] = {"old": self.weight, "new": weight}
            self.weight = weight
            
        if color is not None:
            valid_colors = ["default", "primary", "secondary", "success", "warning", "danger", "info"]
            if color not in valid_colors:
                return {
                    "success": False,
                    "message": f"Invalid color. Valid colors: {valid_colors}"
                }
            changes["color"] = {"old": self.color, "new": color}
            self.color = color
            
        if italic is not None:
            changes["italic"] = {"old": self.italic, "new": italic}
            self.italic = italic
            
        if underline is not None:
            changes["underline"] = {"old": self.underline, "new": underline}
            self.underline = underline
            
        if strikethrough is not None:
            changes["strikethrough"] = {"old": self.strikethrough, "new": strikethrough}
            self.strikethrough = strikethrough
        
        return {
            "success": True,
            "changes": changes
        }
    
    def get_computed_style(self) -> Dict[str, Any]:
        """
        Get computed text style properties
        
        Returns:
            Dict containing computed style properties
        """
        return {
            "size": self.size,
            "weight": self.weight,
            "color": self.color,
            "italic": self.italic,
            "underline": self.underline,
            "strikethrough": self.strikethrough
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "content": self.text,
            "element": self.element_type,
            "size": self.size,
            "weight": self.weight,
            "color": self.color,
            "italic": self.italic,
            "underline": self.underline,
            "strikethrough": self.strikethrough,
            **self.get_base_props()
        }
            
        return {
            "type": "text",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Text':
        """
        Create text component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Text instance
        """
        return Text(
            text=data.get('text', ''),
            element_type=data.get('element', 'span'),
            size=data.get('size', 'medium'),
            weight=data.get('weight', 'normal'),
            color=data.get('color', 'default'),
            italic=data.get('italic', False),
            underline=data.get('underline', False),
            strikethrough=data.get('strikethrough', False)
        )

def create_text(text: str = "", element_type: str = "span", 
                size: str = "medium", weight: str = "normal", 
                color: str = "default", italic: bool = False, 
                underline: bool = False, strikethrough: bool = False, 
                **kwargs) -> Dict[str, Any]:
    """Create a text component"""
    component = Text(text, element_type, size, weight, color, italic, underline, strikethrough, **kwargs)
    return component.to_dict()