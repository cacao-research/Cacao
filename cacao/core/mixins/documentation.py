"""
Documentation mixin for automatically generating
markdown-style API docs for components or functions.
"""

from typing import Any

class DocumentedMixin:
    """Adds auto-documentation capabilities to components or classes."""
    
    def generate_docs(self) -> str:
        """
        Outputs Markdown with component or class API details.
        Override `_document_props()` and `_document_methods()` as needed.
        """
        return f"""
## {self.__class__.__name__}
**Props**: {self._document_props()}
**Methods**: {self._document_methods()}
        """

    def _document_props(self) -> str:
        """
        Return string describing props or attributes of the class.
        """
        attrs = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        return ", ".join(attrs)

    def _document_methods(self) -> str:
        """
        Return string describing public methods of the class.
        """
        methods = [method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("__")]
        return ", ".join(methods)
