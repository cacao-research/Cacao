"""
Search Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class SearchInput(Component):
    """
    Server-side logic for search component
    """
    
    def __init__(self, value: str = "", placeholder: str = None, disabled: bool = False, **kwargs):
        """
        Initialize search component
        
        Args:
            value: Initial search value
            placeholder: Placeholder text
            disabled: Whether search is disabled
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.value = value
        self.placeholder = placeholder
        self.disabled = disabled
    
    def validate(self) -> bool:
        """
        Validate search value
        
        Returns:
            bool: True if validation passes
        """
        # Basic validation - search can be empty
        return True
    
    def on_search(self, value: str) -> Dict[str, Any]:
        """
        Handle search query
        
        Args:
            value: Search query value
            
        Returns:
            Dict containing search results or response data
        """
        self.value = value
        
        # Add search logic here
        # For example, filter data, call search API, etc.
        
        return {
            "success": True,
            "query": self.value,
            "results": [],  # Replace with actual search results
            "total": 0
        }
    
    def clear_search(self) -> Dict[str, Any]:
        """
        Clear search value
        
        Returns:
            Dict containing response data
        """
        self.value = ""
        
        return {
            "success": True,
            "query": "",
            "cleared": True
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "value": self.value,
            "disabled": self.disabled,
            **self.get_base_props()
        }
        
        if self.placeholder:
            props["placeholder"] = self.placeholder
            
        return {
            "type": "search",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'SearchInput':
        """
        Create search component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            SearchInput instance
        """
        return SearchInput(
            value=data.get('value', ''),
            placeholder=data.get('placeholder'),
            disabled=data.get('disabled', False)
        )

def create_search(value: str = "", placeholder: str = None, disabled: bool = False, **kwargs) -> Dict[str, Any]:
    """Create a search component"""
    component = SearchInput(value, placeholder, disabled, **kwargs)
    return component.to_dict()