"""
Checkbox Component Python Integration
Example of how to create Python logic for form components
"""

from typing import Dict, Any, Optional
from cacao.ui.components.base import Component

class Checkbox(Component):
    """
    Server-side logic for checkbox component
    """
    
    def __init__(self, checked: bool = False, label: str = "", disabled: bool = False, **kwargs):
        """
        Initialize checkbox component
        
        Args:
            checked: Whether checkbox is initially checked
            label: Label text for the checkbox
            disabled: Whether checkbox is disabled
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.checked = checked
        self.label = label
        self.disabled = disabled
    
    def validate(self) -> bool:
        """
        Validate checkbox state
        
        Returns:
            bool: True if validation passes
        """
        # Add any validation logic here
        return True
    
    def on_change(self, checked: bool) -> Dict[str, Any]:
        """
        Handle checkbox state change
        
        Args:
            checked: New checked state
            
        Returns:
            Dict containing response data
        """
        self.checked = checked
        
        # Add any business logic here
        # For example, updating related data, triggering events, etc.
        
        return {
            "success": True,
            "checked": self.checked,
            "message": f"Checkbox {'checked' if checked else 'unchecked'}"
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        return {
            "type": "checkbox",
            "props": {
                "checked": self.checked,
                "label": self.label,
                "disabled": self.disabled,
                "className": getattr(self, 'className', 'checkbox'),
                **self.get_base_props()
            }
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Checkbox':
        """
        Create checkbox component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Checkbox instance
        """
        return Checkbox(
            checked=data.get('checked', False),
            label=data.get('label', ''),
            disabled=data.get('disabled', False)
        )

# Example usage:
def create_checkbox_example():
    """Example of how to use the checkbox component"""
    checkbox = Checkbox(
        checked=False,
        label="Accept Terms and Conditions",
        disabled=False
    )
    
    # Render component
    return checkbox.to_dict()

def handle_checkbox_event(component_data: Dict[str, Any], event_data: Dict[str, Any]):
    """
    Example event handler for checkbox component
    
    Args:
        component_data: Current component state
        event_data: Event data from frontend
    """
    checkbox = Checkbox.from_form_data(component_data.get('props', {}))
    
    # Handle the change event
    new_checked = event_data.get('checked', False)
    result = checkbox.on_change(new_checked)
    
    return {
        "component": checkbox.to_dict(),
        "result": result
    }