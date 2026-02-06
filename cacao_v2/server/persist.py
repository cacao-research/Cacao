"""
Signal persistence for Cacao v2.

Persist allows signals to be saved to and restored from storage,
enabling state to survive server restarts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar, Generic
from abc import ABC, abstractmethod
import json
import asyncio
from pathlib import Path

if TYPE_CHECKING:
    from .session import Session
    from .signal import Signal

T = TypeVar("T")


class StorageBackend(Protocol):
    """Protocol for storage backends."""

    async def get(self, key: str) -> Any | None:
        """Get a value from storage."""
        ...

    async def set(self, key: str, value: Any) -> None:
        """Set a value in storage."""
        ...

    async def delete(self, key: str) -> None:
        """Delete a value from storage."""
        ...

    async def keys(self, prefix: str = "") -> list[str]:
        """List all keys with optional prefix."""
        ...


class MemoryStorage:
    """
    In-memory storage backend.

    Values are lost when the server restarts.
    Useful for testing or caching.
    """

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    async def get(self, key: str) -> Any | None:
        return self._data.get(key)

    async def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    async def delete(self, key: str) -> None:
        self._data.pop(key, None)

    async def keys(self, prefix: str = "") -> list[str]:
        return [k for k in self._data.keys() if k.startswith(prefix)]

    def clear(self) -> None:
        """Clear all data."""
        self._data.clear()


class FileStorage:
    """
    File-based storage backend.

    Stores each key as a separate JSON file in a directory.
    Simple but effective for small-scale persistence.
    """

    def __init__(self, directory: str | Path) -> None:
        """
        Create a file storage backend.

        Args:
            directory: Directory to store files in
        """
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    def _key_to_path(self, key: str) -> Path:
        """Convert a key to a file path."""
        # Sanitize key for filesystem
        safe_key = key.replace("/", "_").replace("\\", "_")
        return self._dir / f"{safe_key}.json"

    async def get(self, key: str) -> Any | None:
        path = self._key_to_path(key)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, IOError):
            return None

    async def set(self, key: str, value: Any) -> None:
        path = self._key_to_path(key)
        path.write_text(json.dumps(value))

    async def delete(self, key: str) -> None:
        path = self._key_to_path(key)
        if path.exists():
            path.unlink()

    async def keys(self, prefix: str = "") -> list[str]:
        keys = []
        for path in self._dir.glob("*.json"):
            key = path.stem
            if key.startswith(prefix):
                keys.append(key)
        return keys


class Persist(Generic[T]):
    """
    Wrapper that adds persistence to a signal.

    Persist automatically saves signal values to storage and restores
    them when sessions reconnect.

    Example:
        storage = FileStorage("./data")

        user_prefs = Signal({}, name="user_prefs")
        persist = Persist(user_prefs, storage, key_prefix="prefs")

        # Values are automatically saved when changed
        # and restored when sessions reconnect
    """

    def __init__(
        self,
        signal: "Signal[T]",
        storage: StorageBackend,
        *,
        key_prefix: str = "",
        debounce_ms: int = 500,
        serialize: Any | None = None,
        deserialize: Any | None = None,
    ) -> None:
        """
        Create a persistent signal wrapper.

        Args:
            signal: The signal to persist
            storage: Storage backend to use
            key_prefix: Prefix for storage keys
            debounce_ms: Debounce saves by this many milliseconds
            serialize: Custom serialization function
            deserialize: Custom deserialization function
        """
        self._signal = signal
        self._storage = storage
        self._key_prefix = key_prefix
        self._debounce_ms = debounce_ms
        self._serialize = serialize or (lambda x: x)
        self._deserialize = deserialize or (lambda x: x)

        self._pending_saves: dict[str, asyncio.Task[None]] = {}

        # Subscribe to signal changes
        self._unsubscribe = signal.subscribe(self._on_change)

    @property
    def signal(self) -> "Signal[T]":
        """The underlying signal."""
        return self._signal

    def _storage_key(self, session_id: str) -> str:
        """Get the storage key for a session."""
        prefix = f"{self._key_prefix}:" if self._key_prefix else ""
        return f"{prefix}{self._signal.name}:{session_id}"

    def _on_change(self, session_id: str, value: T) -> None:
        """Handle signal change - schedule save."""
        # Cancel any pending save for this session
        if session_id in self._pending_saves:
            self._pending_saves[session_id].cancel()

        # Schedule a new save
        async def save_after_delay() -> None:
            await asyncio.sleep(self._debounce_ms / 1000)
            await self._save(session_id, value)

        self._pending_saves[session_id] = asyncio.create_task(save_after_delay())

    async def _save(self, session_id: str, value: T) -> None:
        """Save a value to storage."""
        try:
            key = self._storage_key(session_id)
            serialized = self._serialize(value)
            await self._storage.set(key, serialized)
        except Exception as e:
            print(f"Persist save error for {self._signal.name}: {e}")
        finally:
            self._pending_saves.pop(session_id, None)

    async def restore(self, session: "Session") -> T | None:
        """
        Restore a signal's value from storage for a session.

        Args:
            session: The session to restore for

        Returns:
            The restored value, or None if not found
        """
        try:
            key = self._storage_key(session.id)
            stored = await self._storage.get(key)
            if stored is not None:
                value = self._deserialize(stored)
                self._signal.set(session, value)
                return value
        except Exception as e:
            print(f"Persist restore error for {self._signal.name}: {e}")
        return None

    async def delete(self, session: "Session") -> None:
        """
        Delete persisted data for a session.

        Args:
            session: The session to delete data for
        """
        try:
            key = self._storage_key(session.id)
            await self._storage.delete(key)
        except Exception as e:
            print(f"Persist delete error for {self._signal.name}: {e}")

    def dispose(self) -> None:
        """Stop persisting and cancel pending saves."""
        self._unsubscribe()
        for task in self._pending_saves.values():
            task.cancel()
        self._pending_saves.clear()


class PersistManager:
    """
    Manager for multiple persistent signals.

    Provides bulk restore and cleanup operations.

    Example:
        storage = FileStorage("./data")
        manager = PersistManager(storage)

        # Register signals for persistence
        manager.add(user_prefs)
        manager.add(settings)

        # Restore all on session connect
        await manager.restore_all(session)
    """

    def __init__(self, storage: StorageBackend, *, key_prefix: str = "") -> None:
        """
        Create a persist manager.

        Args:
            storage: Storage backend to use
            key_prefix: Prefix for all storage keys
        """
        self._storage = storage
        self._key_prefix = key_prefix
        self._persists: dict[str, Persist[Any]] = {}

    def add(
        self,
        signal: "Signal[Any]",
        *,
        debounce_ms: int = 500,
    ) -> Persist[Any]:
        """
        Add a signal to be persisted.

        Args:
            signal: The signal to persist
            debounce_ms: Debounce saves by this many milliseconds

        Returns:
            The Persist wrapper
        """
        persist = Persist(
            signal,
            self._storage,
            key_prefix=self._key_prefix,
            debounce_ms=debounce_ms,
        )
        self._persists[signal.name] = persist
        return persist

    async def restore_all(self, session: "Session") -> dict[str, Any]:
        """
        Restore all persisted signals for a session.

        Args:
            session: The session to restore for

        Returns:
            Dict of signal names to restored values
        """
        restored = {}
        for name, persist in self._persists.items():
            value = await persist.restore(session)
            if value is not None:
                restored[name] = value
        return restored

    async def delete_all(self, session: "Session") -> None:
        """
        Delete all persisted data for a session.

        Args:
            session: The session to delete data for
        """
        for persist in self._persists.values():
            await persist.delete(session)

    def dispose(self) -> None:
        """Dispose all persist wrappers."""
        for persist in self._persists.values():
            persist.dispose()
        self._persists.clear()
