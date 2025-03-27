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
