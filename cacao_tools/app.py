"""
Cacao Tools - A collection of developer utilities
Inspired by IT-Tools (https://it-tools.tech)
Built with Cacao Framework
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cacao import App
from cacao.core.state import State

# Import tool categories
from cacao_tools.tools import crypto, converters, generators, encoders, text

app = App()

# Global state
current_tool = State("home")

# Tool registry - maps tool IDs to their render functions
TOOLS = {
    # Crypto
    "hash-text": crypto.hash_text,
    "uuid-generator": crypto.uuid_generator,
    "password-generator": crypto.password_generator,

    # Converters
    "color-converter": converters.color_converter,
    "case-converter": converters.case_converter,
    "number-base": converters.number_base_converter,

    # Encoders/Decoders
    "base64": encoders.base64_tool,
    "url-encode": encoders.url_encode_tool,
    "jwt-decode": encoders.jwt_decode_tool,

    # Generators
    "lorem-ipsum": generators.lorem_ipsum,
    "qr-code": generators.qr_code,

    # Text
    "text-diff": text.text_diff,
    "regex-tester": text.regex_tester,
    "word-counter": text.word_counter,
}

# Navigation structure
NAV_ITEMS = [
    {
        "category": "Crypto",
        "icon": "fa-solid fa-lock",
        "tools": [
            {"id": "hash-text", "name": "Hash Text", "desc": "MD5, SHA1, SHA256, SHA512"},
            {"id": "uuid-generator", "name": "UUID Generator", "desc": "Generate UUIDs v1/v4"},
            {"id": "password-generator", "name": "Password Generator", "desc": "Secure random passwords"},
        ]
    },
    {
        "category": "Converters",
        "icon": "fa-solid fa-arrows-rotate",
        "tools": [
            {"id": "color-converter", "name": "Color Converter", "desc": "HEX, RGB, HSL"},
            {"id": "case-converter", "name": "Case Converter", "desc": "camelCase, snake_case, etc."},
            {"id": "number-base", "name": "Number Base", "desc": "Binary, Hex, Decimal, Octal"},
        ]
    },
    {
        "category": "Encoders",
        "icon": "fa-solid fa-code",
        "tools": [
            {"id": "base64", "name": "Base64", "desc": "Encode/Decode Base64"},
            {"id": "url-encode", "name": "URL Encode", "desc": "Encode/Decode URLs"},
            {"id": "jwt-decode", "name": "JWT Decode", "desc": "Decode JWT tokens"},
        ]
    },
    {
        "category": "Generators",
        "icon": "fa-solid fa-wand-magic-sparkles",
        "tools": [
            {"id": "lorem-ipsum", "name": "Lorem Ipsum", "desc": "Generate placeholder text"},
            {"id": "qr-code", "name": "QR Code", "desc": "Generate QR codes"},
        ]
    },
    {
        "category": "Text",
        "icon": "fa-solid fa-font",
        "tools": [
            {"id": "text-diff", "name": "Text Diff", "desc": "Compare two texts"},
            {"id": "regex-tester", "name": "Regex Tester", "desc": "Test regular expressions"},
            {"id": "word-counter", "name": "Word Counter", "desc": "Count words, chars, lines"},
        ]
    },
]


def render_sidebar():
    """Render the sidebar navigation."""
    nav_children = []

    for category in NAV_ITEMS:
        # Category header
        nav_children.append({
            "type": "div",
            "props": {
                "className": "nav-category",
                "children": [
                    {
                        "type": "i",
                        "props": {"className": category["icon"]}
                    },
                    {
                        "type": "span",
                        "props": {"content": category["category"]}
                    }
                ]
            }
        })

        # Tools in category
        for tool in category["tools"]:
            is_active = current_tool.value == tool["id"]
            nav_children.append({
                "type": "div",
                "props": {
                    "className": f"nav-item {'active' if is_active else ''}",
                    "onClick": f"navigate:{tool['id']}",
                    "children": [
                        {
                            "type": "span",
                            "props": {
                                "className": "nav-item-name",
                                "content": tool["name"]
                            }
                        }
                    ]
                }
            })

    return {
        "type": "aside",
        "props": {
            "className": "tools-sidebar",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "sidebar-header",
                        "children": [
                            {
                                "type": "h1",
                                "props": {
                                    "content": "Cacao Tools",
                                    "className": "logo"
                                }
                            },
                            {
                                "type": "p",
                                "props": {
                                    "content": "Developer Utilities",
                                    "className": "tagline"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "nav",
                    "props": {
                        "className": "tools-nav",
                        "children": nav_children
                    }
                }
            ]
        }
    }


def render_home():
    """Render the home/welcome page."""
    tool_cards = []

    for category in NAV_ITEMS:
        for tool in category["tools"]:
            tool_cards.append({
                "type": "div",
                "props": {
                    "className": "tool-card",
                    "onClick": f"navigate:{tool['id']}",
                    "children": [
                        {
                            "type": "i",
                            "props": {"className": f"{category['icon']} tool-card-icon"}
                        },
                        {
                            "type": "h3",
                            "props": {"content": tool["name"]}
                        },
                        {
                            "type": "p",
                            "props": {"content": tool["desc"]}
                        }
                    ]
                }
            })

    return {
        "type": "div",
        "props": {
            "className": "home-content",
            "children": [
                {
                    "type": "div",
                    "props": {
                        "className": "home-header",
                        "children": [
                            {
                                "type": "h1",
                                "props": {"content": "Welcome to Cacao Tools"}
                            },
                            {
                                "type": "p",
                                "props": {
                                    "content": "A collection of handy utilities for developers. Select a tool from the sidebar or click on a card below."
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "div",
                    "props": {
                        "className": "tools-grid",
                        "children": tool_cards
                    }
                }
            ]
        }
    }


def render_content():
    """Render the main content area."""
    tool_id = current_tool.value

    if tool_id == "home" or tool_id not in TOOLS:
        return render_home()

    # Get the tool's render function and call it
    tool_render = TOOLS[tool_id]
    return tool_render()


@app.mix("/")
def index():
    """Main application layout."""
    return {
        "type": "div",
        "props": {
            "className": "tools-app",
            "children": [
                render_sidebar(),
                {
                    "type": "main",
                    "props": {
                        "className": "tools-main",
                        "children": [render_content()]
                    }
                }
            ]
        }
    }


# ============================================
# Event Handlers
# ============================================

@app.event("navigate")
async def handle_navigate(data):
    """Handle navigation between tools."""
    tool_id = data.get("value", "home")
    current_tool.set(tool_id)


# --- Crypto Events ---

@app.event("hash:input")
async def handle_hash_input(data):
    """Handle hash input change."""
    crypto.hash_input.set(data.get("value", ""))


@app.event("hash:generate")
async def handle_hash_generate(data):
    """Generate hashes."""
    text = crypto.hash_input.value
    if text:
        results = crypto.generate_hashes(text)
        crypto.hash_results.set(results)


@app.event("uuid:version")
async def handle_uuid_version(data):
    """Handle UUID version change."""
    crypto.uuid_version.set(data.get("value", "4"))


@app.event("uuid:generate")
async def handle_uuid_generate(data):
    """Generate UUID."""
    version = crypto.uuid_version.value
    result = crypto.generate_uuid(version)
    crypto.uuid_result.set(result)


@app.event("pwd:length")
async def handle_pwd_length(data):
    """Handle password length change."""
    crypto.pwd_length.set(int(data.get("value", 16)))


@app.event("pwd:upper")
async def handle_pwd_upper(data):
    """Toggle uppercase."""
    crypto.pwd_include_upper.set(data.get("checked", True))


@app.event("pwd:lower")
async def handle_pwd_lower(data):
    """Toggle lowercase."""
    crypto.pwd_include_lower.set(data.get("checked", True))


@app.event("pwd:digits")
async def handle_pwd_digits(data):
    """Toggle digits."""
    crypto.pwd_include_digits.set(data.get("checked", True))


@app.event("pwd:symbols")
async def handle_pwd_symbols(data):
    """Toggle symbols."""
    crypto.pwd_include_symbols.set(data.get("checked", True))


@app.event("pwd:generate")
async def handle_pwd_generate(data):
    """Generate password."""
    result = crypto.generate_password(
        crypto.pwd_length.value,
        crypto.pwd_include_upper.value,
        crypto.pwd_include_lower.value,
        crypto.pwd_include_digits.value,
        crypto.pwd_include_symbols.value
    )
    crypto.pwd_result.set(result)


# --- Converter Events ---

@app.event("color:picker")
@app.event("color:input")
async def handle_color_input(data):
    """Handle color input change."""
    value = data.get("value", "")
    converters.color_input.set(value)

    # Try to parse and convert
    try:
        if value.startswith("#") and len(value) == 7:
            r, g, b = converters.hex_to_rgb(value)
            h, s, l = converters.rgb_to_hsl(r, g, b)
            converters.color_results.set({
                "hex": value.upper(),
                "rgb": f"rgb({r}, {g}, {b})",
                "hsl": f"hsl({h}, {s}%, {l}%)"
            })
    except Exception:
        pass


@app.event("case:input")
async def handle_case_input(data):
    """Handle case converter input."""
    value = data.get("value", "")
    converters.case_input.set(value)

    if value:
        results = converters.convert_all_cases(value)
        converters.case_results.set(results)
    else:
        converters.case_results.set({})


@app.event("num:input")
async def handle_num_input(data):
    """Handle number input."""
    converters.num_input.set(data.get("value", ""))
    _update_number_conversion()


@app.event("num:base")
async def handle_num_base(data):
    """Handle base change."""
    converters.num_base.set(data.get("value", "10"))
    _update_number_conversion()


def _update_number_conversion():
    """Update number conversion results."""
    value = converters.num_input.value
    base = int(converters.num_base.value)
    if value:
        results = converters.convert_number_base(value, base)
        converters.num_results.set(results)
    else:
        converters.num_results.set({})


# --- Encoder Events ---

@app.event("b64:mode:encode")
async def handle_b64_mode_encode(data):
    """Set Base64 mode to encode."""
    encoders.b64_mode.set("encode")
    _update_b64()


@app.event("b64:mode:decode")
async def handle_b64_mode_decode(data):
    """Set Base64 mode to decode."""
    encoders.b64_mode.set("decode")
    _update_b64()


@app.event("b64:input")
async def handle_b64_input(data):
    """Handle Base64 input change."""
    encoders.b64_input.set(data.get("value", ""))
    _update_b64()


def _update_b64():
    """Update Base64 output."""
    input_val = encoders.b64_input.value
    if encoders.b64_mode.value == "encode":
        encoders.b64_output.set(encoders.encode_base64(input_val))
    else:
        encoders.b64_output.set(encoders.decode_base64(input_val))


@app.event("url:mode:encode")
async def handle_url_mode_encode(data):
    """Set URL mode to encode."""
    encoders.url_mode.set("encode")
    _update_url()


@app.event("url:mode:decode")
async def handle_url_mode_decode(data):
    """Set URL mode to decode."""
    encoders.url_mode.set("decode")
    _update_url()


@app.event("url:input")
async def handle_url_input(data):
    """Handle URL input change."""
    encoders.url_input.set(data.get("value", ""))
    _update_url()


def _update_url():
    """Update URL output."""
    input_val = encoders.url_input.value
    if encoders.url_mode.value == "encode":
        encoders.url_output.set(encoders.encode_url(input_val))
    else:
        encoders.url_output.set(encoders.decode_url(input_val))


@app.event("jwt:input")
async def handle_jwt_input(data):
    """Handle JWT input change."""
    token = data.get("value", "")
    encoders.jwt_input.set(token)

    if token:
        header, payload, valid = encoders.decode_jwt(token)
        encoders.jwt_header.set(header)
        encoders.jwt_payload.set(payload)
        encoders.jwt_valid.set(valid)
    else:
        encoders.jwt_header.set({})
        encoders.jwt_payload.set({})
        encoders.jwt_valid.set(True)


# --- Generator Events ---

@app.event("lorem:paragraphs")
async def handle_lorem_paragraphs(data):
    """Handle lorem ipsum paragraph count change."""
    generators.lorem_paragraphs.set(int(data.get("value", 3)))


@app.event("lorem:generate")
async def handle_lorem_generate(data):
    """Generate lorem ipsum text."""
    result = generators.generate_lorem(generators.lorem_paragraphs.value)
    generators.lorem_output.set(result)


@app.event("qr:input")
async def handle_qr_input(data):
    """Handle QR code input change."""
    generators.qr_input.set(data.get("value", ""))


@app.event("qr:size")
async def handle_qr_size(data):
    """Handle QR code size change."""
    generators.qr_size.set(int(data.get("value", 200)))


# --- Text Events ---

@app.event("diff:text1")
async def handle_diff_text1(data):
    """Handle diff text 1 change."""
    text.diff_text1.set(data.get("value", ""))


@app.event("diff:text2")
async def handle_diff_text2(data):
    """Handle diff text 2 change."""
    text.diff_text2.set(data.get("value", ""))


@app.event("diff:compare")
async def handle_diff_compare(data):
    """Compare texts."""
    result = text.simple_diff(text.diff_text1.value, text.diff_text2.value)
    text.diff_result.set(result)


@app.event("regex:pattern")
async def handle_regex_pattern(data):
    """Handle regex pattern change."""
    text.regex_pattern.set(data.get("value", ""))
    _update_regex()


@app.event("regex:text")
async def handle_regex_text(data):
    """Handle regex test text change."""
    text.regex_text.set(data.get("value", ""))
    _update_regex()


@app.event("regex:flag:i")
async def handle_regex_flag_i(data):
    """Toggle case insensitive flag."""
    flags = text.regex_flags.value.copy()
    flags["i"] = data.get("checked", False)
    text.regex_flags.set(flags)
    _update_regex()


@app.event("regex:flag:m")
async def handle_regex_flag_m(data):
    """Toggle multiline flag."""
    flags = text.regex_flags.value.copy()
    flags["m"] = data.get("checked", False)
    text.regex_flags.set(flags)
    _update_regex()


@app.event("regex:flag:g")
async def handle_regex_flag_g(data):
    """Toggle global flag."""
    flags = text.regex_flags.value.copy()
    flags["g"] = data.get("checked", True)
    text.regex_flags.set(flags)
    _update_regex()


def _update_regex():
    """Update regex matches."""
    pattern = text.regex_pattern.value
    test_text = text.regex_text.value
    flags = text.regex_flags.value

    if pattern and test_text:
        matches = text.test_regex(pattern, test_text, flags)
        text.regex_matches.set(matches)
    else:
        text.regex_matches.set([])


@app.event("wc:input")
async def handle_wc_input(data):
    """Handle word counter input change."""
    value = data.get("value", "")
    text.wc_input.set(value)
    stats = text.count_text(value)
    text.wc_stats.set(stats)


@app.event("copy")
async def handle_copy(data):
    """Handle copy to clipboard (client-side will handle actual copy)."""
    # This is handled client-side via JavaScript
    pass


if __name__ == "__main__":
    app.brew(
        type="web",
        title="Cacao Tools",
        ASCII_debug=True,  # Windows compatibility
        css_files=["cacao_tools/static/tools.css"],
        theme={
            "colors": {
                "primary": "#8B4513",
                "background": "#1a1a2e",
                "sidebar_bg": "#16213e",
                "content_bg": "#1a1a2e",
                "card_bg": "#0f3460",
                "text": "#eaeaea",
                "text_secondary": "#a0a0a0"
            }
        }
    )
