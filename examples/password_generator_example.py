import cacao
from cacao import State, Component
from typing import Dict, Any, Optional
import random
import string

app = cacao.App()

# Create password state with all the specified properties
password_state = State({
    'length': 12,
    'easy_to_say': False,
    'easy_to_read': False,
    'all_characters': True,
    'uppercase': True,
    'lowercase': True,
    'numbers': True,
    'symbols': True,
    'password': '',
    'copied': False
})

def generate_password() -> str:
    """Generate a password based on current state settings."""
    state = password_state.value
    
    # Define character sets
    uppercase_chars = string.ascii_uppercase  # A-Z
    lowercase_chars = string.ascii_lowercase  # a-z
    number_chars = string.digits             # 0-9
    symbol_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Handle easy_to_say filtering (removes 0, O, l, 1)
    if state['easy_to_say']:
        uppercase_chars = uppercase_chars.replace('O', '')
        lowercase_chars = lowercase_chars.replace('l', '')
        number_chars = number_chars.replace('0', '').replace('1', '')
    
    # Handle easy_to_read filtering (removes I, l, 1, O, 0)
    if state['easy_to_read']:
        uppercase_chars = uppercase_chars.replace('I', '').replace('O', '')
        lowercase_chars = lowercase_chars.replace('l', '')
        number_chars = number_chars.replace('1', '').replace('0', '')
    
    # Build character pool based on toggles
    char_pool = ""
    
    if state['all_characters']:
        # When all_characters is True, use all character types
        char_pool = uppercase_chars + lowercase_chars + number_chars + symbol_chars
    else:
        # Use individual toggles
        if state['uppercase']:
            char_pool += uppercase_chars
        if state['lowercase']:
            char_pool += lowercase_chars
        if state['numbers']:
            char_pool += number_chars
        if state['symbols']:
            char_pool += symbol_chars
    
    # Ensure we have characters to work with
    if not char_pool:
        char_pool = lowercase_chars  # Fallback to lowercase letters
    
    # Generate password of specified length
    password = ''.join(random.choice(char_pool) for _ in range(state['length']))
    
    return password

def regenerate_password() -> None:
    """Regenerate password and update state."""
    current_state = password_state.value.copy()
    current_state['password'] = generate_password()
    current_state['copied'] = False  # Reset copied status when regenerating
    password_state.set(current_state)

# Subscribe to password state changes to automatically regenerate password
@password_state.subscribe
def on_password_state_change(new_state: Dict[str, Any]) -> None:
    """Handle password state changes and regenerate password when settings change."""
    print(f"Password state changed: {new_state}")
    
    # Check if any settings that affect password generation have changed
    # (We'll regenerate on any change for now, but could be more selective)
    if new_state['password'] == '':
        # If password is empty (initial state), generate one
        regenerate_password()

# Create a basic PasswordGenerator component for future UI use
class PasswordGenerator(Component):
    def __init__(self) -> None:
        super().__init__()
        self.id = id(self)
        self.component_type = "password_generator"
        
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the password generator component."""
        password_data = self._get_password_state(ui_state)
        
        return {
            "type": "section",
            "component_type": self.component_type,
            "props": {
                "style": {
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "padding": "40px",
                    "background": "linear-gradient(145deg, #1e3c72 0%, #2a5298 100%)",
                    "borderRadius": "25px",
                    "boxShadow": "0 20px 40px rgba(0,0,0,0.3)",
                    "maxWidth": "600px",
                    "width": "100%",
                    "margin": "0 auto",
                    "color": "white",
                    "position": "relative",
                    "overflow": "hidden"
                },
                "children": [
                    # Decorative top bar
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "position": "absolute",
                                "top": "0",
                                "left": "0",
                                "right": "0",
                                "height": "6px",
                                "background": "linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.4), rgba(255,255,255,0.1))",
                                "borderTopLeftRadius": "25px",
                                "borderTopRightRadius": "25px"
                            }
                        }
                    },
                    
                    # Title
                    {
                        "type": "h2",
                        "props": {
                            "content": "Password Generator",
                            "style": {
                                "fontSize": "32px",
                                "fontWeight": "800",
                                "marginBottom": "30px",
                                "textAlign": "center",
                                "color": "white",
                                "textShadow": "0 2px 4px rgba(0,0,0,0.3)",
                                "letterSpacing": "-1px"
                            }
                        }
                    },
                    
                    # Password Display Section
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "100%",
                                "marginBottom": "30px"
                            },
                            "children": [
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "background": "rgba(255,255,255,0.1)",
                                            "padding": "20px",
                                            "borderRadius": "12px",
                                            "border": "2px solid rgba(255,255,255,0.2)",
                                            "marginBottom": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": password_data.get('password', 'Click Generate to create password'),
                                                    "style": {
                                                        "fontSize": "18px",
                                                        "fontFamily": "'Consolas', 'Monaco', monospace",
                                                        "wordBreak": "break-all",
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "lineHeight": "1.4",
                                                        "fontWeight": "600",
                                                        "letterSpacing": "1px"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                # Copy button and status
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "gap": "15px"
                                        },
                                        "children": [
                                            {
                                                "type": "button",
                                                "props": {
                                                    "label": "📋 Copy",
                                                    "action": "copy_password",
                                                    "style": {
                                                        "padding": "10px 20px",
                                                        "backgroundColor": "rgba(255,255,255,0.2)",
                                                        "color": "white",
                                                        "border": "2px solid rgba(255,255,255,0.3)",
                                                        "borderRadius": "10px",
                                                        "fontSize": "14px",
                                                        "fontWeight": "600",
                                                        "cursor": "pointer",
                                                        "transition": "all 0.2s ease",
                                                        ":hover": {
                                                            "backgroundColor": "rgba(255,255,255,0.3)",
                                                            "transform": "translateY(-2px)",
                                                            "boxShadow": "0 6px 12px rgba(0,0,0,0.2)"
                                                        }
                                                    }
                                                }
                                            },
                                            # Copied status indicator
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": "✓ Copied!" if password_data.get('copied', False) else "",
                                                    "style": {
                                                        "fontSize": "14px",
                                                        "color": "#4ade80",
                                                        "fontWeight": "600",
                                                        "opacity": "1" if password_data.get('copied', False) else "0",
                                                        "transition": "opacity 0.3s ease"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Password Length Control
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "100%",
                                "marginBottom": "25px"
                            },
                            "children": [
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "space-between",
                                            "marginBottom": "10px"
                                        },
                                        "children": [
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": "Password Length",
                                                    "style": {
                                                        "fontSize": "16px",
                                                        "fontWeight": "600",
                                                        "color": "white"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": str(password_data.get('length', 12)),
                                                    "style": {
                                                        "fontSize": "18px",
                                                        "fontWeight": "700",
                                                        "color": "#60a5fa",
                                                        "background": "rgba(255,255,255,0.1)",
                                                        "padding": "5px 12px",
                                                        "borderRadius": "8px",
                                                        "minWidth": "40px",
                                                        "textAlign": "center"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "slider",
                                    "props": {
                                        "className": "range-slider",
                                        "min": 4,
                                        "max": 50,
                                        "step": 1,
                                        "value": password_data.get('length', 12),
                                        "onChange": {
                                            "action": "update_length"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Character Options
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "100%",
                                "marginBottom": "25px"
                            },
                            "children": [
                                {
                                    "type": "text",
                                    "props": {
                                        "content": "Character Options",
                                        "style": {
                                            "fontSize": "16px",
                                            "fontWeight": "600",
                                            "color": "white",
                                            "marginBottom": "15px",
                                            "display": "block"
                                        }
                                    }
                                },
                                
                                # Special options
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "flexDirection": "column",
                                            "gap": "12px",
                                            "marginBottom": "20px"
                                        },
                                        "children": [
                                            {
                                                "type": "label",
                                                "props": {
                                                    "style": {
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "gap": "10px",
                                                        "cursor": "pointer",
                                                        "padding": "8px",
                                                        "borderRadius": "8px",
                                                        "transition": "background-color 0.2s ease",
                                                        ":hover": {
                                                            "backgroundColor": "rgba(255,255,255,0.1)"
                                                        }
                                                    },
                                                    "children": [
                                                        {
                                                            "type": "checkbox",
                                                            "props": {
                                                                "checked": password_data.get('easy_to_say', False),
                                                                "action": "toggle_easy_to_say",
                                                                "style": {
                                                                    "width": "18px",
                                                                    "height": "18px",
                                                                    "cursor": "pointer"
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "type": "text",
                                                            "props": {
                                                                "content": "Easy to say (no 0, O, l, 1)",
                                                                "style": {
                                                                    "fontSize": "14px",
                                                                    "color": "white",
                                                                    "fontWeight": "500"
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                "type": "label",
                                                "props": {
                                                    "style": {
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "gap": "10px",
                                                        "cursor": "pointer",
                                                        "padding": "8px",
                                                        "borderRadius": "8px",
                                                        "transition": "background-color 0.2s ease",
                                                        ":hover": {
                                                            "backgroundColor": "rgba(255,255,255,0.1)"
                                                        }
                                                    },
                                                    "children": [
                                                        {
                                                            "type": "checkbox",
                                                            "props": {
                                                                "checked": password_data.get('easy_to_read', False),
                                                                "action": "toggle_easy_to_read",
                                                                "style": {
                                                                    "width": "18px",
                                                                    "height": "18px",
                                                                    "cursor": "pointer"
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "type": "text",
                                                            "props": {
                                                                "content": "Easy to read (no I, l, 1, O, 0)",
                                                                "style": {
                                                                    "fontSize": "14px",
                                                                    "color": "white",
                                                                    "fontWeight": "500"
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                },
                                
                                # Master toggle
                                {
                                    "type": "label",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "alignItems": "center",
                                            "gap": "10px",
                                            "cursor": "pointer",
                                            "padding": "12px",
                                            "borderRadius": "10px",
                                            "background": "rgba(255,255,255,0.1)",
                                            "border": "2px solid rgba(255,255,255,0.2)",
                                            "marginBottom": "15px",
                                            "transition": "all 0.2s ease",
                                            ":hover": {
                                                "backgroundColor": "rgba(255,255,255,0.15)"
                                            }
                                        },
                                        "children": [
                                            {
                                                "type": "checkbox",
                                                "props": {
                                                    "checked": password_data.get('all_characters', True),
                                                    "action": "toggle_all_characters",
                                                    "style": {
                                                        "width": "20px",
                                                        "height": "20px",
                                                        "cursor": "pointer"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": "All Characters",
                                                    "style": {
                                                        "fontSize": "16px",
                                                        "color": "white",
                                                        "fontWeight": "600"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                
                                # Individual character type checkboxes
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "grid",
                                            "gridTemplateColumns": "1fr 1fr",
                                            "gap": "10px",
                                            "opacity": "0.6" if password_data.get('all_characters', True) else "1",
                                            "transition": "opacity 0.3s ease"
                                        },
                                        "children": [
                                            {
                                                "type": "label",
                                                "props": {
                                                    "style": {
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "gap": "8px",
                                                        "cursor": "pointer",
                                                        "padding": "8px",
                                                        "borderRadius": "8px",
                                                        "transition": "background-color 0.2s ease",
                                                        ":hover": {
                                                            "backgroundColor": "rgba(255,255,255,0.1)"
                                                        }
                                                    },
                                                    "children": [
                                                        {
                                                            "type": "checkbox",
                                                            "props": {
                                                                "checked": password_data.get('uppercase', True),
                                                                "action": "toggle_uppercase",
                                                                "disabled": password_data.get('all_characters', True),
                                                                "style": {
                                                                    "width": "16px",
                                                                    "height": "16px",
                                                                    "cursor": "pointer"
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "type": "text",
                                                            "props": {
                                                                "content": "Uppercase",
                                                                "style": {
                                                                    "fontSize": "14px",
                                                                    "color": "white",
                                                                    "fontWeight": "500"
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                "type": "label",
                                                "props": {
                                                    "style": {
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "gap": "8px",
                                                        "cursor": "pointer",
                                                        "padding": "8px",
                                                        "borderRadius": "8px",
                                                        "transition": "background-color 0.2s ease",
                                                        ":hover": {
                                                            "backgroundColor": "rgba(255,255,255,0.1)"
                                                        }
                                                    },
                                                    "children": [
                                                        {
                                                            "type": "checkbox",
                                                            "props": {
                                                                "checked": password_data.get('lowercase', True),
                                                                "action": "toggle_lowercase",
                                                                "disabled": password_data.get('all_characters', True),
                                                                "style": {
                                                                    "width": "16px",
                                                                    "height": "16px",
                                                                    "cursor": "pointer"
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "type": "text",
                                                            "props": {
                                                                "content": "Lowercase",
                                                                "style": {
                                                                    "fontSize": "14px",
                                                                    "color": "white",
                                                                    "fontWeight": "500"
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                "type": "label",
                                                "props": {
                                                    "style": {
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "gap": "8px",
                                                        "cursor": "pointer",
                                                        "padding": "8px",
                                                        "borderRadius": "8px",
                                                        "transition": "background-color 0.2s ease",
                                                        ":hover": {
                                                            "backgroundColor": "rgba(255,255,255,0.1)"
                                                        }
                                                    },
                                                    "children": [
                                                        {
                                                            "type": "checkbox",
                                                            "props": {
                                                                "checked": password_data.get('numbers', True),
                                                                "action": "toggle_numbers",
                                                                "disabled": password_data.get('all_characters', True),
                                                                "style": {
                                                                    "width": "16px",
                                                                    "height": "16px",
                                                                    "cursor": "pointer"
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "type": "text",
                                                            "props": {
                                                                "content": "Numbers",
                                                                "style": {
                                                                    "fontSize": "14px",
                                                                    "color": "white",
                                                                    "fontWeight": "500"
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                "type": "label",
                                                "props": {
                                                    "style": {
                                                        "display": "flex",
                                                        "alignItems": "center",
                                                        "gap": "8px",
                                                        "cursor": "pointer",
                                                        "padding": "8px",
                                                        "borderRadius": "8px",
                                                        "transition": "background-color 0.2s ease",
                                                        ":hover": {
                                                            "backgroundColor": "rgba(255,255,255,0.1)"
                                                        }
                                                    },
                                                    "children": [
                                                        {
                                                            "type": "checkbox",
                                                            "props": {
                                                                "checked": password_data.get('symbols', True),
                                                                "action": "toggle_symbols",
                                                                "disabled": password_data.get('all_characters', True),
                                                                "style": {
                                                                    "width": "16px",
                                                                    "height": "16px",
                                                                    "cursor": "pointer"
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "type": "text",
                                                            "props": {
                                                                "content": "Symbols",
                                                                "style": {
                                                                    "fontSize": "14px",
                                                                    "color": "white",
                                                                    "fontWeight": "500"
                                                                }
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
                    },
                    
                    # Generate Button
                    {
                        "type": "button",
                        "props": {
                            "label": "🔐 Generate New Password",
                            "action": "generate_password",
                            "style": {
                                "padding": "15px 30px",
                                "backgroundColor": "rgba(255,255,255,0.2)",
                                "color": "white",
                                "border": "2px solid rgba(255,255,255,0.3)",
                                "borderRadius": "12px",
                                "fontSize": "16px",
                                "fontWeight": "700",
                                "cursor": "pointer",
                                "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                                ":hover": {
                                    "backgroundColor": "rgba(255,255,255,0.3)",
                                    "transform": "translateY(-3px)",
                                    "boxShadow": "0 12px 24px rgba(0,0,0,0.2)"
                                },
                                ":active": {
                                    "transform": "translateY(0)",
                                    "boxShadow": "0 6px 12px rgba(0,0,0,0.15)"
                                }
                            }
                        }
                    }
                ]
            }
        }
    
    def _get_password_state(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get the current password state."""
        if ui_state and isinstance(ui_state, dict) and 'password_data' in ui_state:
            return ui_state['password_data']
        return password_state.value

# Register event handler for password generation
@app.event("generate_password")
def handle_generate_password(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle password generation button click.
    
    Args:
        event_data: Event data passed from the frontend
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Generate password event received with data: {event_data}")
    
    # Generate new password
    regenerate_password()
    
    print(f"New password generated: {password_state.value['password']}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for length slider
@app.event("update_length")
def handle_update_length(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle password length slider change.
    
    Args:
        event_data: Event data containing the new length value
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Update length event received with data: {event_data}")
    
    # Extract length value from event data
    new_length = 12  # Default fallback
    if event_data is not None:
        try:
            # Handle new format: event_data is the value directly (float/int)
            if isinstance(event_data, (int, float)):
                new_length = int(event_data)
            # Handle legacy format: event_data is a dict with 'value' key
            elif isinstance(event_data, dict) and 'value' in event_data:
                new_length = int(event_data['value'])
            else:
                print(f"Unexpected event_data format: {type(event_data)} - {repr(event_data)}")
            
            # Ensure length is within valid bounds
            new_length = max(4, min(50, new_length))
        except (ValueError, TypeError) as e:
            print(f"Invalid length value: {event_data}, using default: {new_length}. Error: {e}")
    
    # Update password state
    current_state = password_state.value.copy()
    current_state['length'] = new_length
    current_state['copied'] = False  # Reset copied status
    password_state.set(current_state)
    
    print(f"Length updated to: {new_length}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for easy to say toggle
@app.event("toggle_easy_to_say")
def handle_toggle_easy_to_say(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle easy to say checkbox toggle.
    
    Args:
        event_data: Event data containing the checked state
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Toggle easy to say event received with data: {event_data}")
    
    # Extract checked state from event data
    checked = False
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    # Update password state
    current_state = password_state.value.copy()
    current_state['easy_to_say'] = checked
    current_state['copied'] = False  # Reset copied status
    password_state.set(current_state)
    
    print(f"Easy to say toggled to: {checked}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for easy to read toggle
@app.event("toggle_easy_to_read")
def handle_toggle_easy_to_read(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle easy to read checkbox toggle.
    
    Args:
        event_data: Event data containing the checked state
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Toggle easy to read event received with data: {event_data}")
    
    # Extract checked state from event data
    checked = False
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    # Update password state
    current_state = password_state.value.copy()
    current_state['easy_to_read'] = checked
    current_state['copied'] = False  # Reset copied status
    password_state.set(current_state)
    
    print(f"Easy to read toggled to: {checked}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for all characters master toggle
@app.event("toggle_all_characters")
def handle_toggle_all_characters(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle all characters master toggle with special logic.
    
    When enabled, this disables individual character type toggles.
    When disabled, it enables individual toggles.
    
    Args:
        event_data: Event data containing the checked state
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Toggle all characters event received with data: {event_data}")
    
    # Extract checked state from event data
    checked = True  # Default to true
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    # Update password state with master toggle logic
    current_state = password_state.value.copy()
    current_state['all_characters'] = checked
    current_state['copied'] = False  # Reset copied status
    
    # When all_characters is enabled, ensure all individual toggles are true
    # When disabled, individual toggles become controllable
    if checked:
        current_state['uppercase'] = True
        current_state['lowercase'] = True
        current_state['numbers'] = True
        current_state['symbols'] = True
    
    password_state.set(current_state)
    
    print(f"All characters toggled to: {checked}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for uppercase toggle
@app.event("toggle_uppercase")
def handle_toggle_uppercase(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle uppercase checkbox toggle.
    
    Args:
        event_data: Event data containing the checked state
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Toggle uppercase event received with data: {event_data}")
    
    # Extract checked state from event data
    checked = True  # Default to true
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    # Update password state
    current_state = password_state.value.copy()
    current_state['uppercase'] = checked
    current_state['copied'] = False  # Reset copied status
    password_state.set(current_state)
    
    print(f"Uppercase toggled to: {checked}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for lowercase toggle
@app.event("toggle_lowercase")
def handle_toggle_lowercase(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle lowercase checkbox toggle.
    
    Args:
        event_data: Event data containing the checked state
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Toggle lowercase event received with data: {event_data}")
    
    # Extract checked state from event data
    checked = True  # Default to true
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    # Update password state
    current_state = password_state.value.copy()
    current_state['lowercase'] = checked
    current_state['copied'] = False  # Reset copied status
    password_state.set(current_state)
    
    print(f"Lowercase toggled to: {checked}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for numbers toggle
@app.event("toggle_numbers")
def handle_toggle_numbers(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle numbers checkbox toggle.
    
    Args:
        event_data: Event data containing the checked state
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Toggle numbers event received with data: {event_data}")
    
    # Extract checked state from event data
    checked = True  # Default to true
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    # Update password state
    current_state = password_state.value.copy()
    current_state['numbers'] = checked
    current_state['copied'] = False  # Reset copied status
    password_state.set(current_state)
    
    print(f"Numbers toggled to: {checked}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for symbols toggle
@app.event("toggle_symbols")
def handle_toggle_symbols(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle symbols checkbox toggle.
    
    Args:
        event_data: Event data containing the checked state
        
    Returns:
        Dict[str, Any]: Response with updated password data
    """
    print(f"Toggle symbols event received with data: {event_data}")
    
    # Extract checked state from event data
    checked = True  # Default to true
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    # Update password state
    current_state = password_state.value.copy()
    current_state['symbols'] = checked
    current_state['copied'] = False  # Reset copied status
    password_state.set(current_state)
    
    print(f"Symbols toggled to: {checked}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

# Event handler for copy password functionality
@app.event("copy_password")
def handle_copy_password(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle copy password button click.
    
    Sets the copied status to True to show the "Copied!" indicator.
    
    Args:
        event_data: Event data from the copy button
        
    Returns:
        Dict[str, Any]: Response with updated password data showing copied status
    """
    print(f"Copy password event received with data: {event_data}")
    
    # Update password state to show copied status
    current_state = password_state.value.copy()
    current_state['copied'] = True
    password_state.set(current_state)
    
    print(f"Password copied: {current_state['password']}")
    
    # Return updated state
    return {
        "password_data": password_state.value
    }

@app.mix("/")
def home() -> Dict[str, Any]:
    """Main page with password generator."""
    # Initialize password if empty
    if not password_state.value['password']:
        regenerate_password()
    
    password_component = PasswordGenerator()
    
    return {
        "type": "div",
        "props": {
            "style": {
                "minHeight": "100vh",
                "background": "linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%)",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "padding": "40px 20px",
                "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Cacao Password Generator",
                    "style": {
                        "fontSize": "48px",
                        "fontWeight": "800",
                        "color": "#ecf0f1",
                        "textAlign": "center",
                        "marginBottom": "50px",
                        "textShadow": "0 2px 4px rgba(0,0,0,0.3)",
                        "letterSpacing": "-1px"
                    }
                }
            },
            password_component.render()
        ]
    }

if __name__ == "__main__":
    app.brew()  # Run the app like brewing hot chocolate!