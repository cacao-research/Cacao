"""Encoder/Decoder tools - Base64, URL encoding, JWT."""

import base64
import urllib.parse
import json
from cacao.core.state import State

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
                            {"type": "h2", "props": {"content": "Base64 Encoder/Decoder"}},
                            {"type": "p", "props": {"content": "Encode text to Base64 or decode Base64 to text"}}
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
                                    "className": "mode-toggle",
                                    "children": [
                                        {
                                            "type": "button",
                                            "props": {
                                                "content": "Encode",
                                                "onClick": "b64:mode:encode",
                                                "className": f"btn {'btn-primary' if b64_mode.value == 'encode' else 'btn-secondary'}"
                                            }
                                        },
                                        {
                                            "type": "button",
                                            "props": {
                                                "content": "Decode",
                                                "onClick": "b64:mode:decode",
                                                "className": f"btn {'btn-primary' if b64_mode.value == 'decode' else 'btn-secondary'}"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "dual-pane",
                                    "children": [
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "pane",
                                                "children": [
                                                    {"type": "label", "props": {"content": "Input"}},
                                                    {
                                                        "type": "textarea",
                                                        "props": {
                                                            "placeholder": "Enter text to encode/decode...",
                                                            "value": b64_input.value,
                                                            "onChange": "b64:input",
                                                            "className": "tool-input mono",
                                                            "rows": 8
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "pane",
                                                "children": [
                                                    {"type": "label", "props": {"content": "Output"}},
                                                    {
                                                        "type": "textarea",
                                                        "props": {
                                                            "value": b64_output.value,
                                                            "readOnly": True,
                                                            "className": "tool-input mono",
                                                            "rows": 8
                                                        }
                                                    },
                                                    {
                                                        "type": "button",
                                                        "props": {
                                                            "content": "Copy",
                                                            "onClick": f"copy:{b64_output.value}",
                                                            "className": "btn btn-sm"
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
    }


def url_encode_tool():
    """URL encode/decode tool."""
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
                            {"type": "h2", "props": {"content": "URL Encoder/Decoder"}},
                            {"type": "p", "props": {"content": "Encode or decode URL components"}}
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
                                    "className": "mode-toggle",
                                    "children": [
                                        {
                                            "type": "button",
                                            "props": {
                                                "content": "Encode",
                                                "onClick": "url:mode:encode",
                                                "className": f"btn {'btn-primary' if url_mode.value == 'encode' else 'btn-secondary'}"
                                            }
                                        },
                                        {
                                            "type": "button",
                                            "props": {
                                                "content": "Decode",
                                                "onClick": "url:mode:decode",
                                                "className": f"btn {'btn-primary' if url_mode.value == 'decode' else 'btn-secondary'}"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "dual-pane",
                                    "children": [
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "pane",
                                                "children": [
                                                    {"type": "label", "props": {"content": "Input"}},
                                                    {
                                                        "type": "textarea",
                                                        "props": {
                                                            "placeholder": "Enter URL or text to encode/decode...",
                                                            "value": url_input.value,
                                                            "onChange": "url:input",
                                                            "className": "tool-input mono",
                                                            "rows": 6
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "pane",
                                                "children": [
                                                    {"type": "label", "props": {"content": "Output"}},
                                                    {
                                                        "type": "textarea",
                                                        "props": {
                                                            "value": url_output.value,
                                                            "readOnly": True,
                                                            "className": "tool-input mono",
                                                            "rows": 6
                                                        }
                                                    },
                                                    {
                                                        "type": "button",
                                                        "props": {
                                                            "content": "Copy",
                                                            "onClick": f"copy:{url_output.value}",
                                                            "className": "btn btn-sm"
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
    }


def jwt_decode_tool():
    """JWT decoder tool."""
    header_json = json.dumps(jwt_header.value, indent=2) if jwt_header.value else ""
    payload_json = json.dumps(jwt_payload.value, indent=2) if jwt_payload.value else ""

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
                            {"type": "h2", "props": {"content": "JWT Decoder"}},
                            {"type": "p", "props": {"content": "Decode and inspect JSON Web Tokens"}}
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
                                    "className": "input-section",
                                    "children": [
                                        {"type": "label", "props": {"content": "JWT Token"}},
                                        {
                                            "type": "textarea",
                                            "props": {
                                                "placeholder": "Paste your JWT token here...",
                                                "value": jwt_input.value,
                                                "onChange": "jwt:input",
                                                "className": "tool-input mono",
                                                "rows": 4
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": f"jwt-status {'valid' if jwt_valid.value else 'invalid'}",
                                    "children": [
                                        {
                                            "type": "span",
                                            "props": {
                                                "content": "Valid JWT structure" if jwt_valid.value else "Invalid JWT"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "jwt-parts",
                                    "children": [
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "jwt-part",
                                                "children": [
                                                    {"type": "h4", "props": {"content": "Header", "className": "jwt-part-title header"}},
                                                    {
                                                        "type": "pre",
                                                        "props": {
                                                            "content": header_json,
                                                            "className": "jwt-json"
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "type": "div",
                                            "props": {
                                                "className": "jwt-part",
                                                "children": [
                                                    {"type": "h4", "props": {"content": "Payload", "className": "jwt-part-title payload"}},
                                                    {
                                                        "type": "pre",
                                                        "props": {
                                                            "content": payload_json,
                                                            "className": "jwt-json"
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
    }


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

        # Decode header
        header_b64 = parts[0] + '=' * (4 - len(parts[0]) % 4)  # Add padding
        header = json.loads(base64.urlsafe_b64decode(header_b64))

        # Decode payload
        payload_b64 = parts[1] + '=' * (4 - len(parts[1]) % 4)  # Add padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))

        return header, payload, True
    except Exception:
        return {}, {}, False
