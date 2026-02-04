"""Converter tools - colors, case, number bases."""

import re
from cacao.core.state import State
from cacao.ui import (
    div, h2, p, textarea, select, input,
    result_row, tool_container, labeled
)

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
    hex_val = color_input.value if color_input.value.startswith("#") else "#000000"

    return tool_container(
        "Color Converter",
        "Convert between HEX, RGB, and HSL color formats",
        div(
            input(type="color", value=hex_val, onChange="color:picker", className="color-picker"),
            input(
                value=color_input.value,
                onChange="color:input",
                placeholder="#8B4513 or rgb(139,69,19)",
                className="tool-input"
            ),
            className="color-input-group"
        ),
        div(className="color-preview", style={"backgroundColor": color_results.value.get("hex", "#000")}),
        div(
            result_row("HEX", color_results.value.get("hex", "")),
            result_row("RGB", color_results.value.get("rgb", "")),
            result_row("HSL", color_results.value.get("hsl", "")),
            className="color-results"
        )
    )


def case_converter():
    """Convert text between different cases."""
    return tool_container(
        "Case Converter",
        "Convert text between camelCase, snake_case, kebab-case, and more",
        textarea(
            value=case_input.value,
            onChange="case:input",
            placeholder="Enter text to convert (e.g., 'hello world' or 'helloWorld')",
            className="tool-input",
            rows=2
        ),
        div(
            result_row("camelCase", case_results.value.get("camel", "")),
            result_row("PascalCase", case_results.value.get("pascal", "")),
            result_row("snake_case", case_results.value.get("snake", "")),
            result_row("CONSTANT_CASE", case_results.value.get("constant", "")),
            result_row("kebab-case", case_results.value.get("kebab", "")),
            result_row("Title Case", case_results.value.get("title", "")),
            result_row("UPPERCASE", case_results.value.get("upper", "")),
            result_row("lowercase", case_results.value.get("lower", "")),
            className="case-results"
        )
    )


def _num_result_row(label: str, value: str, prefix: str):
    """Render a number result row with prefix."""
    display = f"{prefix}{value}" if value else ""
    return result_row(label, display)


def number_base_converter():
    """Convert numbers between different bases."""
    return tool_container(
        "Number Base Converter",
        "Convert between binary, octal, decimal, and hexadecimal",
        div(
            input(
                value=num_input.value,
                onChange="num:input",
                placeholder="Enter a number",
                className="tool-input"
            ),
            select(
                value=num_base.value,
                onChange="num:base",
                options=[
                    ("2", "Binary (base 2)"),
                    ("8", "Octal (base 8)"),
                    ("10", "Decimal (base 10)"),
                    ("16", "Hex (base 16)")
                ]
            ),
            className="input-group"
        ),
        div(
            _num_result_row("Binary", num_results.value.get("bin", ""), "0b"),
            _num_result_row("Octal", num_results.value.get("oct", ""), "0o"),
            _num_result_row("Decimal", num_results.value.get("dec", ""), ""),
            _num_result_row("Hexadecimal", num_results.value.get("hex", ""), "0x"),
            className="num-results"
        )
    )


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
