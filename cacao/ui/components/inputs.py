"""
Inputs module for UI components in the Cacao framework.
Provides implementations for interactive input elements such as sliders and forms.
"""

from typing import Any, Dict, List, Optional, Callable, Union
from .base import Component


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


