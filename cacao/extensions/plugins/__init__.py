"""
Plugin interface for the Cacao framework.
Defines the base class and registration mechanism for plugins.
"""

from typing import Callable, Dict, Any, List

PLUGINS: List[Any] = []

class Plugin:
    """
    Base class for Cacao plugins.
    Plugins can extend framework functionalities (e.g., themes, metrics, auth).
    """
    def __init__(self, name: str):
        self.name = name

    def register(self) -> None:
        """
        Called when the plugin is registered.
        Must be implemented by the plugin.
        """
        raise NotImplementedError("Plugin must implement the register() method.")

def register_plugin(plugin: Plugin) -> None:
    """
    Registers a plugin into the framework.
    """
    PLUGINS.append(plugin)
    plugin.register()
