"""
Switch Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class Switch(Component):
    """
    Server-side logic for switch component
    """
    
    def __init__(self, checked: bool = False, disabled: bool = False, **kwargs):
        """
        Initialize switch component
        
        Args:
            checked: Whether switch is initially checked
            disabled: Whether switch is disabled
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.checked = checked
        self.disabled = disabled
    
    def validate(self) -> bool:
        """
        Validate switch state
        
        Returns:
            bool: True if validation passes
        """
        # Switches don't typically need validation
        return True
    
    def on_change(self, checked: bool) -> Dict[str, Any]:
        """
        Handle switch state change
        
        Args:
            checked: New checked state
            
        Returns:
            Dict containing response data
        """
        self.checked = checked
        
        # Add any business logic here
        # For example, enabling/disabling features, updating settings, etc.
        
        return {
            "success": True,
            "checked": self.checked,
            "message": f"Switch {'enabled' if checked else 'disabled'}"
        }
    
    def toggle(self) -> Dict[str, Any]:
        """
        Toggle switch state
        
        Returns:
            Dict containing response data
        """
        return self.on_change(not self.checked)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        return {
            "type": "switch",
            "props": {
                "checked": self.checked,
                "disabled": self.disabled,
                **self.get_base_props()
            }
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Switch':
        """
        Create switch component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Switch instance
        """
        return Switch(
            checked=data.get('checked', False),
            disabled=data.get('disabled', False)
        )

def create_switch(checked: bool = False, disabled: bool = False, **kwargs) -> Dict[str, Any]:
    """Create a switch component"""
    component = Switch(checked, disabled, **kwargs)
    return component.to_dict()