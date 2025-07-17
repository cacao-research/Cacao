"""
Textarea Component Python Integration
"""

from typing import Dict, Any, Optional
from ...base import Component

class Textarea(Component):
    """
    Server-side logic for textarea component
    """
    
    def __init__(self, content: str = "", placeholder: str = None, disabled: bool = False,
                 action: str = None, **kwargs):
        """
        Initialize textarea component
        
        Args:
            content: Initial content
            placeholder: Placeholder text
            disabled: Whether textarea is disabled
            action: Action to trigger on content change
            **kwargs: Additional component properties
        """
        super().__init__(**kwargs)
        self.content = content
        self.placeholder = placeholder
        self.disabled = disabled
        self.action = action
    
    def validate(self) -> bool:
        """
        Validate textarea content
        
        Returns:
            bool: True if validation passes
        """
        # Add validation logic here (e.g., length limits, content rules)
        return True
    
    def on_change(self, content: str) -> Dict[str, Any]:
        """
        Handle textarea content change
        
        Args:
            content: New content value
            
        Returns:
            Dict containing response data
        """
        old_content = self.content
        self.content = content
        is_valid = self.validate()
        
        # Calculate statistics
        word_count = len(content.split()) if content else 0
        char_count = len(content)
        
        return {
            "success": True,
            "content": self.content,
            "previousContent": old_content,
            "valid": is_valid,
            "stats": {
                "wordCount": word_count,
                "charCount": char_count
            }
        }
    
    def clear_content(self) -> Dict[str, Any]:
        """
        Clear textarea content
        
        Returns:
            Dict containing response data
        """
        return self.on_change("")
    
    def append_content(self, text: str) -> Dict[str, Any]:
        """
        Append text to current content
        
        Args:
            text: Text to append
            
        Returns:
            Dict containing response data
        """
        new_content = self.content + text
        return self.on_change(new_content)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary for rendering
        
        Returns:
            Dict containing component data
        """
        props = {
            "content": self.content,
            "disabled": self.disabled,
            **self.get_base_props()
        }
        
        if self.placeholder:
            props["placeholder"] = self.placeholder
        if self.action:
            props["action"] = self.action
            
        return {
            "type": "textarea",
            "props": props
        }
    
    @staticmethod
    def from_form_data(data: Dict[str, Any]) -> 'Textarea':
        """
        Create textarea component from form data
        
        Args:
            data: Form data dictionary
            
        Returns:
            Textarea instance
        """
        return Textarea(
            content=data.get('content', ''),
            placeholder=data.get('placeholder'),
            disabled=data.get('disabled', False),
            action=data.get('action')
        )

def create_textarea(content: str = "", placeholder: str = None, disabled: bool = False,
                   action: str = None, **kwargs) -> Dict[str, Any]:
    """Create a textarea component"""
    component = Textarea(content, placeholder, disabled, action, **kwargs)
    return component.to_dict()