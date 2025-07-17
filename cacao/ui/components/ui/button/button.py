"""
Button Component Python Integration
"""

from typing import Dict, Any, Optional, Callable
from ...base import Component

class Button(Component):
    """
    Server-side logic for button component
    """
    
    def __init__(self, button_type: str = "button", variant: str = "primary", 
                 size: str = "medium", disabled: bool = False, 
                 loading: bool = False, onClick: Dict[str, Any] = None, **kwargs):
        """
        Initialize button component
        
        Args:
            button_type: Type of button (button, submit, reset)
            variant: Button variant (primary, secondary, danger, success, warning)
            size: Button size (small, medium, large)
            disabled: Whether button is disabled
            loading: Whether button is in loading state
            onClick: Click handler configuration
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.button_type = button_type
        self.variant = variant
        self.size = size
        self.disabled = disabled
        self.loading = loading
        self.onClick = onClick
    
    def validate(self) -> bool:
        """
        Validate button configuration
        
        Returns:
            bool: True if validation passes
        """
        # Validate button type
        valid_types = ["button", "submit", "reset"]
        if self.button_type not in valid_types:
            return False
            
        # Validate variant
        valid_variants = ["primary", "secondary", "danger", "success", "warning", "info"]
        if self.variant not in valid_variants:
            return False
            
        # Validate size
        valid_sizes = ["small", "medium", "large"]
        if self.size not in valid_sizes:
            return False
            
        return True
    
    def set_loading(self, loading: bool) -> Dict[str, Any]:
        """
        Set loading state
        
        Args:
            loading: New loading state
            
        Returns:
            Dict containing response data
        """
        old_loading = self.loading
        self.loading = loading
        
        return {
            "success": True,
            "loading": self.loading,
            "previous_loading": old_loading
        }
    
    def set_disabled(self, disabled: bool) -> Dict[str, Any]:
        """
        Set disabled state
        
        Args:
            disabled: New disabled state
            
        Returns:
            Dict containing response data
        """
        old_disabled = self.disabled
        self.disabled = disabled
        
        return {
            "success": True,
            "disabled": self.disabled,
            "previous_disabled": old_disabled
        }
    
    def on_click(self) -> Dict[str, Any]:
        """
        Handle button click
        
        Returns:
            Dict containing response data
        """
        if self.disabled or self.loading:
            return {
                "success": False,
                "message": "Button is disabled or loading"
            }
        
        return {
            "success": True,
            "clicked": True,
            "button_type": self.button_type,
            "variant": self.variant
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "type": self.button_type,
            "variant": self.variant,
            "size": self.size,
            "disabled": self.disabled,
            "loading": self.loading,
            **self.get_base_props()
        }
        
        if self.onClick:
            props["onClick"] = self.onClick
            
        return {
            "type": "button",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Button':
        """
        Create button component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Button instance
        """
        return Button(
            button_type=data.get('type', 'button'),
            variant=data.get('variant', 'primary'),
            size=data.get('size', 'medium'),
            disabled=data.get('disabled', False),
            loading=data.get('loading', False),
            onClick=data.get('onClick')
        )

def create_button(button_type: str = "button", variant: str = "primary", 
                  size: str = "medium", disabled: bool = False, 
                  loading: bool = False, onClick: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
    """Create a button component"""
    component = Button(button_type, variant, size, disabled, loading, onClick, **kwargs)
    return component.to_dict()