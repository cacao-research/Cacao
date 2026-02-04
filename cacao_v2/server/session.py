"""
Session management for Cacao v2.

Each WebSocket connection gets a unique Session that isolates state
between users. Sessions track their associated signals and clean up
when the connection closes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import asyncio

if TYPE_CHECKING:
    from starlette.websockets import WebSocket


@dataclass
class Session:
    """
    Represents a single client session (WebSocket connection).

    Sessions provide isolation between users - each session has its own
    signal values, ensuring that state doesn't leak between clients.

    Attributes:
        id: Unique session identifier
        websocket: The WebSocket connection for this session
        created_at: When the session was created
        metadata: Arbitrary session metadata
    """

    id: str
    websocket: "WebSocket | None" = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    _pending_updates: dict[str, Any] = field(default_factory=dict)
    _update_task: asyncio.Task[None] | None = field(default=None, repr=False)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Session):
            return self.id == other.id
        return False

    async def send_state(self, state: dict[str, Any]) -> None:
        """
        Send a state update to the client.

        Args:
            state: The state to send
        """
        if self.websocket is None:
            return

        await self.websocket.send_json({
            "type": "update",
            "changes": state,
        })

    async def send_init(self, state: dict[str, Any]) -> None:
        """
        Send the initial state snapshot to the client.

        Args:
            state: The full state snapshot
        """
        if self.websocket is None:
            return

        await self.websocket.send_json({
            "type": "init",
            "state": state,
            "sessionId": self.id,
        })

    def queue_update(self, key: str, value: Any) -> None:
        """
        Queue a state update to be batched and sent.

        Updates are batched to avoid sending too many messages.

        Args:
            key: The signal name
            value: The new value
        """
        self._pending_updates[key] = value

        # Schedule send if not already scheduled
        if self._update_task is None or self._update_task.done():
            self._update_task = asyncio.create_task(self._flush_updates())

    async def _flush_updates(self) -> None:
        """Send all pending updates."""
        # Small delay to batch updates
        await asyncio.sleep(0.01)  # 10ms batching window

        if self._pending_updates and self.websocket is not None:
            updates = self._pending_updates.copy()
            self._pending_updates.clear()
            await self.send_state(updates)


class SessionManager:
    """
    Manages all active sessions.

    The SessionManager tracks all connected clients and provides
    methods for session lifecycle management.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(self, websocket: "WebSocket | None" = None) -> Session:
        """
        Create a new session.

        Args:
            websocket: The WebSocket connection for this session

        Returns:
            The new Session
        """
        session_id = str(uuid.uuid4())
        session = Session(id=session_id, websocket=websocket)
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        """
        Get a session by ID.

        Args:
            session_id: The session ID to look up

        Returns:
            The Session if found, None otherwise
        """
        return self._sessions.get(session_id)

    def remove(self, session_id: str) -> Session | None:
        """
        Remove a session.

        This should be called when a WebSocket connection closes.

        Args:
            session_id: The session ID to remove

        Returns:
            The removed Session if found, None otherwise
        """
        session = self._sessions.pop(session_id, None)
        if session is not None:
            # Clean up signal values for this session
            from .signal import Signal
            Signal.clear_all_for_session(session)
        return session

    def get_all(self) -> list[Session]:
        """Get all active sessions."""
        return list(self._sessions.values())

    @property
    def count(self) -> int:
        """Number of active sessions."""
        return len(self._sessions)

    async def broadcast(self, message: dict[str, Any]) -> None:
        """
        Broadcast a message to all sessions.

        Args:
            message: The message to broadcast
        """
        for session in self._sessions.values():
            if session.websocket is not None:
                try:
                    await session.websocket.send_json(message)
                except Exception:
                    pass  # Ignore send errors during broadcast
