"""
Timepicker Component Python Integration
"""

from typing import Dict, Any, Optional
from datetime import datetime, time
from ...base import Component

class Timepicker(Component):
    """
    Server-side logic for timepicker component
    """
    
    def __init__(self, value: str = None, disabled: bool = False, min_time: str = None,
                 max_time: str = None, **kwargs):
        """
        Initialize timepicker component
        
        Args:
            value: Initial time value (HH:MM format)
            disabled: Whether timepicker is disabled
            min_time: Minimum selectable time
            max_time: Maximum selectable time
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.value = value
        self.disabled = disabled
        self.min_time = min_time
        self.max_time = max_time
    
    def validate(self) -> bool:
        """
        Validate time value
        
        Returns:
            bool: True if validation passes
        """
        if not self.value:
            return True
            
        try:
            # Parse the time to ensure it's valid
            parsed_time = datetime.strptime(self.value, '%H:%M').time()
            
            # Check min/max constraints
            if self.min_time:
                min_parsed = datetime.strptime(self.min_time, '%H:%M').time()
                if parsed_time < min_parsed:
                    return False
                    
            if self.max_time:
                max_parsed = datetime.strptime(self.max_time, '%H:%M').time()
                if parsed_time > max_parsed:
                    return False
                    
            return True
        except ValueError:
            return False
    
    def on_change(self, value: str) -> Dict[str, Any]:
        """
        Handle time value change
        
        Args:
            value: New time value
            
        Returns:
            Dict containing response data
        """
        old_value = self.value
        self.value = value
        is_valid = self.validate()
        
        # Parse time for additional info
        parsed_time = None
        if value and is_valid:
            try:
                parsed_time = datetime.strptime(value, '%H:%M').time()
            except ValueError:
                pass
        
        return {
            "success": True,
            "value": self.value,
            "previousValue": old_value,
            "valid": is_valid,
            "parsedTime": {
                "hour": parsed_time.hour if parsed_time else None,
                "minute": parsed_time.minute if parsed_time else None,
                "hour12": parsed_time.hour % 12 if parsed_time else None,
                "ampm": "AM" if parsed_time and parsed_time.hour < 12 else "PM" if parsed_time else None
            } if parsed_time else None
        }
    
    def set_to_now(self) -> Dict[str, Any]:
        """
        Set time to current time
        
        Returns:
            Dict containing response data
        """
        now = datetime.now().time().strftime('%H:%M')
        return self.on_change(now)
    
    def clear_time(self) -> Dict[str, Any]:
        """
        Clear time value
        
        Returns:
            Dict containing response data
        """
        return self.on_change("")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "disabled": self.disabled,
            **self.get_base_props()
        }
        
        if self.value:
            props["value"] = self.value
        if self.min_time:
            props["min"] = self.min_time
        if self.max_time:
            props["max"] = self.max_time
            
        return {
            "type": "timepicker",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Timepicker':
        """
        Create timepicker component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Timepicker instance
        """
        return Timepicker(
            value=data.get('value'),
            disabled=data.get('disabled', False),
            min_time=data.get('min'),
            max_time=data.get('max')
        )

def create_timepicker(value: str = None, disabled: bool = False, min_time: str = None,
                     max_time: str = None, **kwargs) -> Dict[str, Any]:
    """Create a timepicker component"""
    component = Timepicker(value, disabled, min_time, max_time, **kwargs)
    return component.to_dict()