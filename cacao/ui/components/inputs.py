"""
Inputs module for UI components in the Cacao framework.
Provides implementations for interactive input elements such as sliders and forms.
"""

from typing import Any, Dict
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

class Form(Component):
    """
    A simple form component for handling user input.
    """
    def __init__(self, fields: Dict[str, Any]) -> None:
        self.fields = fields

    def render(self) -> Dict[str, Any]:
        return {
            "type": "form",
            "props": {
                "fields": self.fields
            }
        }


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


def range_sliders(min_value: float, max_value: float, step: float = 1.0,
                 lower_value: float = None, upper_value: float = None,
                 on_change: dict = None) -> dict:
    """
    Create a range sliders component that allows selecting a range between min and max values.
    Provides two handles for selecting both lower and upper bounds.

    Args:
        min_value (float): Minimum value of the range
        max_value (float): Maximum value of the range
        step (float): Step size for the sliders
        lower_value (float): Initial lower bound value
        upper_value (float): Initial upper bound value
        on_change (dict): Action configuration for value changes

    Returns:
        dict: Component definition
    """
    return {
        "type": "range-sliders",
        "props": {
            "min": min_value,
            "max": max_value,
            "step": step,
            "lowerValue": lower_value if lower_value is not None else min_value,
            "upperValue": upper_value if upper_value is not None else max_value,
            "onChange": on_change
        }
    }


class RangeSliders(Component):
    """
    A range sliders component that allows selecting a range between min and max values.
    Provides two handles for selecting both lower and upper bounds.
    """
    def __init__(self,
                 min_value: float,
                 max_value: float,
                 step: float = 1.0,
                 lower_value: float = None,
                 upper_value: float = None,
                 on_change: callable = None) -> None:
        """
        Initialize a RangeSliders component.
        
        Args:
            min_value (float): Minimum value of the range
            max_value (float): Maximum value of the range
            step (float): Step size for the sliders
            lower_value (float): Initial lower bound value
            upper_value (float): Initial upper bound value
            on_change (callable): Callback function when values change
        """
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.lower_value = lower_value if lower_value is not None else min_value
        self.upper_value = upper_value if upper_value is not None else max_value
        self.on_change = on_change

    def render(self) -> Dict[str, Any]:
        return {
            "type": "range-sliders",
            "props": {
                "min": self.min_value,
                "max": self.max_value,
                "step": self.step,
                "lowerValue": self.lower_value,
                "upperValue": self.upper_value,
                "onChange": {
                    "action": "update_range",
                    "params": {
                        "component_type": "range-sliders"
                    }
                } if self.on_change else None
            }
        }
