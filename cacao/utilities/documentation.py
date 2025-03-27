"""
Documentation utilities for the Cacao framework.
Provides functions to parse docstrings and generate Markdown API documentation.
"""

import inspect
from typing import Any

def generate_api_docs(module: Any) -> str:
    """
    Generates Markdown documentation for all public functions and classes in a module.
    
    Args:
        module: The module to document.
    
    Returns:
        A string containing the generated Markdown documentation.
    """
    docs = []
    for name, obj in inspect.getmembers(module):
        if not name.startswith("_"):
            docstring = inspect.getdoc(obj)
            if docstring:
                docs.append(f"## {name}\n\n{docstring}\n")
    return "\n".join(docs)
