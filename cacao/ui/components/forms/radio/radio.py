"""
Radio Component Python Integration
"""

from typing import Dict, Any, Optional, List
from ...base import Component

class Radio(Component):
    """
    Server-side logic for radio component
    """
    
    def __init__(self, options: List[Dict[str, Any]], value: Any = None, name: str = None,
                 disabled: bool = False, **kwargs):
        """
        Initialize radio component
        
        Args:
            options: List of option dictionaries with 'value' and 'label' keys
            value: Selected value
            name: Radio group name
            disabled: Whether radio group is disabled
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.options = options
        self.value = value
        self.name = name
        self.disabled = disabled
    
    def validate(self) -> bool:
        """
        Validate selected value
        
        Returns:
            bool: True if validation passes
        """
        # Check if selected value exists in options
        if self.value is not None:
            valid_values = [opt.get('value') for opt in self.options]
            return self.value in valid_values
            
        return True
    
    def on_change(self, value: Any) -> Dict[str, Any]:
        """
        Handle radio value change
        
        Args:
            value: New selected value
            
        Returns:
            Dict containing response data
        """
        self.value = value
        is_valid = self.validate()
        
        # Find the selected option
        selected_option = None
        for option in self.options:
            if option.get('value') == value:
                selected_option = option
                break
        
        return {
            "success": True,
            "value": self.value,
            "selectedOption": selected_option,
            "valid": is_valid
        }
    
    def add_option(self, value: Any, label: str) -> None:
        """
        Add a new option to the radio group
        
        Args:
            value: Option value
            label: Option label
        """
        self.options.append({"value": value, "label": label})
    
    def remove_option(self, value: Any) -> bool:
        """
        Remove an option from the radio group
        
        Args:
            value: Option value to remove
            
        Returns:
            bool: True if option was removed
        """
        for i, option in enumerate(self.options):
            if option.get('value') == value:
                self.options.pop(i)
                # Clear selection if removed option was selected
                if self.value == value:
                    self.value = None
                return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "options": self.options,
            "disabled": self.disabled,
            **self.get_base_props()
        }
        
        if self.value is not None:
            props["value"] = self.value
        if self.name:
            props["name"] = self.name
            
        return {
            "type": "radio",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Radio':
        """
        Create radio component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Radio instance
        """
        return Radio(
            options=data.get('options', []),
            value=data.get('value'),
            name=data.get('name'),
            disabled=data.get('disabled', False)
        )

def create_radio(options: List[Dict[str, Any]], value: Any = None, name: str = None,
                disabled: bool = False, **kwargs) -> Dict[str, Any]:
    """Create a radio component"""
    component = Radio(options, value, name, disabled, **kwargs)
    return component.to_dict()