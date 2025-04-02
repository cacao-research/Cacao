"""
Mixins package initialization.
Provides common functionality that can be composed into Cacao components and classes.
"""

from .validation import ValidationMixin
from .logging import LoggingMixin, Colors
from .documentation import DocumentedMixin

__all__ = [
    "ValidationMixin",
    "LoggingMixin",
    "Colors",
    "DocumentedMixin"
]