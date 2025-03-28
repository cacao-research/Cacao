"""
Cacao Color Picker Example

Demonstrates:
- Reactive state management
- Component-based UI
- Interactive color selection
"""

from cacao import mix, State, Component
import colorsys

# Reactive state for color values
red = State(0)
green = State(0)
blue = State(0)
hue = State(0)
saturation = State(0)
value = State(0)

class ColorPicker(Component):
    def render(self):
        # Calculate hex color
        r, g, b = int(red.value), int(green.value), int(blue.value)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # HSV values
        h, s, v = hue.value / 360, saturation.value / 100, value.value / 100
        
        return {
            "type": "section",
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {
                            "content": f"Color: {hex_color}",
                            "style": {
                                "color": hex_color,
                                "font-weight": "bold"
                            }
                        }
                    },
                    {
                        "type": "section",
                        "props": {
                            "children": [
                                # RGB Sliders
                                {"type": "slider", "props": {
                                    "label": "Red",
                                    "min": 0,
                                    "max": 255,
                                    "value": red.value,
                                    "onChange": lambda v: red.set(v)
                                }},
                                {"type": "slider", "props": {
                                    "label": "Green", 
                                    "min": 0,
                                    "max": 255,
                                    "value": green.value,
                                    "onChange": lambda v: green.set(v)
                                }},
                                {"type": "slider", "props": {
                                    "label": "Blue",
                                    "min": 0,
                                    "max": 255,
                                    "value": blue.value,
                                    "onChange": lambda v: blue.set(v)
                                }}
                            ]
                        }
                    },
                    {
                        "type": "section",
                        "props": {
                            "children": [
                                # HSV Sliders
                                {"type": "slider", "props": {
                                    "label": "Hue",
                                    "min": 0,
                                    "max": 360,
                                    "value": hue.value,
                                    "onChange": lambda v: hue.set(v)
                                }},
                                {"type": "slider", "props": {
                                    "label": "Saturation",
                                    "min": 0,
                                    "max": 100,
                                    "value": saturation.value,
                                    "onChange": lambda v: saturation.set(v)
                                }},
                                {"type": "slider", "props": {
                                    "label": "Value",
                                    "min": 0,
                                    "max": 100,
                                    "value": value.value,
                                    "onChange": lambda v: value.set(v)
                                }}
                            ]
                        }
                    },
                    {
                        "type": "section",
                        "props": {
                            "style": {
                                "width": "200px",
                                "height": "200px",
                                "background-color": hex_color,
                                "margin": "20px auto"
                            }
                        }
                    }
                ]
            }
        }

# Route for the color picker
@mix("/")
def color_picker_route():
    return {
        "layout": "column",
        "children": [
            {
                "type": "navbar",
                "props": {
                    "brand": "Cacao Color Picker",
                    "links": [
                        {"name": "Home", "url": "/"}
                    ]
                }
            },
            ColorPicker(),
            {
                "type": "footer",
                "props": {"text": "© 2025 Cacao Framework"}
            }
        ]
    }

# Optional: Add state conversion methods
def rgb_to_hsv():
    """Convert RGB to HSV when RGB values change"""
    r, g, b = red.value / 255, green.value / 255, blue.value / 255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    hue.set(h * 360)
    saturation.set(s * 100)
    value.set(v * 100)

def hsv_to_rgb():
    """Convert HSV to RGB when HSV values change"""
    h = hue.value / 360
    s = saturation.value / 100
    v = value.value / 100
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    red.set(int(r * 255))
    green.set(int(g * 255))
    blue.set(int(b * 255))

# Subscribe to state changes for conversion
red.subscribe(rgb_to_hsv)
green.subscribe(rgb_to_hsv)
blue.subscribe(rgb_to_hsv)
hue.subscribe(hsv_to_rgb)
saturation.subscribe(hsv_to_rgb)
value.subscribe(hsv_to_rgb)
