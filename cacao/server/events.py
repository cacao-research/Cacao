"""
Typed event system for Cacao v2.

Events are the mechanism for client-to-server communication. The client
dispatches events (like "increment" or "submit"), and the server handles
them with registered handlers.
"""

from __future__ import annotations

from typing import TypeVar, Generic, Callable, Any, Awaitable, TYPE_CHECKING
from dataclasses import dataclass
import asyncio

if TYPE_CHECKING:
    from .session import Session

T = TypeVar("T")

# Event handler type: async function taking (session, event_data) -> None
EventHandler = Callable[["Session", dict[str, Any]], Awaitable[None]]


@dataclass
class Event(Generic[T]):
    """
    Represents an event received from the client.

    Events are the primary way clients communicate with the server.
    Each event has a name and optional data payload.

    Attributes:
        name: The event name (e.g., "increment", "submit")
        data: The event payload
    """

    name: str
    data: T

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Event[dict[str, Any]]":
        """
        Create an Event from a dictionary.

        Args:
            d: Dictionary with 'name' and optional 'data' keys

        Returns:
            The Event instance
        """
        return cls(
            name=d.get("name", ""),
            data=d.get("data", {}),
        )


class EventRegistry:
    """
    Registry of event handlers.

    The EventRegistry stores all registered event handlers and provides
    methods for dispatching events to the appropriate handlers.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}
        self._bindings: dict[str, Any] = {}  # event_name -> Signal

    def register(self, event_name: str, handler: EventHandler) -> None:
        """
        Register an event handler.

        Multiple handlers can be registered for the same event.

        Args:
            event_name: The event to handle
            handler: The async handler function
        """
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    def bind(self, event_name: str, signal: Any) -> None:
        """
        Bind an event to a signal for automatic updates.

        When an event with this name is received, the signal will be
        automatically updated with the event's 'value' field.

        Args:
            event_name: The event name (e.g., "name:input")
            signal: The Signal to bind to
        """
        self._bindings[event_name] = signal

    def unregister(self, event_name: str, handler: EventHandler) -> bool:
        """
        Unregister an event handler.

        Args:
            event_name: The event name
            handler: The handler to remove

        Returns:
            True if the handler was found and removed
        """
        if event_name in self._handlers:
            try:
                self._handlers[event_name].remove(handler)
                return True
            except ValueError:
                pass
        return False

    async def dispatch(
        self,
        session: "Session",
        event: Event[dict[str, Any]],
    ) -> None:
        """
        Dispatch an event to all registered handlers.

        If the event is bound to a signal, the signal is updated first.
        Then all handlers are called concurrently.

        Args:
            session: The session that sent the event
            event: The event to dispatch
        """
        # Handle auto-binding first
        if event.name in self._bindings:
            signal = self._bindings[event.name]
            value = event.data.get("value")
            if value is not None:
                signal.set(session, value)

        # Get handlers for this event
        handlers = self._handlers.get(event.name, [])

        if not handlers:
            return

        # Run all handlers concurrently
        tasks = [handler(session, event.data) for handler in handlers]
        await asyncio.gather(*tasks, return_exceptions=True)

    def has_handler(self, event_name: str) -> bool:
        """Check if any handler is registered for an event."""
        return (
            event_name in self._handlers and len(self._handlers[event_name]) > 0
        ) or event_name in self._bindings

    def get_registered_events(self) -> list[str]:
        """Get all event names with registered handlers."""
        events = set(self._handlers.keys())
        events.update(self._bindings.keys())
        return list(events)
