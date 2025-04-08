"""
Range Sliders component for Cacao framework.
Provides a customizable dual-slider component for selecting a range of values.
"""

from typing import Dict, Any, Optional, Callable
from .base import Component
from ...core.state import State, get_state

class RangeSliders(Component):
    def __init__(self, 
                 min_value: float, 
                 max_value: float, 
                 step: float = 1.0, 
                 lower_value: float = None, 
                 upper_value: float = None,
                 on_change: Callable = None,
                 styles: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a RangeSliders component.
        
        Args:
            min_value (float): Minimum value of the range
            max_value (float): Maximum value of the range
            step (float): Step size for the sliders
            lower_value (float): Initial lower bound value
            upper_value (float): Initial upper bound value
            on_change (Callable): Callback function when values change
            styles (Dict[str, Any]): Optional dictionary of style overrides
        """
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.lower_value = lower_value if lower_value is not None else min_value
        self.upper_value = upper_value if upper_value is not None else max_value
        self.on_change = on_change
        self.styles = styles or {}
        self.component_type = "range_sliders"
        
    def render(self) -> Dict[str, Any]:
        """Render the range sliders component.
        
        Returns:
            Dict[str, Any]: UI definition for the range sliders
        """
        # Get default styles with overrides from props
        thumb_color = self.styles.get("thumb_color", "#ffffff")
        thumb_border = self.styles.get("thumb_border", "#D2691E")
        track_color = self.styles.get("track_color", "rgba(255,255,255,0.3)")
        container_padding = self.styles.get("container_padding", "20px")
        value_display_bg = self.styles.get("value_display_bg", "rgba(255,255,255,0.1)")
        
        # Create the component structure
        return {
            "type": "div",
            "component_type": self.component_type,
            "props": {
                "className": "range-sliders-container",
                "style": {
                    "width": "100%",
                    "padding": container_padding,
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center"
                },
                "children": [
                    # Style element for the sliders
                    {
                        "type": "style",
                        "props": {
                            "content": f"""
                                .range-slider {{
                                    width: 100%;
                                    margin: 10px 0;
                                    -webkit-appearance: none;
                                    background: transparent;
                                }}
                                .range-slider::-webkit-slider-thumb {{
                                    -webkit-appearance: none;
                                    height: 24px;
                                    width: 24px;
                                    border-radius: 50%;
                                    background: {thumb_color};
                                    cursor: pointer;
                                    margin-top: -10px;
                                    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                                    border: 2px solid {thumb_border};
                                    transition: all 0.2s ease;
                                }}
                                .range-slider::-webkit-slider-thumb:hover {{
                                    transform: scale(1.1);
                                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                                }}
                                .range-slider::-webkit-slider-runnable-track {{
                                    width: 100%;
                                    height: 4px;
                                    background: {track_color};
                                    border-radius: 2px;
                                }}
                                .range-display {{
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    margin-top: 20px;
                                    font-size: 20px;
                                    color: #ffffff;
                                    font-weight: bold;
                                    text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
                                }}
                                .range-value {{
                                    min-width: 60px;
                                    text-align: center;
                                    padding: 5px 10px;
                                    background: {value_display_bg};
                                    border-radius: 15px;
                                    margin: 0 10px;
                                }}
                            """
                        }
                    },
                    # Sliders container
                    {
                        "type": "div",
                        "props": {
                            "className": "sliders-wrapper",
                            "style": {
                                "width": "100%",
                                "position": "relative",
                                "padding": "10px 0"
                            },
                            "children": [
                                # Lower slider
                                {
                                    "type": "range-slider",
                                    "props": {
                                        "className": "range-slider lower",
                                        "min": self.min_value,
                                        "max": self.max_value,
                                        "step": self.step,
                                        "value": self.lower_value,
                                        "onChange": {
                                            "action": "update_range_sliders",
                                            "params": {
                                                "component_type": self.component_type,
                                                "slider": "lower"
                                            }
                                        }
                                    }
                                },
                                # Upper slider
                                {
                                    "type": "range-slider",
                                    "props": {
                                        "className": "range-slider upper",
                                        "min": self.min_value,
                                        "max": self.max_value,
                                        "step": self.step,
                                        "value": self.upper_value,
                                        "onChange": {
                                            "action": "update_range_sliders",
                                            "params": {
                                                "component_type": self.component_type,
                                                "slider": "upper"
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    # Value display
                    {
                        "type": "div",
                        "props": {
                            "className": "range-display",
                            "children": [
                                {
                                    "type": "div",
                                    "props": {
                                        "className": "range-value lower",
                                        "content": str(self.lower_value)
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "content": "-",
                                        "style": {
                                            "margin": "0 5px"
                                        }
                                    }
                                },
                                {
                                    "type": "div",
                                    "props": {
                                        "className": "range-value upper",
                                        "content": str(self.upper_value)
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }