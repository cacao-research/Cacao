"""
Range Sliders Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class RangeSliders(Component):
    """
    Server-side logic for range sliders component
    """
    
    def __init__(self, min_val: float = 0, max_val: float = 100, step: float = 1,
                 lower_value: float = None, upper_value: float = None, 
                 onChange: Dict[str, Any] = None, **kwargs):
        """
        Initialize range sliders component
        
        Args:
            min_val: Minimum value of the range
            max_val: Maximum value of the range
            step: Step increment
            lower_value: Current lower bound value
            upper_value: Current upper bound value
            onChange: Change handler configuration
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.lower_value = lower_value if lower_value is not None else min_val
        self.upper_value = upper_value if upper_value is not None else max_val
        self.onChange = onChange
    
    def validate(self) -> bool:
        """
        Validate range slider values
        
        Returns:
            bool: True if validation passes
        """
        # Check if values are within bounds
        if (self.lower_value < self.min_val or self.lower_value > self.max_val or
            self.upper_value < self.min_val or self.upper_value > self.max_val):
            return False
            
        # Check if lower value doesn't exceed upper value
        if self.lower_value > self.upper_value:
            return False
            
        # Check if values align with step increment
        if self.step > 0:
            lower_steps = (self.lower_value - self.min_val) / self.step
            upper_steps = (self.upper_value - self.min_val) / self.step
            return (abs(lower_steps - round(lower_steps)) < 1e-10 and 
                    abs(upper_steps - round(upper_steps)) < 1e-10)
            
        return True
    
    def on_change(self, lower_value: float = None, upper_value: float = None) -> Dict[str, Any]:
        """
        Handle range slider value change
        
        Args:
            lower_value: New lower bound value
            upper_value: New upper bound value
            
        Returns:
            Dict containing response data
        """
        old_lower = self.lower_value
        old_upper = self.upper_value
        
        # Update values if provided
        if lower_value is not None:
            self.lower_value = lower_value
        if upper_value is not None:
            self.upper_value = upper_value
            
        # Ensure lower doesn't exceed upper
        if self.lower_value > self.upper_value:
            # Adjust the non-active slider
            if lower_value is not None:
                self.upper_value = self.lower_value
            else:
                self.lower_value = self.upper_value
        
        is_valid = self.validate()
        
        # Calculate percentages
        range_span = self.max_val - self.min_val
        lower_percentage = ((self.lower_value - self.min_val) / range_span) * 100 if range_span != 0 else 0
        upper_percentage = ((self.upper_value - self.min_val) / range_span) * 100 if range_span != 0 else 0
        
        return {
            "success": True,
            "lower_value": self.lower_value,
            "upper_value": self.upper_value,
            "previous_lower": old_lower,
            "previous_upper": old_upper,
            "valid": is_valid,
            "lower_percentage": lower_percentage,
            "upper_percentage": upper_percentage,
            "range_span": self.upper_value - self.lower_value,
            "min": self.min_val,
            "max": self.max_val
        }
    
    def set_lower_value(self, value: float) -> Dict[str, Any]:
        """
        Set lower bound value
        
        Args:
            value: New lower bound value
            
        Returns:
            Dict containing response data
        """
        return self.on_change(lower_value=value)
    
    def set_upper_value(self, value: float) -> Dict[str, Any]:
        """
        Set upper bound value
        
        Args:
            value: New upper bound value
            
        Returns:
            Dict containing response data
        """
        return self.on_change(upper_value=value)
    
    def set_range(self, lower: float, upper: float) -> Dict[str, Any]:
        """
        Set both lower and upper values
        
        Args:
            lower: New lower bound value
            upper: New upper bound value
            
        Returns:
            Dict containing response data
        """
        return self.on_change(lower_value=lower, upper_value=upper)
    
    def expand_range(self, amount: float) -> Dict[str, Any]:
        """
        Expand the range by the specified amount on both sides
        
        Args:
            amount: Amount to expand the range
            
        Returns:
            Dict containing response data
        """
        new_lower = max(self.lower_value - amount, self.min_val)
        new_upper = min(self.upper_value + amount, self.max_val)
        return self.on_change(lower_value=new_lower, upper_value=new_upper)
    
    def contract_range(self, amount: float) -> Dict[str, Any]:
        """
        Contract the range by the specified amount on both sides
        
        Args:
            amount: Amount to contract the range
            
        Returns:
            Dict containing response data
        """
        new_lower = min(self.lower_value + amount, self.upper_value)
        new_upper = max(self.upper_value - amount, self.lower_value)
        return self.on_change(lower_value=new_lower, upper_value=new_upper)
    
    def reset_to_bounds(self) -> Dict[str, Any]:
        """
        Reset range to full bounds (min to max)
        
        Returns:
            Dict containing response data
        """
        return self.on_change(lower_value=self.min_val, upper_value=self.max_val)
    
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
            "lowerValue": self.lower_value,
            "upperValue": self.upper_value,
            **self.get_base_props()
        }
        
        if self.onChange:
            props["onChange"] = self.onChange
            
        return {
            "type": "range-sliders",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'RangeSliders':
        """
        Create range sliders component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            RangeSliders instance
        """
        return RangeSliders(
            min_val=data.get('min', 0),
            max_val=data.get('max', 100),
            step=data.get('step', 1),
            lower_value=data.get('lower_value'),
            upper_value=data.get('upper_value'),
            onChange=data.get('onChange')
        )

def create_range_sliders(min_val: float = 0, max_val: float = 100, step: float = 1,
                        lower_value: float = None, upper_value: float = None, 
                        onChange: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
    """Create a range sliders component"""
    component = RangeSliders(min_val, max_val, step, lower_value, upper_value, onChange, **kwargs)
    return component.to_dict()