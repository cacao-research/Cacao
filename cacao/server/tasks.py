"""
Background task queue for Cacao v2.

Provides a non-blocking task queue that runs async tasks without blocking
the event loop. Tasks are tracked, can be cancelled, and report status.
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .log import get_logger

_logger = get_logger("cacao.tasks")


class TaskStatus(Enum):
    """Status of a background task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskInfo:
    """Information about a background task."""

    id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: Any = None
    error: str | None = None


class BackgroundTaskQueue:
    """
    A background task queue that runs async callables without blocking
    the WebSocket event loop.

    Example:
        queue = BackgroundTaskQueue(max_workers=4)
        await queue.start()

        task_id = await queue.submit(my_heavy_func, name="data-export")
        info = queue.get_task(task_id)

        await queue.shutdown()
    """

    def __init__(self, *, max_workers: int = 8) -> None:
        """
        Create a background task queue.

        Args:
            max_workers: Maximum concurrent tasks
        """
        self._max_workers = max_workers
        self._semaphore: asyncio.Semaphore | None = None
        self._tasks: dict[str, TaskInfo] = {}
        self._async_tasks: dict[str, asyncio.Task[Any]] = {}
        self._running = False

    async def start(self) -> None:
        """Start the task queue."""
        self._semaphore = asyncio.Semaphore(self._max_workers)
        self._running = True
        _logger.debug(
            "Task queue started (max_workers=%d)", self._max_workers, extra={"label": "tasks"}
        )

    async def submit(
        self,
        coro_func: Callable[..., Awaitable[Any]],
        *args: Any,
        name: str = "",
        **kwargs: Any,
    ) -> str:
        """
        Submit an async callable to run in the background.

        Args:
            coro_func: Async function to run
            *args: Positional arguments for the function
            name: Human-readable task name
            **kwargs: Keyword arguments for the function

        Returns:
            Task ID for tracking
        """
        if not self._running:
            raise RuntimeError("Task queue is not running. Call start() first.")

        task_id = str(uuid.uuid4())[:8]
        info = TaskInfo(id=task_id, name=name or coro_func.__name__)
        self._tasks[task_id] = info

        async_task = asyncio.create_task(self._run_task(task_id, coro_func, *args, **kwargs))
        self._async_tasks[task_id] = async_task

        _logger.debug("Task %s submitted: %s", task_id, info.name, extra={"label": "tasks"})
        return task_id

    async def _run_task(
        self,
        task_id: str,
        coro_func: Callable[..., Awaitable[Any]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run a task with semaphore-based concurrency control."""
        info = self._tasks[task_id]

        assert self._semaphore is not None
        async with self._semaphore:
            info.status = TaskStatus.RUNNING
            info.started_at = datetime.now()

            try:
                info.result = await coro_func(*args, **kwargs)
                info.status = TaskStatus.COMPLETED
            except asyncio.CancelledError:
                info.status = TaskStatus.CANCELLED
            except Exception as e:
                info.status = TaskStatus.FAILED
                info.error = str(e)
                _logger.warning("Task %s failed: %s", task_id, e, extra={"label": "tasks"})
            finally:
                info.completed_at = datetime.now()
                self._async_tasks.pop(task_id, None)

    def get_task(self, task_id: str) -> TaskInfo | None:
        """Get info about a task by ID."""
        return self._tasks.get(task_id)

    def cancel(self, task_id: str) -> bool:
        """
        Cancel a running or pending task.

        Returns:
            True if the task was cancelled
        """
        async_task = self._async_tasks.get(task_id)
        if async_task and not async_task.done():
            async_task.cancel()
            return True
        return False

    @property
    def pending_count(self) -> int:
        """Number of pending or running tasks."""
        return sum(
            1
            for info in self._tasks.values()
            if info.status in (TaskStatus.PENDING, TaskStatus.RUNNING)
        )

    async def shutdown(self, *, timeout: float = 10.0) -> None:
        """
        Shut down the task queue, waiting for running tasks to complete.

        Args:
            timeout: Maximum seconds to wait for tasks to finish
        """
        self._running = False

        active = [t for t in self._async_tasks.values() if not t.done()]
        if active:
            _logger.info(
                "Waiting for %d background tasks to finish...",
                len(active),
                extra={"label": "tasks"},
            )
            done, pending = await asyncio.wait(active, timeout=timeout)
            for task in pending:
                task.cancel()
            if pending:
                _logger.warning(
                    "Cancelled %d tasks after timeout", len(pending), extra={"label": "tasks"}
                )

        self._tasks.clear()
        self._async_tasks.clear()
        _logger.debug("Task queue shut down", extra={"label": "tasks"})

    def cleanup_completed(self, *, max_age_seconds: float = 3600) -> int:
        """
        Remove completed/failed/cancelled tasks older than max_age.

        Returns:
            Number of tasks removed
        """
        now = datetime.now()
        to_remove = []
        for task_id, info in self._tasks.items():
            if info.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
                if (
                    info.completed_at
                    and (now - info.completed_at).total_seconds() > max_age_seconds
                ):
                    to_remove.append(task_id)

        for task_id in to_remove:
            self._tasks.pop(task_id, None)
            self._async_tasks.pop(task_id, None)

        return len(to_remove)
