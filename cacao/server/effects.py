"""
Side effects and reactive utilities for Cacao v2.

Effects allow running side effects in response to signal changes.
They are useful for things like logging, analytics, or triggering
external API calls.
"""

from __future__ import annotations

from typing import TypeVar, Generic, Callable, Any, TYPE_CHECKING, Awaitable
from functools import wraps
import asyncio

if TYPE_CHECKING:
    from .session import Session
    from .signal import Signal

T = TypeVar("T")


class Effect:
    """
    A side effect that runs when signals change.

    Effects are used for running side effects in response to signal changes.
    Unlike Computed signals, Effects don't return values - they perform
    actions like logging, API calls, or triggering other operations.

    Example:
        count = Signal(0, name="count")

        @Effect.on(count)
        def log_count_change(session, value):
            print(f"Count changed to {value}")

        # Or with async:
        @Effect.on(count)
        async def sync_to_database(session, value):
            await db.save("count", value)
    """

    _all_effects: list["Effect"] = []

    def __init__(
        self,
        callback: Callable[["Session", Any], Any | Awaitable[Any]],
        signals: list["Signal[Any]"],
        *,
        name: str | None = None,
        run_immediately: bool = False,
    ) -> None:
        """
        Create a new Effect.

        Args:
            callback: Function to call when signals change
            signals: Signals to watch for changes
            name: Optional name for debugging
            run_immediately: If True, run the effect once on creation
        """
        self._callback = callback
        self._signals = signals
        self._name = name or f"effect_{id(self)}"
        self._enabled = True
        self._unsubscribers: list[Callable[[], None]] = []

        # Subscribe to all signals
        for signal in signals:
            unsub = signal.subscribe(self._on_signal_change)
            self._unsubscribers.append(unsub)

        Effect._all_effects.append(self)

    @property
    def name(self) -> str:
        """The name of this effect."""
        return self._name

    @property
    def enabled(self) -> bool:
        """Whether the effect is currently enabled."""
        return self._enabled

    def enable(self) -> None:
        """Enable the effect."""
        self._enabled = True

    def disable(self) -> None:
        """Disable the effect temporarily."""
        self._enabled = False

    def _on_signal_change(self, session_id: str, value: Any) -> None:
        """Handle signal change."""
        if not self._enabled:
            return

        # Import here to avoid circular import
        from .session import SessionManager

        session = SessionManager.get_session(session_id)
        if session is None:
            return

        try:
            result = self._callback(session, value)
            if asyncio.iscoroutine(result):
                asyncio.create_task(result)
        except Exception as e:
            # Log but don't break the signal chain
            print(f"Effect '{self._name}' error: {e}")

    def dispose(self) -> None:
        """
        Dispose the effect and unsubscribe from all signals.
        """
        for unsub in self._unsubscribers:
            unsub()
        self._unsubscribers.clear()
        if self in Effect._all_effects:
            Effect._all_effects.remove(self)

    @classmethod
    def on(
        cls,
        *signals: "Signal[Any]",
        name: str | None = None,
        run_immediately: bool = False,
    ) -> Callable[[Callable[["Session", Any], Any]], "Effect"]:
        """
        Decorator to create an effect from a function.

        Args:
            *signals: Signals to watch
            name: Optional name for the effect
            run_immediately: If True, run effect immediately

        Example:
            @Effect.on(count_signal)
            def on_count_change(session, value):
                print(f"Count is now {value}")
        """
        def decorator(fn: Callable[["Session", Any], Any]) -> Effect:
            effect_name = name or fn.__name__
            return cls(fn, list(signals), name=effect_name, run_immediately=run_immediately)
        return decorator

    @classmethod
    def dispose_all(cls) -> None:
        """Dispose all registered effects."""
        for effect in cls._all_effects[:]:
            effect.dispose()


class Watch(Generic[T]):
    """
    Watch a signal and run a callback when it changes.

    Similar to Effect but focused on a single signal with typed values.

    Example:
        count = Signal(0, name="count")

        watch = Watch(count, lambda session, old, new: print(f"{old} -> {new}"))
    """

    def __init__(
        self,
        signal: "Signal[T]",
        callback: Callable[["Session", T, T], Any | Awaitable[Any]],
        *,
        immediate: bool = False,
    ) -> None:
        """
        Create a new Watch.

        Args:
            signal: Signal to watch
            callback: Called with (session, old_value, new_value)
            immediate: If True, call callback immediately with current value
        """
        self._signal = signal
        self._callback = callback
        self._previous: dict[str, T] = {}

        self._unsubscribe = signal.subscribe(self._on_change)

    def _on_change(self, session_id: str, new_value: T) -> None:
        """Handle signal change."""
        from .session import SessionManager

        session = SessionManager.get_session(session_id)
        if session is None:
            return

        old_value = self._previous.get(session_id, self._signal.default)
        self._previous[session_id] = new_value

        if old_value != new_value:
            try:
                result = self._callback(session, old_value, new_value)
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception as e:
                print(f"Watch callback error: {e}")

    def dispose(self) -> None:
        """Stop watching the signal."""
        self._unsubscribe()
        self._previous.clear()


def effect(
    *signals: "Signal[Any]",
    name: str | None = None,
) -> Callable[[Callable[["Session", Any], Any]], Effect]:
    """
    Shorthand decorator for creating effects.

    Example:
        @effect(count, name="log_count")
        def log_count(session, value):
            print(f"Count: {value}")
    """
    return Effect.on(*signals, name=name)
