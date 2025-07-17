"""
Rate Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class Rate(Component):
    """
    Server-side logic for rate component
    """
    
    def __init__(self, max_rating: int = 5, value: float = 0, allow_half: bool = True,
                 onChange: Dict[str, Any] = None, **kwargs):
        """
        Initialize rate component
        
        Args:
            max_rating: Maximum rating value
            value: Current rating value
            allow_half: Whether to allow half-star ratings
            onChange: Change handler configuration
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.max_rating = max_rating
        self.value = value
        self.allow_half = allow_half
        self.onChange = onChange
    
    def validate(self) -> bool:
        """
        Validate rating value
        
        Returns:
            bool: True if validation passes
        """
        # Check if value is within bounds
        if self.value < 0 or self.value > self.max_rating:
            return False
            
        # Check half-star constraints
        if not self.allow_half and self.value % 1 != 0:
            return False
            
        return True
    
    def on_rate(self, value: float) -> Dict[str, Any]:
        """
        Handle rating change
        
        Args:
            value: New rating value
            
        Returns:
            Dict containing response data
        """
        old_value = self.value
        self.value = value
        is_valid = self.validate()
        
        # Calculate percentage
        percentage = (value / self.max_rating) * 100 if self.max_rating > 0 else 0
        
        # Determine star display
        full_stars = int(value)
        has_half_star = (value % 1) >= 0.5
        empty_stars = self.max_rating - full_stars - (1 if has_half_star else 0)
        
        return {
            "success": True,
            "value": self.value,
            "previousValue": old_value,
            "valid": is_valid,
            "percentage": percentage,
            "stars": {
                "full": full_stars,
                "half": 1 if has_half_star else 0,
                "empty": empty_stars
            }
        }
    
    def clear_rating(self) -> Dict[str, Any]:
        """
        Clear rating value
        
        Returns:
            Dict containing response data
        """
        return self.on_rate(0)
    
    def set_max_rating(self) -> Dict[str, Any]:
        """
        Set to maximum rating
        
        Returns:
            Dict containing response data
        """
        return self.on_rate(self.max_rating)
    
    def increment_rating(self, step: float = 1) -> Dict[str, Any]:
        """
        Increment rating by step
        
        Args:
            step: Amount to increment
            
        Returns:
            Dict containing response data
        """
        new_value = min(self.value + step, self.max_rating)
        return self.on_rate(new_value)
    
    def decrement_rating(self, step: float = 1) -> Dict[str, Any]:
        """
        Decrement rating by step
        
        Args:
            step: Amount to decrement
            
        Returns:
            Dict containing response data
        """
        new_value = max(self.value - step, 0)
        return self.on_rate(new_value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "max": self.max_rating,
            "value": self.value,
            "allowHalf": self.allow_half,
            **self.get_base_props()
        }
        
        if self.onChange:
            props["onChange"] = self.onChange
            
        return {
            "type": "rate",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Rate':
        """
        Create rate component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Rate instance
        """
        return Rate(
            max_rating=data.get('max', 5),
            value=data.get('value', 0),
            allow_half=data.get('allowHalf', True),
            onChange=data.get('onChange')
        )

def create_rate(max_rating: int = 5, value: float = 0, allow_half: bool = True,
               onChange: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
    """Create a rate component"""
    component = Rate(max_rating, value, allow_half, onChange, **kwargs)
    return component.to_dict()