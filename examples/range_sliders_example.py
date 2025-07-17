"""
Example demonstrating how a slider component can update another component.
Shows how to create a simple slider that updates a separate value display.
"""

import cacao
from cacao import State
from typing import Dict, Any

app = cacao.App()

# Create state for slider value
slider_value = State(500)

@app.mix("/")
def home() -> Dict[str, Any]:
    """Main page with slider and value display."""
    return {
        "type": "div",
        "props": {
            "style": {
                "minHeight": "100vh",
                "background": "linear-gradient(135deg, #2c1810 0%, #3a1f14 100%)",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "padding": "20px",
                "fontFamily": "'Poppins', sans-serif"
            }
        },
        "children": [
            {
                "type": "div",
                "props": {
                    "style": {
                        "maxWidth": "800px",
                        "width": "100%",
                        "margin": "0 auto",
                        "textAlign": "center"
                    },
                    "children": [
                        {
                            "type": "h1",
                            "props": {
                                "content": "Slider Example {%icon-fa-sliders%}",
                                "style": {
                                    "fontSize": "48px",
                                    "fontWeight": "800",
                                    "color": "#934a15",
                                    "marginBottom": "40px",
                                    "textShadow": "0 2px 4px rgba(0,0,0,0.3)",
                                    "letterSpacing": "-1px"
                                }
                            }
                        },
                        {
                            "type": "section",
                            "component_type": "slider_section",
                            "props": {
                                "style": {
                                    "background": "linear-gradient(145deg, #8B4513 0%, #D2691E 100%)",
                                    "borderRadius": "30px",
                                    "boxShadow": "0 20px 40px rgba(0,0,0,0.2)",
                                    "padding": "40px",
                                    "position": "relative",
                                    "overflow": "hidden"
                                },
                                "children": [
                                    {
                                        "type": "h3",
                                        "props": {
                                            "content": "Adjust the slider to update the value display",
                                            "style": {
                                                "color": "#ffffff",
                                                "marginBottom": "30px",
                                                "fontSize": "20px",
                                                "fontWeight": "500"
                                            }
                                        }
                                    },
                                    # Slider component
                                    {
                                        "type": "div",
                                        "props": {
                                            "style": {
                                                "padding": "20px",
                                                "background": "rgba(0,0,0,0.1)",
                                                "borderRadius": "15px",
                                                "marginBottom": "30px"
                                            },
                                            "children": [
                                                {
                                                    "type": "p",
                                                    "props": {
                                                        "content": "Slider Component",
                                                        "style": {
                                                            "color": "#ffffff",
                                                            "marginBottom": "15px",
                                                            "fontSize": "18px",
                                                            "fontWeight": "bold"
                                                        }
                                                    }
                                                },
                                                {
                                                    "type": "range-slider",
                                                    "props": {
                                                        "className": "range-slider",
                                                        "min": 0,
                                                        "max": 1000,
                                                        "step": 10,
                                                        "value": slider_value.value,
                                                        "onChange": {
                                                            "action": "update_slider",
                                                            "params": {
                                                                "component_type": "slider_section"
                                                            }
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    # Separate value display component
                                    {
                                        "type": "div",
                                        "props": {
                                            "style": {
                                                "padding": "20px",
                                                "background": "rgba(0,0,0,0.1)",
                                                "borderRadius": "15px"
                                            },
                                            "children": [
                                                {
                                                    "type": "p",
                                                    "props": {
                                                        "content": "Value Display Component",
                                                        "style": {
                                                            "color": "#ffffff",
                                                            "marginBottom": "15px",
                                                            "fontSize": "18px",
                                                            "fontWeight": "bold"
                                                        }
                                                    }
                                                },
                                                {
                                                    "type": "div",
                                                    "props": {
                                                        "className": "value-display",
                                                        "content": f"Current Value: {slider_value.value}"
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }

@app.event("update_slider")
def handle_slider_change(value: float) -> Dict[str, Any]:
    """Handle changes in slider value.
    
    Args:
        value: New value for the slider
    """
    value = float(value)
    print(f"Updating slider to: {value}")
    slider_value.set(value)
    return {"value": value}

if __name__ == "__main__":
    app.brew()