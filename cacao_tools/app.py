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
from cacao.ui import div, span, h1, h3, p, aside, nav, main, icon

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


# ============================================
# UI Rendering
# ============================================

def render_sidebar():
    """Render the sidebar navigation."""
    nav_children = []

    for category in NAV_ITEMS:
        # Category header
        nav_children.append(
            div(icon(category["icon"]), span(category["category"]), className="nav-category")
        )
        # Tools in category
        for tool in category["tools"]:
            is_active = current_tool.value == tool["id"]
            nav_children.append(
                div(
                    span(tool["name"], className="nav-item-name"),
                    className=f"nav-item {'active' if is_active else ''}",
                    onClick=f"navigate:{tool['id']}"
                )
            )

    return aside(
        div(
            h1("Cacao Tools", className="logo"),
            p("Developer Utilities", className="tagline"),
            className="sidebar-header"
        ),
        nav(*nav_children, className="tools-nav"),
        className="tools-sidebar"
    )


def render_home():
    """Render the home/welcome page."""
    tool_cards = []

    for category in NAV_ITEMS:
        for tool in category["tools"]:
            tool_cards.append(
                div(
                    icon(f"{category['icon']} tool-card-icon"),
                    h3(tool["name"]),
                    p(tool["desc"]),
                    className="tool-card",
                    onClick=f"navigate:{tool['id']}"
                )
            )

    return div(
        div(
            h1("Welcome to Cacao Tools"),
            p("A collection of handy utilities for developers. Select a tool from the sidebar or click on a card below."),
            className="home-header"
        ),
        div(*tool_cards, className="tools-grid"),
        className="home-content"
    )


def render_content():
    """Render the main content area."""
    tool_id = current_tool.value
    if tool_id == "home" or tool_id not in TOOLS:
        return render_home()
    return TOOLS[tool_id]()


@app.mix("/")
def index():
    """Main application layout."""
    return div(
        render_sidebar(),
        main(render_content(), className="tools-main"),
        className="tools-app"
    )


# ============================================
# Event Bindings (using new bind_input API)
# ============================================

# Navigation
app.bind_input("navigate", current_tool)

# --- Crypto ---
app.bind_input("hash:input", crypto.hash_input)
app.bind_input("uuid:version", crypto.uuid_version)
app.bind_input("pwd:length", crypto.pwd_length, cast=int)
app.bind_toggle("pwd:upper", crypto.pwd_include_upper)
app.bind_toggle("pwd:lower", crypto.pwd_include_lower)
app.bind_toggle("pwd:digits", crypto.pwd_include_digits)
app.bind_toggle("pwd:symbols", crypto.pwd_include_symbols)

# --- Converters ---
app.bind_input("color:input", converters.color_input)
app.bind_input("color:picker", converters.color_input)
app.bind_input("case:input", converters.case_input)
app.bind_input("num:input", converters.num_input)
app.bind_input("num:base", converters.num_base)

# --- Encoders ---
app.bind_input("b64:input", encoders.b64_input)
app.bind_input("url:input", encoders.url_input)
app.bind_input("jwt:input", encoders.jwt_input)

# --- Generators ---
app.bind_input("lorem:paragraphs", generators.lorem_paragraphs, cast=int)
app.bind_input("qr:input", generators.qr_input)
app.bind_input("qr:size", generators.qr_size, cast=int)

# --- Text ---
app.bind_input("diff:text1", text.diff_text1)
app.bind_input("diff:text2", text.diff_text2)
app.bind_input("regex:pattern", text.regex_pattern)
app.bind_input("regex:text", text.regex_text)
app.bind_input("wc:input", text.wc_input)


# ============================================
# Custom Event Handlers (for logic that can't be auto-bound)
# ============================================

@app.event("hash:generate")
async def handle_hash_generate(data):
    """Generate hashes from input text."""
    input_text = crypto.hash_input.value
    if input_text:
        crypto.hash_results.set(crypto.generate_hashes(input_text))


@app.event("uuid:generate")
async def handle_uuid_generate(data):
    """Generate UUID based on selected version."""
    crypto.uuid_result.set(crypto.generate_uuid(crypto.uuid_version.value))


@app.event("pwd:generate")
async def handle_pwd_generate(data):
    """Generate password with current settings."""
    crypto.pwd_result.set(crypto.generate_password(
        crypto.pwd_length.value,
        crypto.pwd_include_upper.value,
        crypto.pwd_include_lower.value,
        crypto.pwd_include_digits.value,
        crypto.pwd_include_symbols.value
    ))


@app.event("b64:mode:encode")
async def handle_b64_encode(data):
    """Switch to encode mode and update output."""
    encoders.b64_mode.set("encode")
    encoders.b64_output.set(encoders.encode_base64(encoders.b64_input.value))


@app.event("b64:mode:decode")
async def handle_b64_decode(data):
    """Switch to decode mode and update output."""
    encoders.b64_mode.set("decode")
    encoders.b64_output.set(encoders.decode_base64(encoders.b64_input.value))


@app.event("url:mode:encode")
async def handle_url_encode(data):
    """Switch to encode mode and update output."""
    encoders.url_mode.set("encode")
    encoders.url_output.set(encoders.encode_url(encoders.url_input.value))


@app.event("url:mode:decode")
async def handle_url_decode(data):
    """Switch to decode mode and update output."""
    encoders.url_mode.set("decode")
    encoders.url_output.set(encoders.decode_url(encoders.url_input.value))


@app.event("lorem:generate")
async def handle_lorem_generate(data):
    """Generate lorem ipsum text."""
    generators.lorem_output.set(generators.generate_lorem(generators.lorem_paragraphs.value))


@app.event("diff:compare")
async def handle_diff_compare(data):
    """Compare two texts."""
    text.diff_result.set(text.simple_diff(text.diff_text1.value, text.diff_text2.value))


@app.event("regex:flag:i")
async def handle_regex_flag_i(data):
    """Toggle case insensitive flag."""
    flags = text.regex_flags.value.copy()
    flags["i"] = data.get("checked", False)
    text.regex_flags.set(flags)


@app.event("regex:flag:m")
async def handle_regex_flag_m(data):
    """Toggle multiline flag."""
    flags = text.regex_flags.value.copy()
    flags["m"] = data.get("checked", False)
    text.regex_flags.set(flags)


@app.event("regex:flag:g")
async def handle_regex_flag_g(data):
    """Toggle global flag."""
    flags = text.regex_flags.value.copy()
    flags["g"] = data.get("checked", True)
    text.regex_flags.set(flags)


@app.event("copy")
async def handle_copy(data):
    """Handle copy to clipboard (client-side handles actual copy)."""
    pass


# ============================================
# State Change Subscribers (for derived state updates)
# ============================================

@converters.color_input.subscribe
def on_color_change(value):
    """Update color conversions when input changes."""
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


@converters.case_input.subscribe
def on_case_change(value):
    """Update case conversions when input changes."""
    if value:
        converters.case_results.set(converters.convert_all_cases(value))
    else:
        converters.case_results.set({})


@converters.num_input.subscribe
def on_num_input_change(value):
    """Update number conversions when input changes."""
    _update_number_conversion()


@converters.num_base.subscribe
def on_num_base_change(value):
    """Update number conversions when base changes."""
    _update_number_conversion()


def _update_number_conversion():
    """Update number conversion results."""
    value = converters.num_input.value
    if value:
        base = int(converters.num_base.value)
        converters.num_results.set(converters.convert_number_base(value, base))
    else:
        converters.num_results.set({})


@encoders.b64_input.subscribe
def on_b64_input_change(value):
    """Update base64 output when input changes."""
    if encoders.b64_mode.value == "encode":
        encoders.b64_output.set(encoders.encode_base64(value))
    else:
        encoders.b64_output.set(encoders.decode_base64(value))


@encoders.url_input.subscribe
def on_url_input_change(value):
    """Update URL output when input changes."""
    if encoders.url_mode.value == "encode":
        encoders.url_output.set(encoders.encode_url(value))
    else:
        encoders.url_output.set(encoders.decode_url(value))


@encoders.jwt_input.subscribe
def on_jwt_input_change(token):
    """Decode JWT when input changes."""
    if token:
        header, payload, valid = encoders.decode_jwt(token)
        encoders.jwt_header.set(header)
        encoders.jwt_payload.set(payload)
        encoders.jwt_valid.set(valid)
    else:
        encoders.jwt_header.set({})
        encoders.jwt_payload.set({})
        encoders.jwt_valid.set(True)


@text.wc_input.subscribe
def on_wc_input_change(value):
    """Update word count stats when input changes."""
    text.wc_stats.set(text.count_text(value))


@text.regex_pattern.subscribe
def on_regex_pattern_change(value):
    """Update regex matches when pattern changes."""
    _update_regex()


@text.regex_text.subscribe
def on_regex_text_change(value):
    """Update regex matches when text changes."""
    _update_regex()


@text.regex_flags.subscribe
def on_regex_flags_change(value):
    """Update regex matches when flags change."""
    _update_regex()


def _update_regex():
    """Update regex matches."""
    pattern = text.regex_pattern.value
    test_text = text.regex_text.value
    if pattern and test_text:
        text.regex_matches.set(text.test_regex(pattern, test_text, text.regex_flags.value))
    else:
        text.regex_matches.set([])


# ============================================
# Main
# ============================================

if __name__ == "__main__":
    app.brew(
        type="web",
        title="Cacao Tools",
        ASCII_debug=True,
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
