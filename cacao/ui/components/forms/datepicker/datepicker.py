"""
Datepicker Component Python Integration
"""

from typing import Dict, Any, Optional
from datetime import datetime, date
from ...base import Component

class Datepicker(Component):
    """
    Server-side logic for datepicker component
    """
    
    def __init__(self, value: str = None, disabled: bool = False, min_date: str = None,
                 max_date: str = None, **kwargs):
        """
        Initialize datepicker component
        
        Args:
            value: Initial date value (YYYY-MM-DD format)
            disabled: Whether datepicker is disabled
            min_date: Minimum selectable date
            max_date: Maximum selectable date
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.value = value
        self.disabled = disabled
        self.min_date = min_date
        self.max_date = max_date
    
    def validate(self) -> bool:
        """
        Validate date value
        
        Returns:
            bool: True if validation passes
        """
        if not self.value:
            return True
            
        try:
            # Parse the date to ensure it's valid
            parsed_date = datetime.strptime(self.value, '%Y-%m-%d').date()
            
            # Check min/max constraints
            if self.min_date:
                min_parsed = datetime.strptime(self.min_date, '%Y-%m-%d').date()
                if parsed_date < min_parsed:
                    return False
                    
            if self.max_date:
                max_parsed = datetime.strptime(self.max_date, '%Y-%m-%d').date()
                if parsed_date > max_parsed:
                    return False
                    
            return True
        except ValueError:
            return False
    
    def on_change(self, value: str) -> Dict[str, Any]:
        """
        Handle date value change
        
        Args:
            value: New date value
            
        Returns:
            Dict containing response data
        """
        old_value = self.value
        self.value = value
        is_valid = self.validate()
        
        # Parse date for additional info
        parsed_date = None
        if value and is_valid:
            try:
                parsed_date = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        return {
            "success": True,
            "value": self.value,
            "previousValue": old_value,
            "valid": is_valid,
            "parsedDate": {
                "year": parsed_date.year if parsed_date else None,
                "month": parsed_date.month if parsed_date else None,
                "day": parsed_date.day if parsed_date else None,
                "weekday": parsed_date.weekday() if parsed_date else None
            } if parsed_date else None
        }
    
    def set_to_today(self) -> Dict[str, Any]:
        """
        Set date to today
        
        Returns:
            Dict containing response data
        """
        today = date.today().strftime('%Y-%m-%d')
        return self.on_change(today)
    
    def clear_date(self) -> Dict[str, Any]:
        """
        Clear date value
        
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
        if self.min_date:
            props["min"] = self.min_date
        if self.max_date:
            props["max"] = self.max_date
            
        return {
            "type": "datepicker",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Datepicker':
        """
        Create datepicker component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Datepicker instance
        """
        return Datepicker(
            value=data.get('value'),
            disabled=data.get('disabled', False),
            min_date=data.get('min'),
            max_date=data.get('max')
        )

def create_datepicker(value: str = None, disabled: bool = False, min_date: str = None,
                     max_date: str = None, **kwargs) -> Dict[str, Any]:
    """Create a datepicker component"""
    component = Datepicker(value, disabled, min_date, max_date, **kwargs)
    return component.to_dict()