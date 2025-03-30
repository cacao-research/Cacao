import cacao
from cacao import State, Component
from typing import Dict, Any, Optional

app = cacao.App()

# Create counter state
counter_state = State(0)

# Create a counter component
class Counter(Component):
    def __init__(self) -> None:
        super().__init__()
        self.id = id(self)
        self.component_type = "counter"
        
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        counter_value = self._get_counter_value(ui_state)
        
        return {
            "type": "section",
            "component_type": self.component_type,
            "props": {
                "style": {
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "padding": "50px",
                    "background": "linear-gradient(145deg, #8B4513 0%, #D2691E 100%)",
                    "borderRadius": "30px",
                    "boxShadow": "0 20px 40px rgba(0,0,0,0.2)",
                    "maxWidth": "400px",
                    "width": "100%",
                    "margin": "0 auto",
                    "position": "relative",
                    "overflow": "hidden"
                },
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "position": "absolute",
                                "top": "0",
                                "left": "0",
                                "right": "0",
                                "height": "8px",
                                "background": "linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.3), rgba(255,255,255,0.1))",
                                "borderTopLeftRadius": "30px",
                                "borderTopRightRadius": "30px"
                            }
                        }
                    },
                    {
                        "type": "text",
                        "props": {
                            "content": str(counter_value),
                            "style": {
                                "fontSize": "96px",
                                "fontWeight": "800",
                                "color": "white",
                                "textShadow": "2px 2px 8px rgba(0,0,0,0.3)",
                                "margin": "20px 0 40px 0",
                                "fontFamily": "'Poppins', sans-serif",
                                "letterSpacing": "-2px",
                                "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
                            }
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "flex",
                                "gap": "30px",
                                "marginTop": "10px"
                            },
                            "children": [
                                {
                                    "type": "button",
                                    "props": {
                                        "label": "−",
                                        "action": "decrease_counter",
                                        "style": {
                                            "fontSize": "36px",
                                            "width": "80px",
                                            "height": "80px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": "rgba(255, 255, 255, 0.15)",
                                            "color": "white",
                                            "border": "2px solid rgba(255, 255, 255, 0.3)",
                                            "borderRadius": "50%",
                                            "cursor": "pointer",
                                            "transition": "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                                            ":hover": {
                                                "backgroundColor": "rgba(255, 255, 255, 0.25)",
                                                "transform": "translateY(-3px)",
                                                "boxShadow": "0 10px 20px rgba(0,0,0,0.2)"
                                            },
                                            ":active": {
                                                "transform": "translateY(0)",
                                                "boxShadow": "0 5px 10px rgba(0,0,0,0.2)"
                                            }
                                        }
                                    }
                                },
                                {
                                    "type": "button",
                                    "props": {
                                        "label": "+",
                                        "action": "increment_counter",
                                        "style": {
                                            "fontSize": "36px",
                                            "width": "80px",
                                            "height": "80px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "backgroundColor": "rgba(255, 255, 255, 0.15)",
                                            "color": "white",
                                            "border": "2px solid rgba(255, 255, 255, 0.3)",
                                            "borderRadius": "50%",
                                            "cursor": "pointer",
                                            "transition": "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                                            ":hover": {
                                                "backgroundColor": "rgba(255, 255, 255, 0.25)",
                                                "transform": "translateY(-3px)",
                                                "boxShadow": "0 10px 20px rgba(0,0,0,0.2)"
                                            },
                                            ":active": {
                                                "transform": "translateY(0)",
                                                "boxShadow": "0 5px 10px rgba(0,0,0,0.2)"
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    
    def _get_counter_value(self, ui_state: Optional[Dict[str, Any]] = None) -> int:
        if ui_state and isinstance(ui_state, dict) and 'counter' in ui_state:
            return ui_state['counter']
        return counter_state.value

# Subscribe to counter changes
@counter_state.subscribe
def on_counter_change(new_value: int) -> None:
    print(f"Counter changed to: {new_value}")

# Register event handler for the increment_counter action
@app.event("increment_counter")
def handle_increment_counter(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle counter increment button click.
    
    Args:
        event_data: Event data passed from the frontend
        
    Returns:
        Dict[str, Any]: Response with updated counter value
    """
    print(f"Increment counter event received with data: {event_data}")
    # Increment the counter state using set() method
    counter_state.set(counter_state.value + 1)
    print(f"Counter incremented to: {counter_state.value}")
    
    # Return updated state
    return {
        "counter": counter_state.value
    }

# Register event handler for the decrease_counter action
@app.event("decrease_counter")
def handle_decrease_counter(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle counter decrement button click.
    
    Args:
        event_data: Event data passed from the frontend
        
    Returns:
        Dict[str, Any]: Response with updated counter value
    """
    print(f"Decrease counter event received with data: {event_data}")
    # Decrement the counter state using set() method
    counter_state.set(counter_state.value - 1)
    print(f"Counter decremented to: {counter_state.value}")
    
    # Return updated state
    return {
        "counter": counter_state.value
    }

@app.mix("/")
def home() -> Dict[str, Any]:
    """Main page with counter."""
    counter_component = Counter()
    
    return {
        "type": "div",
        "props": {
            "style": {
                "minHeight": "100vh",
                "background": "linear-gradient(135deg, #2c1810 0%, #3a1f14 100%)",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "padding": "40px 20px",
                "fontFamily": "'Poppins', sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Cacao Counter Example",
                    "style": {
                        "fontSize": "48px",
                        "fontWeight": "800",
                        "color": "#f0be9b",
                        "textAlign": "center",
                        "marginBottom": "60px",
                        "textShadow": "0 2px 4px rgba(0,0,0,0.3)",
                        "letterSpacing": "-1px",
                        "position": "relative",
                        "padding": "0 0 20px 0",
                        "width": "100%"
                    }
                }
            },
            counter_component.render()
        ]
    }

if __name__ == "__main__":
    app.brew()  # Run the app like brewing hot chocolate!
