"""Converter tools - colors, case, number bases."""

import re
from cacao.core.state import State

# Color converter state
color_input = State("#8B4513")
color_results = State({"hex": "#8B4513", "rgb": "rgb(139, 69, 19)", "hsl": "hsl(25, 76%, 31%)"})

# Case converter state
case_input = State("")
case_results = State({})

# Number base state
num_input = State("")
num_base = State("10")
num_results = State({})


def color_converter():
    """Convert between color formats."""
    return {
        "type": "div",
        "props": {
            "className": "tool-container",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "tool-header",
                        "children": [
                            {"type": "h2", "props": {"content": "Color Converter"}},
                            {"type": "p", "props": {"content": "Convert between HEX, RGB, and HSL color formats"}}
                        ]
                    }
                },
                {
                    "type": "div",
                    "props": {
                        "className": "tool-body",
                        "children": [
                            {
                                "type": "div",
                                "props": {
                                    "className": "color-input-group",
                                    "children": [
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "color",
                                                "value": color_input.value if color_input.value.startswith("#") else "#000000",
                                                "onChange": "color:picker",
                                                "className": "color-picker"
                                            }
                                        },
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "text",
                                                "value": color_input.value,
                                                "onChange": "color:input",
                                                "placeholder": "#8B4513 or rgb(139,69,19)",
                                                "className": "tool-input"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "color-preview",
                                    "style": {"backgroundColor": color_results.value.get("hex", "#000")}
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "color-results",
                                    "children": [
                                        _color_result_row("HEX", color_results.value.get("hex", "")),
                                        _color_result_row("RGB", color_results.value.get("rgb", "")),
                                        _color_result_row("HSL", color_results.value.get("hsl", "")),
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def _color_result_row(label: str, value: str):
    """Render a color result row."""
    return {
        "type": "div",
        "props": {
            "className": "result-row",
            "children": [
                {"type": "label", "props": {"content": label, "className": "result-label"}},
                {
                    "type": "input",
                    "props": {
                        "type": "text",
                        "value": value,
                        "readOnly": True,
                        "className": "result-value"
                    }
                },
                {
                    "type": "button",
                    "props": {
                        "content": "Copy",
                        "onClick": f"copy:{value}",
                        "className": "btn btn-sm"
                    }
                }
            ]
        }
    }


def case_converter():
    """Convert text between different cases."""
    return {
        "type": "div",
        "props": {
            "className": "tool-container",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "tool-header",
                        "children": [
                            {"type": "h2", "props": {"content": "Case Converter"}},
                            {"type": "p", "props": {"content": "Convert text between camelCase, snake_case, kebab-case, and more"}}
                        ]
                    }
                },
                {
                    "type": "div",
                    "props": {
                        "className": "tool-body",
                        "children": [
                            {
                                "type": "textarea",
                                "props": {
                                    "placeholder": "Enter text to convert (e.g., 'hello world' or 'helloWorld')",
                                    "value": case_input.value,
                                    "onChange": "case:input",
                                    "className": "tool-input",
                                    "rows": 2
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "case-results",
                                    "children": [
                                        _case_result_row("camelCase", case_results.value.get("camel", "")),
                                        _case_result_row("PascalCase", case_results.value.get("pascal", "")),
                                        _case_result_row("snake_case", case_results.value.get("snake", "")),
                                        _case_result_row("CONSTANT_CASE", case_results.value.get("constant", "")),
                                        _case_result_row("kebab-case", case_results.value.get("kebab", "")),
                                        _case_result_row("Title Case", case_results.value.get("title", "")),
                                        _case_result_row("UPPERCASE", case_results.value.get("upper", "")),
                                        _case_result_row("lowercase", case_results.value.get("lower", "")),
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def _case_result_row(label: str, value: str):
    """Render a case result row."""
    return {
        "type": "div",
        "props": {
            "className": "result-row",
            "children": [
                {"type": "label", "props": {"content": label, "className": "result-label"}},
                {
                    "type": "input",
                    "props": {
                        "type": "text",
                        "value": value,
                        "readOnly": True,
                        "className": "result-value"
                    }
                },
                {
                    "type": "button",
                    "props": {
                        "content": "Copy",
                        "onClick": f"copy:{value}",
                        "className": "btn btn-sm"
                    }
                }
            ]
        }
    }


def number_base_converter():
    """Convert numbers between different bases."""
    return {
        "type": "div",
        "props": {
            "className": "tool-container",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "tool-header",
                        "children": [
                            {"type": "h2", "props": {"content": "Number Base Converter"}},
                            {"type": "p", "props": {"content": "Convert between binary, octal, decimal, and hexadecimal"}}
                        ]
                    }
                },
                {
                    "type": "div",
                    "props": {
                        "className": "tool-body",
                        "children": [
                            {
                                "type": "div",
                                "props": {
                                    "className": "input-group",
                                    "children": [
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "text",
                                                "placeholder": "Enter a number",
                                                "value": num_input.value,
                                                "onChange": "num:input",
                                                "className": "tool-input"
                                            }
                                        },
                                        {
                                            "type": "select",
                                            "props": {
                                                "value": num_base.value,
                                                "onChange": "num:base",
                                                "children": [
                                                    {"type": "option", "props": {"value": "2", "content": "Binary (base 2)"}},
                                                    {"type": "option", "props": {"value": "8", "content": "Octal (base 8)"}},
                                                    {"type": "option", "props": {"value": "10", "content": "Decimal (base 10)"}},
                                                    {"type": "option", "props": {"value": "16", "content": "Hex (base 16)"}},
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "num-results",
                                    "children": [
                                        _num_result_row("Binary", num_results.value.get("bin", ""), "0b"),
                                        _num_result_row("Octal", num_results.value.get("oct", ""), "0o"),
                                        _num_result_row("Decimal", num_results.value.get("dec", ""), ""),
                                        _num_result_row("Hexadecimal", num_results.value.get("hex", ""), "0x"),
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def _num_result_row(label: str, value: str, prefix: str):
    """Render a number result row."""
    display_value = f"{prefix}{value}" if value else ""
    return {
        "type": "div",
        "props": {
            "className": "result-row",
            "children": [
                {"type": "label", "props": {"content": label, "className": "result-label"}},
                {
                    "type": "input",
                    "props": {
                        "type": "text",
                        "value": display_value,
                        "readOnly": True,
                        "className": "result-value mono"
                    }
                },
                {
                    "type": "button",
                    "props": {
                        "content": "Copy",
                        "onClick": f"copy:{display_value}",
                        "className": "btn btn-sm"
                    }
                }
            ]
        }
    }


# Utility functions
def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """Convert RGB to HSL."""
    r, g, b = r / 255, g / 255, b / 255
    max_c, min_c = max(r, g, b), min(r, g, b)
    l = (max_c + min_c) / 2

    if max_c == min_c:
        h = s = 0
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        if max_c == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return (round(h * 360), round(s * 100), round(l * 100))


def to_words(text: str) -> list:
    """Split text into words handling various cases."""
    # Handle camelCase and PascalCase
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Handle snake_case and kebab-case
    text = re.sub(r'[_-]', ' ', text)
    return text.lower().split()


def to_camel(words: list) -> str:
    """Convert words to camelCase."""
    if not words:
        return ""
    return words[0] + ''.join(w.capitalize() for w in words[1:])


def to_pascal(words: list) -> str:
    """Convert words to PascalCase."""
    return ''.join(w.capitalize() for w in words)


def to_snake(words: list) -> str:
    """Convert words to snake_case."""
    return '_'.join(words)


def to_constant(words: list) -> str:
    """Convert words to CONSTANT_CASE."""
    return '_'.join(w.upper() for w in words)


def to_kebab(words: list) -> str:
    """Convert words to kebab-case."""
    return '-'.join(words)


def to_title(words: list) -> str:
    """Convert words to Title Case."""
    return ' '.join(w.capitalize() for w in words)


def convert_all_cases(text: str) -> dict:
    """Convert text to all case formats."""
    words = to_words(text)
    return {
        "camel": to_camel(words),
        "pascal": to_pascal(words),
        "snake": to_snake(words),
        "constant": to_constant(words),
        "kebab": to_kebab(words),
        "title": to_title(words),
        "upper": text.upper(),
        "lower": text.lower(),
    }


def convert_number_base(value: str, from_base: int) -> dict:
    """Convert number to all bases."""
    try:
        decimal = int(value, from_base)
        return {
            "bin": bin(decimal)[2:],
            "oct": oct(decimal)[2:],
            "dec": str(decimal),
            "hex": hex(decimal)[2:].upper(),
        }
    except ValueError:
        return {"bin": "", "oct": "", "dec": "", "hex": ""}
