"""Cryptographic tools - hashing, UUID generation, passwords."""

import hashlib
import uuid
import secrets
import string
from cacao.core.state import State
from cacao.ui import (
    div, h2, p, button, textarea, select, checkbox,
    range_input, labeled, result_row, tool_container, input
)

# Constants
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

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
    return tool_container(
        "Hash Text",
        "Generate hashes using MD5, SHA1, SHA256, SHA512",
        textarea(
            value=hash_input.value,
            onChange="hash:input",
            placeholder="Enter text to hash...",
            className="tool-input",
            rows=4
        ),
        button("Generate Hashes", onClick="hash:generate", className="btn btn-primary"),
        div(
            result_row("MD5", hash_results.value.get("md5", "")),
            result_row("SHA1", hash_results.value.get("sha1", "")),
            result_row("SHA256", hash_results.value.get("sha256", "")),
            result_row("SHA512", hash_results.value.get("sha512", "")),
            className="hash-results"
        )
    )


def uuid_generator():
    """Generate UUIDs."""
    return tool_container(
        "UUID Generator",
        "Generate universally unique identifiers",
        labeled(
            "Version:",
            select(
                value=uuid_version.value,
                onChange="uuid:version",
                options=[("1", "UUID v1 (timestamp)"), ("4", "UUID v4 (random)")]
            )
        ),
        button("Generate UUID", onClick="uuid:generate", className="btn btn-primary"),
        div(
            input(value=uuid_result.value, readOnly=True, className="result-value large"),
            button("Copy", onClick=f"copy:{uuid_result.value}", className="btn btn-sm"),
            className="result-box"
        )
    )


def password_generator():
    """Generate secure passwords."""
    return tool_container(
        "Password Generator",
        "Generate cryptographically secure passwords",
        labeled(
            f"Length: {pwd_length.value}",
            range_input(
                value=pwd_length.value,
                onChange="pwd:length",
                min=8,
                max=64
            )
        ),
        div(
            checkbox(pwd_include_upper.value, "pwd:upper", "Uppercase (A-Z)"),
            checkbox(pwd_include_lower.value, "pwd:lower", "Lowercase (a-z)"),
            checkbox(pwd_include_digits.value, "pwd:digits", "Digits (0-9)"),
            checkbox(pwd_include_symbols.value, "pwd:symbols", "Symbols (!@#$...)"),
            className="checkbox-group"
        ),
        button("Generate Password", onClick="pwd:generate", className="btn btn-primary"),
        div(
            input(value=pwd_result.value, readOnly=True, className="result-value large mono"),
            button("Copy", onClick=f"copy:{pwd_result.value}", className="btn btn-sm"),
            className="result-box"
        )
    )


# Utility functions

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
        chars += SYMBOLS

    if not chars:
        chars = string.ascii_letters + string.digits

    return ''.join(secrets.choice(chars) for _ in range(length))
