"""
Validation mixin for the Cacao framework.
Provides input sanitization to ensure data integrity and security.
"""

import re
from typing import Any, Callable

class ValidationMixin:
    """
    Mixin that provides methods for sanitizing and validating user input.
    """

    @staticmethod
    def sanitize(input_data: str) -> str:
        """
        Sanitize a given string by escaping potentially harmful characters.
        This implementation removes script tags and escapes HTML special characters.
        """
        # Remove script tags and their content
        sanitized = re.sub(
            r'<script.*?>.*?</script>',
            '',
            input_data,
            flags=re.IGNORECASE | re.DOTALL
        )
        # Escape HTML special characters
        sanitized = (
            sanitized.replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;")
                     .replace("\"", "&quot;")
                     .replace("'", "&#x27;")
        )
        return sanitized

    @staticmethod
    def validate_length(input_data: str, min_length: int = 1, max_length: int = 1000) -> bool:
        """
        Validates that the length of input_data is within specified bounds.
        """
        return min_length <= len(input_data) <= max_length

    def validate(self, input_data: Any, validator: Callable[[Any], bool]) -> bool:
        """
        General validation method that applies a validator function to the input_data.
        """
        return validator(input_data)
