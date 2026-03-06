"""
Cacao Plugin Registry.

Provides a formal plugin system for Cacao extensions like CacaoDocs.
Plugins can register themselves, define lifecycle hooks, and inject
UI into predefined slots.

Example:
    from cacao.server.plugin import PluginRegistry

    registry = PluginRegistry()
    registry.register("cacaodocs", version="0.1.19", config_schema={...})
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

logger = logging.getLogger("cacao.plugin")

LifecycleHook = Literal[
    "on_init", "on_ready", "on_shutdown", "on_request", "on_session_start", "on_session_end"
]

_VALID_HOOKS: set[str] = {
    "on_init",
    "on_ready",
    "on_shutdown",
    "on_request",
    "on_session_start",
    "on_session_end",
}

_VALID_SLOTS: set[str] = {
    "header",
    "footer",
    "sidebar",
    "head",  # inject into <head> (scripts, styles)
}


@dataclass
class Plugin:
    """Registered plugin metadata and hooks."""

    name: str
    version: str = "0.0.0"
    description: str = ""
    author: str = ""
    config_schema: dict[str, Any] = field(default_factory=dict)
    hooks: dict[str, list[Callable[..., Any]]] = field(default_factory=dict)
    slots: dict[str, list[Callable[..., Any]]] = field(default_factory=dict)
    middleware: list[Callable[..., Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def on(self, hook: LifecycleHook, handler: Callable[..., Any]) -> None:
        """Register a lifecycle hook handler."""
        if hook not in _VALID_HOOKS:
            raise ValueError(f"Invalid hook '{hook}'. Valid hooks: {_VALID_HOOKS}")
        self.hooks.setdefault(hook, []).append(handler)

    def inject(self, slot: str, renderer: Callable[..., Any]) -> None:
        """Register a UI renderer for a slot (header, footer, sidebar, head)."""
        if slot not in _VALID_SLOTS:
            raise ValueError(f"Invalid slot '{slot}'. Valid slots: {_VALID_SLOTS}")
        self.slots.setdefault(slot, []).append(renderer)

    def add_middleware(self, handler: Callable[..., Any]) -> None:
        """Add middleware that intercepts/transforms events."""
        self.middleware.append(handler)


class PluginRegistry:
    """Central registry for all Cacao plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(
        self,
        name: str,
        *,
        version: str = "0.0.0",
        description: str = "",
        author: str = "",
        config_schema: dict[str, Any] | None = None,
        **metadata: Any,
    ) -> Plugin:
        """
        Register a plugin.

        Args:
            name: Unique plugin name (e.g. "cacaodocs")
            version: Plugin version string
            description: Short description
            author: Plugin author
            config_schema: Optional schema describing expected cacao.yaml keys
            **metadata: Arbitrary extra metadata

        Returns:
            The Plugin instance (use to add hooks, slots, middleware)
        """
        if name in self._plugins:
            logger.warning("Plugin '%s' already registered, replacing", name)

        plugin = Plugin(
            name=name,
            version=version,
            description=description,
            author=author,
            config_schema=config_schema or {},
            metadata=metadata,
        )
        self._plugins[name] = plugin
        logger.info("Plugin registered: %s v%s", name, version)
        return plugin

    def get(self, name: str) -> Plugin | None:
        """Get a registered plugin by name."""
        return self._plugins.get(name)

    def all(self) -> dict[str, Plugin]:
        """Get all registered plugins."""
        return dict(self._plugins)

    def unregister(self, name: str) -> bool:
        """Unregister a plugin. Returns True if it existed."""
        if name in self._plugins:
            del self._plugins[name]
            logger.info("Plugin unregistered: %s", name)
            return True
        return False

    async def run_hook(self, hook: LifecycleHook, *args: Any, **kwargs: Any) -> None:
        """Run all handlers for a lifecycle hook across all plugins."""
        for plugin in self._plugins.values():
            for handler in plugin.hooks.get(hook, []):
                try:
                    result = handler(*args, **kwargs)
                    # Await if coroutine
                    if hasattr(result, "__await__"):
                        await result
                except Exception:
                    logger.exception("Error in plugin '%s' hook '%s'", plugin.name, hook)

    def get_slot_renderers(self, slot: str) -> list[Callable[..., Any]]:
        """Get all renderers registered for a UI slot."""
        renderers: list[Callable[..., Any]] = []
        for plugin in self._plugins.values():
            renderers.extend(plugin.slots.get(slot, []))
        return renderers

    def get_all_middleware(self) -> list[Callable[..., Any]]:
        """Get all middleware handlers from all plugins."""
        middleware: list[Callable[..., Any]] = []
        for plugin in self._plugins.values():
            middleware.extend(plugin.middleware)
        return middleware


# Global registry instance
_registry = PluginRegistry()


def get_registry() -> PluginRegistry:
    """Get the global plugin registry."""
    return _registry
