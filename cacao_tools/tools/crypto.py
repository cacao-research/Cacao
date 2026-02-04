"""Cryptographic tools - hashing, UUID generation, passwords."""

import hashlib
import uuid
import secrets
import string
from cacao.core.state import State

# State for hash tool
hash_input = State("")
hash_results = State({})

# State for UUID generator
uuid_version = State("4")
uuid_result = State("")

# State for password generator
pwd_length = State(16)
pwd_include_upper = State(True)
pwd_include_lower = State(True)
pwd_include_digits = State(True)
pwd_include_symbols = State(True)
pwd_result = State("")


def hash_text():
    """Hash text with multiple algorithms."""
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
                            {"type": "h2", "props": {"content": "Hash Text"}},
                            {"type": "p", "props": {"content": "Generate hashes using MD5, SHA1, SHA256, SHA512"}}
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
                                    "placeholder": "Enter text to hash...",
                                    "value": hash_input.value,
                                    "onChange": "hash:input",
                                    "className": "tool-input",
                                    "rows": 4
                                }
                            },
                            {
                                "type": "button",
                                "props": {
                                    "content": "Generate Hashes",
                                    "onClick": "hash:generate",
                                    "className": "btn btn-primary"
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "hash-results",
                                    "children": [
                                        _hash_result_row("MD5", hash_results.value.get("md5", "")),
                                        _hash_result_row("SHA1", hash_results.value.get("sha1", "")),
                                        _hash_result_row("SHA256", hash_results.value.get("sha256", "")),
                                        _hash_result_row("SHA512", hash_results.value.get("sha512", "")),
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def _hash_result_row(algo: str, value: str):
    """Render a single hash result row."""
    return {
        "type": "div",
        "props": {
            "className": "result-row",
            "children": [
                {"type": "label", "props": {"content": algo, "className": "result-label"}},
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


def uuid_generator():
    """Generate UUIDs."""
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
                            {"type": "h2", "props": {"content": "UUID Generator"}},
                            {"type": "p", "props": {"content": "Generate universally unique identifiers"}}
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
                                        {"type": "label", "props": {"content": "Version:"}},
                                        {
                                            "type": "select",
                                            "props": {
                                                "value": uuid_version.value,
                                                "onChange": "uuid:version",
                                                "children": [
                                                    {"type": "option", "props": {"value": "1", "content": "UUID v1 (timestamp)"}},
                                                    {"type": "option", "props": {"value": "4", "content": "UUID v4 (random)"}},
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "button",
                                "props": {
                                    "content": "Generate UUID",
                                    "onClick": "uuid:generate",
                                    "className": "btn btn-primary"
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "result-box",
                                    "children": [
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "text",
                                                "value": uuid_result.value,
                                                "readOnly": True,
                                                "className": "result-value large"
                                            }
                                        },
                                        {
                                            "type": "button",
                                            "props": {
                                                "content": "Copy",
                                                "onClick": f"copy:{uuid_result.value}",
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


def password_generator():
    """Generate secure passwords."""
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
                            {"type": "h2", "props": {"content": "Password Generator"}},
                            {"type": "p", "props": {"content": "Generate cryptographically secure passwords"}}
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
                                        {"type": "label", "props": {"content": f"Length: {pwd_length.value}"}},
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "range",
                                                "min": 8,
                                                "max": 64,
                                                "value": pwd_length.value,
                                                "onChange": "pwd:length"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "checkbox-group",
                                    "children": [
                                        _checkbox("Uppercase (A-Z)", pwd_include_upper.value, "pwd:upper"),
                                        _checkbox("Lowercase (a-z)", pwd_include_lower.value, "pwd:lower"),
                                        _checkbox("Digits (0-9)", pwd_include_digits.value, "pwd:digits"),
                                        _checkbox("Symbols (!@#$...)", pwd_include_symbols.value, "pwd:symbols"),
                                    ]
                                }
                            },
                            {
                                "type": "button",
                                "props": {
                                    "content": "Generate Password",
                                    "onClick": "pwd:generate",
                                    "className": "btn btn-primary"
                                }
                            },
                            {
                                "type": "div",
                                "props": {
                                    "className": "result-box",
                                    "children": [
                                        {
                                            "type": "input",
                                            "props": {
                                                "type": "text",
                                                "value": pwd_result.value,
                                                "readOnly": True,
                                                "className": "result-value large mono"
                                            }
                                        },
                                        {
                                            "type": "button",
                                            "props": {
                                                "content": "Copy",
                                                "onClick": f"copy:{pwd_result.value}",
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


def _checkbox(label: str, checked: bool, action: str):
    """Render a checkbox."""
    return {
        "type": "label",
        "props": {
            "className": "checkbox-label",
            "children": [
                {
                    "type": "input",
                    "props": {
                        "type": "checkbox",
                        "checked": checked,
                        "onChange": action
                    }
                },
                {"type": "span", "props": {"content": label}}
            ]
        }
    }


# Event handlers would be registered in app.py
def generate_hashes(text: str) -> dict:
    """Generate all hash types for given text."""
    encoded = text.encode('utf-8')
    return {
        "md5": hashlib.md5(encoded).hexdigest(),
        "sha1": hashlib.sha1(encoded).hexdigest(),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "sha512": hashlib.sha512(encoded).hexdigest(),
    }


def generate_uuid(version: str) -> str:
    """Generate UUID of specified version."""
    if version == "1":
        return str(uuid.uuid1())
    return str(uuid.uuid4())


def generate_password(length: int, upper: bool, lower: bool, digits: bool, symbols: bool) -> str:
    """Generate a secure password."""
    chars = ""
    if upper:
        chars += string.ascii_uppercase
    if lower:
        chars += string.ascii_lowercase
    if digits:
        chars += string.digits
    if symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not chars:
        chars = string.ascii_letters + string.digits

    return ''.join(secrets.choice(chars) for _ in range(length))
