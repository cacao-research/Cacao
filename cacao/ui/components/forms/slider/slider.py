"""
Slider Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class Slider(Component):
    """
    Server-side logic for slider component
    """
    
    def __init__(self, min_val: float = 0, max_val: float = 100, step: float = 1,
                 value: float = 0, onChange: Dict[str, Any] = None, **kwargs):
        """
        Initialize slider component
        
        Args:
            min_val: Minimum value
            max_val: Maximum value
            step: Step increment
            value: Current value
            onChange: Change handler configuration
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.value = value
        self.onChange = onChange
    
    def validate(self) -> bool:
        """
        Validate slider value
        
        Returns:
            bool: True if validation passes
        """
        # Check if value is within bounds
        if self.value < self.min_val or self.value > self.max_val:
            return False
            
        # Check if value aligns with step increment
        if self.step > 0:
            steps_from_min = (self.value - self.min_val) / self.step
            return abs(steps_from_min - round(steps_from_min)) < 1e-10
            
        return True
    
    def on_change(self, value: float) -> Dict[str, Any]:
        """
        Handle slider value change
        
        Args:
            value: New slider value
            
        Returns:
            Dict containing response data
        """
        old_value = self.value
        self.value = value
        is_valid = self.validate()
        
        # Calculate percentage
        percentage = ((value - self.min_val) / (self.max_val - self.min_val)) * 100 if self.max_val != self.min_val else 0
        
        return {
            "success": True,
            "value": self.value,
            "previousValue": old_value,
            "valid": is_valid,
            "percentage": percentage,
            "min": self.min_val,
            "max": self.max_val
        }
    
    def increment(self) -> Dict[str, Any]:
        """
        Increment slider value by step
        
        Returns:
            Dict containing response data
        """
        new_value = min(self.value + self.step, self.max_val)
        return self.on_change(new_value)
    
    def decrement(self) -> Dict[str, Any]:
        """
        Decrement slider value by step
        
        Returns:
            Dict containing response data
        """
        new_value = max(self.value - self.step, self.min_val)
        return self.on_change(new_value)
    
    def set_to_min(self) -> Dict[str, Any]:
        """
        Set slider to minimum value
        
        Returns:
            Dict containing response data
        """
        return self.on_change(self.min_val)
    
    def set_to_max(self) -> Dict[str, Any]:
        """
        Set slider to maximum value
        
        Returns:
            Dict containing response data
        """
        return self.on_change(self.max_val)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "min": self.min_val,
            "max": self.max_val,
            "step": self.step,
            "value": self.value,
            **self.get_base_props()
        }
        
        if self.onChange:
            props["onChange"] = self.onChange
            
        return {
            "type": "slider",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Slider':
        """
        Create slider component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Slider instance
        """
        return Slider(
            min_val=data.get('min', 0),
            max_val=data.get('max', 100),
            step=data.get('step', 1),
            value=data.get('value', 0),
            onChange=data.get('onChange')
        )

def create_slider(min_val: float = 0, max_val: float = 100, step: float = 1,
                 value: float = 0, onChange: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
    """Create a slider component"""
    component = Slider(min_val, max_val, step, value, onChange, **kwargs)
    return component.to_dict()