"""
Input Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class Input(Component):
    """
    Server-side logic for input component
    """
    
    def __init__(self, input_type: str = "text", value: str = "", placeholder: str = None, 
                 disabled: bool = False, required: bool = False, **kwargs):
        """
        Initialize input component
        
        Args:
            input_type: Type of input (text, email, password, etc.)
            value: Initial value
            placeholder: Placeholder text
            disabled: Whether input is disabled
            required: Whether input is required
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.input_type = input_type
        self.value = value
        self.placeholder = placeholder
        self.disabled = disabled
        self.required = required
    
    def validate(self) -> bool:
        """
        Validate input value
        
        Returns:
            bool: True if validation passes
        """
        if self.required and not self.value:
            return False
            
        # Add specific validation based on input type
        if self.input_type == "email":
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(email_pattern, self.value) is not None
            
        return True
    
    def on_change(self, value: str) -> Dict[str, Any]:
        """
        Handle input value change
        
        Args:
            value: New input value
            
        Returns:
            Dict containing response data
        """
        self.value = value
        is_valid = self.validate()
        
        return {
            "success": True,
            "value": self.value,
            "valid": is_valid
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "inputType": self.input_type,
            "value": self.value,
            "disabled": self.disabled,
            "required": self.required,
            **self.get_base_props()
        }
        
        if self.placeholder:
            props["placeholder"] = self.placeholder
            
        return {
            "type": "input",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Input':
        """
        Create input component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Input instance
        """
        return Input(
            input_type=data.get('inputType', 'text'),
            value=data.get('value', ''),
            placeholder=data.get('placeholder'),
            disabled=data.get('disabled', False),
            required=data.get('required', False)
        )

def create_input(input_type: str = "text", value: str = "", placeholder: str = None,
                disabled: bool = False, required: bool = False, **kwargs) -> Dict[str, Any]:
    """Create an input component"""
    component = Input(input_type, value, placeholder, disabled, required, **kwargs)
    return component.to_dict()