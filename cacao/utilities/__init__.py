"""
Utilities package initialization.
Provides common utilities and helper functions for the Cacao framework.
"""

from .cache import cache
from .documentation import generate_api_docs
from .icons import IconRegistry, icon_registry, process_icons_in_component
from .task_queue import TaskQueue

__all__ = [
    "cache",
    "generate_api_docs",
    "IconRegistry",
    "icon_registry",
    "process_icons_in_component",
    "TaskQueue"
]