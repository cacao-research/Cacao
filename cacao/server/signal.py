"""
Reactive Signal primitive with session-scoped state.

Signals are the core reactive primitive in Cacao v2. They hold state that is
scoped to individual sessions (WebSocket connections), ensuring multi-user
apps work correctly by default.
"""

from __future__ import annotations

from typing import TypeVar, Generic, Callable, Any, TYPE_CHECKING
from weakref import WeakSet
import asyncio

if TYPE_CHECKING:
    from .session import Session

T = TypeVar("T")


class Signal(Generic[T]):
    """
    A reactive state container with session-scoped values.

    Each Signal can hold different values for different sessions, making it
    safe for multi-user applications. When a Signal's value changes, all
    registered subscribers are notified.

    Example:
        count = Signal(0, name="count")

        # In a route handler:
        current = count.get(session)
        count.set(session, current + 1)
    """

    _all_signals: dict[str, "Signal[Any]"] = {}

    def __init__(self, default: T, *, name: str | None = None) -> None:
        """
        Create a new Signal with a default value.

        Args:
            default: The default value for new sessions
            name: Optional name for the signal (used in state sync).
                  If not provided, one will be auto-generated.
        """
        self._default = default
        self._values: dict[str, T] = {}  # session_id -> value
        self._subscribers: WeakSet[Callable[[str, T], Any]] = WeakSet()

        # Auto-generate name if not provided
        if name is None:
            name = f"signal_{id(self)}"
        self._name = name

        # Register globally for state serialization
        Signal._all_signals[name] = self

    @property
    def name(self) -> str:
        """The name of this signal, used in state sync."""
        return self._name

    @property
    def default(self) -> T:
        """The default value for new sessions."""
        return self._default

    def get(self, session: "Session") -> T:
        """
        Get the current value for a session.

        Args:
            session: The session to get the value for

        Returns:
            The current value, or the default if not set
        """
        return self._values.get(session.id, self._default)

    def set(self, session: "Session", value: T) -> None:
        """
        Set the value for a session and notify subscribers.

        Args:
            session: The session to set the value for
            value: The new value
        """
        old_value = self._values.get(session.id, self._default)
        if old_value == value:
            return  # No change, skip notification

        self._values[session.id] = value

        # Notify subscribers
        for subscriber in self._subscribers:
            try:
                result = subscriber(session.id, value)
                # Handle async subscribers
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception:
                pass  # Don't let subscriber errors break the signal

    def update(self, session: "Session", updater: Callable[[T], T]) -> T:
        """
        Update the value using a function.

        Args:
            session: The session to update the value for
            updater: A function that takes the current value and returns the new value

        Returns:
            The new value
        """
        current = self.get(session)
        new_value = updater(current)
        self.set(session, new_value)
        return new_value

    def subscribe(self, callback: Callable[[str, T], Any]) -> Callable[[], None]:
        """
        Subscribe to value changes.

        Args:
            callback: Called with (session_id, new_value) on changes

        Returns:
            An unsubscribe function
        """
        self._subscribers.add(callback)

        def unsubscribe() -> None:
            self._subscribers.discard(callback)

        return unsubscribe

    def clear_session(self, session: "Session") -> None:
        """
        Clear the value for a session (revert to default).

        Args:
            session: The session to clear
        """
        self._values.pop(session.id, None)

    def get_all_for_session(self, session: "Session") -> dict[str, Any]:
        """
        Get all signal values for a session.

        This is a class method that returns all registered signals' values
        for the given session.

        Args:
            session: The session to get values for

        Returns:
            A dict mapping signal names to their values
        """
        return {
            name: signal.get(session)
            for name, signal in Signal._all_signals.items()
        }

    @classmethod
    def get_all_signals(cls) -> dict[str, "Signal[Any]"]:
        """Get all registered signals."""
        return cls._all_signals.copy()

    @classmethod
    def clear_all_for_session(cls, session: "Session") -> None:
        """Clear all signal values for a session."""
        for signal in cls._all_signals.values():
            signal.clear_session(session)


class Computed(Generic[T]):
    """
    A derived signal that computes its value from other signals.

    Computed signals are read-only and automatically update when their
    dependencies change.

    Example:
        count = Signal(0, name="count")
        doubled = Computed(lambda s: count.get(s) * 2, name="doubled")
    """

    def __init__(
        self,
        compute: Callable[["Session"], T],
        *,
        name: str | None = None,
        dependencies: list[Signal[Any]] | None = None,
    ) -> None:
        """
        Create a new Computed signal.

        Args:
            compute: Function that computes the value given a session
            name: Optional name for the computed signal
            dependencies: Signals this computed depends on (for invalidation)
        """
        self._compute = compute
        self._cache: dict[str, T] = {}
        self._dependencies = dependencies or []

        if name is None:
            name = f"computed_{id(self)}"
        self._name = name

        # Register globally
        Signal._all_signals[name] = self  # type: ignore

        # Subscribe to dependencies for cache invalidation
        for dep in self._dependencies:
            dep.subscribe(self._invalidate)

    @property
    def name(self) -> str:
        """The name of this computed signal."""
        return self._name

    def _invalidate(self, session_id: str, _value: Any) -> None:
        """Invalidate cached value when dependency changes."""
        self._cache.pop(session_id, None)

    def get(self, session: "Session") -> T:
        """
        Get the computed value for a session.

        The value is cached until dependencies change.

        Args:
            session: The session to compute the value for

        Returns:
            The computed value
        """
        if session.id not in self._cache:
            self._cache[session.id] = self._compute(session)
        return self._cache[session.id]

    def clear_session(self, session: "Session") -> None:
        """Clear the cached value for a session."""
        self._cache.pop(session.id, None)
