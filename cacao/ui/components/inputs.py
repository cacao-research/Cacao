"""
Inputs module for UI components in the Cacao framework.
Provides implementations for interactive input elements such as sliders and forms.
"""

from typing import Any, Dict, List, Optional, Callable, Union
from .base import Component

class Slider(Component):
    """
    A slider component for numeric input.
    """
    def __init__(self, min_value: float, max_value: float, step: float = 1.0, value: float = None) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value if value is not None else min_value

    def render(self) -> Dict[str, Any]:
        return {
            "type": "slider",
            "props": {
                "min": self.min_value,
                "max": self.max_value,
                "step": self.step,
                "value": self.value
            }
        }
# Form component has been moved to forms.py



def slider(min_value: float, max_value: float, step: float = 1.0,
          value: float = None, on_change: dict = None) -> dict:
    """
    Create a simple slider component.

    Args:
        min_value (float): Minimum value of the slider
        max_value (float): Maximum value of the slider
        step (float): Step size for the slider
        value (float): Initial value
        on_change (dict): Action configuration for value changes

    Returns:
        dict: Component definition
    """
    return {
        "type": "slider",
        "props": {
            "min": min_value,
            "max": max_value,
            "step": step,
            "value": value if value is not None else min_value,
            "onChange": on_change
        }
    }

# --- New Input Components ---

class Input(Component):
    """
    Single-line text input with support for type, placeholder, value, etc.
    """
    def __init__(
        self,
        input_type: str = "text",
        value: str = "",
        placeholder: str = "",
        on_change: Optional[Callable[[str], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.input_type = input_type
        self.value = value
        self.placeholder = placeholder
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "input",
            "props": {
                "inputType": self.input_type,
                "value": self.value,
                "placeholder": self.placeholder,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class TextArea(Component):
    """
    Multi-line text input.
    """
    def __init__(
        self,
        value: str = "",
        placeholder: str = "",
        rows: int = 4,
        on_change: Optional[Callable[[str], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.value = value
        self.placeholder = placeholder
        self.rows = rows
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "textarea",
            "props": {
                "value": self.value,
                "placeholder": self.placeholder,
                "rows": self.rows,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class SearchInput(Component):
    """
    Input field with a built-in search button.
    """
    def __init__(
        self,
        value: str = "",
        placeholder: str = "",
        on_search: Optional[Callable[[str], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.value = value
        self.placeholder = placeholder
        self.on_search = on_search
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "search",
            "props": {
                "value": self.value,
                "placeholder": self.placeholder,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class InputGroup(Component):
    """
    Groups multiple input fields together.
    """
    def __init__(
        self,
        children: List[Component],
        **kwargs
    ) -> None:
        self.children = children
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "inputGroup",
            "props": {
                "children": [child.render() for child in self.children],
                **self.extra_props
            }
        }

class Select(Component):
    """
    Allows users to choose from a list of options.
    """
    def __init__(
        self,
        options: List[Dict[str, Any]],
        value: Any = None,
        placeholder: str = "",
        on_change: Optional[Callable[[Any], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.options = options
        self.value = value
        self.placeholder = placeholder
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "select",
            "props": {
                "options": self.options,
                "value": self.value,
                "placeholder": self.placeholder,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class Cascader(Component):
    """
    Select options from a hierarchical menu.
    """
    def __init__(
        self,
        options: List[Dict[str, Any]],
        value: Any = None,
        placeholder: str = "",
        on_change: Optional[Callable[[Any], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.options = options
        self.value = value
        self.placeholder = placeholder
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "cascader",
            "props": {
                "options": self.options,
                "value": self.value,
                "placeholder": self.placeholder,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class Checkbox(Component):
    """
    Allows users to select one or more options.
    """
    def __init__(
        self,
        label: str = "",
        checked: bool = False,
        on_change: Optional[Callable[[bool], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.label = label
        self.checked = checked
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "checkbox",
            "props": {
                "label": self.label,
                "checked": self.checked,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class Radio(Component):
    """
    Allows users to select a single option from a group.
    """
    def __init__(
        self,
        options: List[Dict[str, Any]],
        value: Any = None,
        on_change: Optional[Callable[[Any], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.options = options
        self.value = value
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "radio",
            "props": {
                "options": self.options,
                "value": self.value,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class Switch(Component):
    """
    Toggles between two states (on/off).
    """
    def __init__(
        self,
        checked: bool = False,
        on_change: Optional[Callable[[bool], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.checked = checked
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "switch",
            "props": {
                "checked": self.checked,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class Rate(Component):
    """
    Allows users to give a rating (e.g., stars).
    """
    def __init__(
        self,
        value: int = 0,
        max_value: int = 5,
        on_change: Optional[Callable[[int], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.value = value
        self.max_value = max_value
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "rate",
            "props": {
                "value": self.value,
                "max": self.max_value,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class DatePicker(Component):
    """
    Allows users to select a date or date range.
    """
    def __init__(
        self,
        value: Any = None,
        range: bool = False,
        on_change: Optional[Callable[[Any], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.value = value
        self.range = range
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "datepicker",
            "props": {
                "value": self.value,
                "range": self.range,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class TimePicker(Component):
    """
    Allows users to select a time.
    """
    def __init__(
        self,
        value: Any = None,
        on_change: Optional[Callable[[Any], None]] = None,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.value = value
        self.on_change = on_change
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "timepicker",
            "props": {
                "value": self.value,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

class Upload(Component):
    """
    Allows users to upload files.
    """
    def __init__(
        self,
        files: Optional[List[Any]] = None,
        on_upload: Optional[Callable[[List[Any]], None]] = None,
        multiple: bool = False,
        disabled: bool = False,
        **kwargs
    ) -> None:
        self.files = files or []
        self.on_upload = on_upload
        self.multiple = multiple
        self.disabled = disabled
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "upload",
            "props": {
                "files": self.files,
                "multiple": self.multiple,
                "disabled": self.disabled,
                **self.extra_props
            }
        }

# Add Input subclasses as properties
Input.TextArea = TextArea
Input.Search = SearchInput
Input.Group = InputGroup
