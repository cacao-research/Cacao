"""
Session persistence for Cacao v2.

Saves and restores session signal state across server restarts.
When a client reconnects, its session state is restored from disk
if the session ID matches a previously saved session.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .log import get_logger

if TYPE_CHECKING:
    from .session import Session

_logger = get_logger("cacao.session_persist")

# Module-level persistence store
_store: SessionStore | None = None


class SessionStore:
    """
    Persists session signal state to disk so that sessions survive
    server restarts.

    State is saved per-session as a JSON file in the storage directory.
    On reconnect, the client can send its previous session ID to restore
    state.

    Example:
        store = SessionStore(".cacao_sessions")
        await store.save(session)
        state = await store.load(session_id)
    """

    def __init__(self, directory: str | Path = ".cacao_sessions") -> None:
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._save_lock = asyncio.Lock()

    def _session_path(self, session_id: str) -> Path:
        """Get file path for a session's state."""
        safe_id = session_id.replace("/", "_").replace("\\", "_")
        return self._dir / f"{safe_id}.json"

    async def save(self, session: Session) -> None:
        """
        Save all signal values for a session to disk.

        Args:
            session: The session to save
        """
        from .signal import Signal

        state: dict[str, Any] = {}
        for name, signal in Signal.get_all_signals().items():
            if hasattr(signal, "get"):
                value = signal.get(session)
                try:
                    json.dumps(value)  # Verify it's serializable
                    state[name] = value
                except (TypeError, ValueError):
                    continue  # Skip non-serializable values

        path = self._session_path(session.id)
        async with self._save_lock:
            try:
                data = {
                    "session_id": session.id,
                    "state": state,
                    "metadata": {
                        k: v
                        for k, v in session.metadata.items()
                        if isinstance(v, (str, int, float, bool, type(None)))
                    },
                }
                path.write_text(json.dumps(data))
                _logger.debug(
                    "Saved session %s (%d signals)",
                    session.id[:8],
                    len(state),
                    extra={"label": "persist"},
                )
            except Exception as e:
                _logger.warning(
                    "Failed to save session %s: %s",
                    session.id[:8],
                    e,
                    extra={"label": "persist"},
                )

    async def load(self, session_id: str) -> dict[str, Any] | None:
        """
        Load saved state for a session ID.

        Args:
            session_id: The session ID to restore

        Returns:
            Dict with 'state' and 'metadata', or None if not found
        """
        path = self._session_path(session_id)
        if not path.exists():
            return None

        try:
            data: dict[str, Any] = json.loads(path.read_text())
            _logger.debug("Loaded session %s", session_id[:8], extra={"label": "persist"})
            return data
        except (OSError, json.JSONDecodeError) as e:
            _logger.warning(
                "Failed to load session %s: %s",
                session_id[:8],
                e,
                extra={"label": "persist"},
            )
            return None

    async def remove(self, session_id: str) -> None:
        """Remove persisted state for a session."""
        path = self._session_path(session_id)
        if path.exists():
            try:
                path.unlink()
            except OSError:
                pass

    async def save_all(self, sessions: list[Session]) -> int:
        """
        Save all active sessions. Used during graceful shutdown.

        Returns:
            Number of sessions saved
        """
        count = 0
        for session in sessions:
            await self.save(session)
            count += 1
        return count

    def cleanup(self, *, max_age_seconds: float = 86400) -> int:
        """
        Remove session files older than max_age.

        Returns:
            Number of files removed
        """
        import time

        count = 0
        now = time.time()
        for path in self._dir.glob("*.json"):
            try:
                if (now - path.stat().st_mtime) > max_age_seconds:
                    path.unlink()
                    count += 1
            except OSError:
                continue
        return count


def get_session_store() -> SessionStore | None:
    """Get the global session store."""
    return _store


def enable_session_persistence(directory: str | Path = ".cacao_sessions") -> SessionStore:
    """
    Enable session persistence.

    Args:
        directory: Directory to store session state files

    Returns:
        The configured SessionStore
    """
    global _store
    _store = SessionStore(directory)
    return _store
