"""
Batch updates for Cacao v2.

Batch allows grouping multiple signal updates into a single
network message, improving performance and ensuring atomic updates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable
from contextlib import contextmanager
import asyncio

if TYPE_CHECKING:
    from .session import Session
    from .signal import Signal

# Thread-local storage for batch context
_batch_context: dict[str, "BatchContext"] = {}


class BatchContext:
    """
    Context for batching signal updates.

    Collects updates and sends them as a single message when the batch ends.
    """

    def __init__(self, session: "Session") -> None:
        self.session = session
        self.updates: dict[str, Any] = {}
        self._original_send: Callable[..., Any] | None = None

    def add_update(self, signal_name: str, value: Any) -> None:
        """Add an update to the batch."""
        self.updates[signal_name] = value

    async def flush(self) -> None:
        """Send all batched updates."""
        if not self.updates:
            return

        message = {
            "type": "batch",
            "changes": [
                {"key": name, "value": value}
                for name, value in self.updates.items()
            ],
        }

        await self.session.send(message)
        self.updates.clear()


@contextmanager
def batch(session: "Session"):
    """
    Context manager for batching signal updates.

    All signal updates within the context will be collected and sent
    as a single batch message when the context exits.

    Example:
        with batch(session):
            name.set(session, "John")
            age.set(session, 30)
            email.set(session, "john@example.com")
        # All three updates sent in one message

    Args:
        session: The session to batch updates for

    Yields:
        The batch context (rarely needed directly)
    """
    ctx = BatchContext(session)
    _batch_context[session.id] = ctx

    try:
        yield ctx
    finally:
        # Send batched updates
        if ctx.updates:
            asyncio.create_task(ctx.flush())
        del _batch_context[session.id]


def get_current_batch(session_id: str) -> BatchContext | None:
    """Get the current batch context for a session, if any."""
    return _batch_context.get(session_id)


def is_batching(session_id: str) -> bool:
    """Check if the session is currently in a batch context."""
    return session_id in _batch_context


class Batch:
    """
    Class-based batch context for more control.

    Example:
        b = Batch(session)
        b.set(count, 10)
        b.set(name, "John")
        await b.commit()
    """

    def __init__(self, session: "Session") -> None:
        """
        Create a new batch.

        Args:
            session: The session to batch updates for
        """
        self.session = session
        self.updates: dict[str, Any] = {}
        self._committed = False

    def set(self, signal: "Signal[Any]", value: Any) -> "Batch":
        """
        Add a signal update to the batch.

        Args:
            signal: The signal to update
            value: The new value

        Returns:
            self for chaining
        """
        if self._committed:
            raise RuntimeError("Batch already committed")

        self.updates[signal.name] = value
        # Also update the signal's internal state
        signal._values[self.session.id] = value
        return self

    def update(self, signal: "Signal[Any]", updater: Callable[[Any], Any]) -> "Batch":
        """
        Add a signal update using an updater function.

        Args:
            signal: The signal to update
            updater: Function that takes current value and returns new value

        Returns:
            self for chaining
        """
        current = signal.get(self.session)
        return self.set(signal, updater(current))

    async def commit(self) -> None:
        """
        Send all batched updates to the client.
        """
        if self._committed:
            raise RuntimeError("Batch already committed")

        self._committed = True

        if not self.updates:
            return

        message = {
            "type": "batch",
            "changes": [
                {"key": name, "value": value}
                for name, value in self.updates.items()
            ],
        }

        await self.session.send(message)

    def __len__(self) -> int:
        """Number of pending updates."""
        return len(self.updates)

    def __bool__(self) -> bool:
        """True if there are pending updates."""
        return bool(self.updates)


async def batch_updates(
    session: "Session",
    updates: dict["Signal[Any]", Any],
) -> None:
    """
    Helper function to batch multiple updates at once.

    Args:
        session: The session to update
        updates: Dict mapping signals to their new values

    Example:
        await batch_updates(session, {
            count: 10,
            name: "John",
            active: True,
        })
    """
    b = Batch(session)
    for signal, value in updates.items():
        b.set(signal, value)
    await b.commit()
