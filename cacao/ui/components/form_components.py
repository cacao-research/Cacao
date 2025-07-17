"""
Forms module for UI components in the Cacao framework.
Provides backward compatibility imports for components that have been migrated to the new folder structure.
"""

from typing import List, Dict, Any, Optional, Callable, Union
from .base import Component

from .forms import (
    Input,
    SearchInput,
    Select,
    Checkbox,
    Radio,
    Switch,
    Textarea,
    Datepicker,
    Timepicker,
    Slider,
    Rate,
    Upload
)


class Form(Component):
    """
    Collects and validates user input with labels, controls, and validation rules.
    """
    def __init__(
        self,
        fields: List[Dict[str, Any]],
        layout: str = "vertical",
        on_submit: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_change: Optional[Callable[[Dict[str, Any]], None]] = None,
        initial_values: Dict[str, Any] = None,
        validation_rules: Dict[str, List[Dict[str, Any]]] = None,
        **kwargs
    ) -> None:
        self.fields = fields
        self.layout = layout
        self.on_submit = on_submit
        self.on_change = on_change
        self.initial_values = initial_values or {}
        self.validation_rules = validation_rules or {}
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "form",
            "props": {
                "fields": self.fields,
                "layout": self.layout,
                "initialValues": self.initial_values,
                "validationRules": self.validation_rules,
                **self.extra_props
            }
        }

class FormItem(Component):
    """
    A single form item with label, control, and validation.
    """
    def __init__(
        self,
        name: str,
        label: str,
        control: Component,
        rules: List[Dict[str, Any]] = None,
        help_text: str = None,
        **kwargs
    ) -> None:
        self.name = name
        self.label = label
        self.control = control
        self.rules = rules or []
        self.help_text = help_text
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "formItem",
            "props": {
                "name": self.name,
                "label": self.label,
                "control": self.control.render(),
                "rules": self.rules,
                "helpText": self.help_text,
                **self.extra_props
            }
        }

def create_form(
    fields: List[Dict[str, Any]],
    layout: str = "vertical",
    on_submit: Optional[Dict[str, Any]] = None,
    initial_values: Dict[str, Any] = None,
    validation_rules: Dict[str, List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create a form component with fields, layout, and validation.

    Args:
        fields (List[Dict[str, Any]]): Form fields configuration
        layout (str): Form layout ('vertical', 'horizontal', 'inline')
        on_submit (Dict[str, Any]): Action configuration for form submission
        initial_values (Dict[str, Any]): Initial values for form fields
        validation_rules (Dict[str, List[Dict[str, Any]]]): Validation rules for fields

    Returns:
        Dict[str, Any]: Form component definition
    """
    return {
        "type": "form",
        "props": {
            "fields": fields,
            "layout": layout,
            "initialValues": initial_values or {},
            "validationRules": validation_rules or {},
            "onSubmit": on_submit
        }
    }

# Export all form components and helpers for backward compatibility
__all__ = [
    # Base form components
    'Form', 'FormItem', 'create_form',
    
    # Individual component classes
    'Input', 'SearchInput', 'Select', 'Checkbox',
    'Radio', 'Switch', 'Textarea', 'Datepicker',
    'Timepicker', 'Slider', 'Rate', 'Upload',
    
    # Helper functions
    'create_input', 'create_search', 'create_select', 'create_checkbox',
    'create_radio', 'create_switch', 'create_textarea', 'create_datepicker',
    'create_timepicker', 'create_slider', 'create_rate', 'create_upload'
]