"""Encoder/Decoder tools - Base64, URL encoding, JWT."""

import base64
import urllib.parse
import json
from cacao.core.state import State
from cacao.ui import (
    div, h2, h4, p, span, pre, button, textarea, label,
    tool_container, dual_pane, mode_toggle
)

# Base64 state
b64_input = State("")
b64_output = State("")
b64_mode = State("encode")

# URL encode state
url_input = State("")
url_output = State("")
url_mode = State("encode")

# JWT state
jwt_input = State("")
jwt_header = State({})
jwt_payload = State({})
jwt_valid = State(True)


def base64_tool():
    """Base64 encode/decode tool."""
    return tool_container(
        "Base64 Encoder/Decoder",
        "Encode text to Base64 or decode Base64 to text",
        mode_toggle(
            [("encode", "Encode", "b64:mode:encode"),
             ("decode", "Decode", "b64:mode:decode")],
            b64_mode.value
        ),
        dual_pane(
            "Input",
            textarea(
                value=b64_input.value,
                onChange="b64:input",
                placeholder="Enter text to encode/decode...",
                className="tool-input mono",
                rows=8
            ),
            "Output",
            div(
                textarea(
                    value=b64_output.value,
                    readOnly=True,
                    className="tool-input mono",
                    rows=8
                ),
                button("Copy", onClick=f"copy:{b64_output.value}", className="btn btn-sm")
            )
        )
    )


def url_encode_tool():
    """URL encode/decode tool."""
    return tool_container(
        "URL Encoder/Decoder",
        "Encode or decode URL components",
        mode_toggle(
            [("encode", "Encode", "url:mode:encode"),
             ("decode", "Decode", "url:mode:decode")],
            url_mode.value
        ),
        dual_pane(
            "Input",
            textarea(
                value=url_input.value,
                onChange="url:input",
                placeholder="Enter URL or text to encode/decode...",
                className="tool-input mono",
                rows=6
            ),
            "Output",
            div(
                textarea(
                    value=url_output.value,
                    readOnly=True,
                    className="tool-input mono",
                    rows=6
                ),
                button("Copy", onClick=f"copy:{url_output.value}", className="btn btn-sm")
            )
        )
    )


def jwt_decode_tool():
    """JWT decoder tool."""
    header_json = json.dumps(jwt_header.value, indent=2) if jwt_header.value else ""
    payload_json = json.dumps(jwt_payload.value, indent=2) if jwt_payload.value else ""

    return tool_container(
        "JWT Decoder",
        "Decode and inspect JSON Web Tokens",
        div(
            label("JWT Token"),
            textarea(
                value=jwt_input.value,
                onChange="jwt:input",
                placeholder="Paste your JWT token here...",
                className="tool-input mono",
                rows=4
            ),
            className="input-section"
        ),
        div(
            span("Valid JWT structure" if jwt_valid.value else "Invalid JWT"),
            className=f"jwt-status {'valid' if jwt_valid.value else 'invalid'}"
        ),
        div(
            div(
                h4("Header", className="jwt-part-title header"),
                pre(header_json, className="jwt-json"),
                className="jwt-part"
            ),
            div(
                h4("Payload", className="jwt-part-title payload"),
                pre(payload_json, className="jwt-json"),
                className="jwt-part"
            ),
            className="jwt-parts"
        )
    )


# Utility functions

def encode_base64(text: str) -> str:
    """Encode text to Base64."""
    try:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return ""


def decode_base64(text: str) -> str:
    """Decode Base64 to text."""
    try:
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[Invalid Base64]"


def encode_url(text: str) -> str:
    """URL encode text."""
    return urllib.parse.quote(text, safe='')


def decode_url(text: str) -> str:
    """URL decode text."""
    try:
        return urllib.parse.unquote(text)
    except Exception:
        return "[Invalid URL encoding]"


def decode_jwt(token: str) -> tuple:
    """Decode JWT token and return (header, payload, valid)."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {}, {}, False

        # Decode header (add padding)
        header_b64 = parts[0] + '=' * (4 - len(parts[0]) % 4)
        header = json.loads(base64.urlsafe_b64decode(header_b64))

        # Decode payload (add padding)
        payload_b64 = parts[1] + '=' * (4 - len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))

        return header, payload, True
    except Exception:
        return {}, {}, False
