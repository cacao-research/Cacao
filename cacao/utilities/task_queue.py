"""
Task queue utilities for the Cacao framework.
Manages asynchronous task execution using asyncio.
"""

import asyncio
from typing import Callable, Any

class TaskQueue:
    """
    A simple asynchronous task queue.
    """
    def __init__(self, max_workers: int = 5) -> None:
        self.queue = asyncio.Queue()
        self.max_workers = max_workers
        self.workers = []

    async def _worker(self) -> None:
        while True:
            task: Callable[[], Any] = await self.queue.get()
            try:
                result = task()
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                print(f"Task error: {e}")
            finally:
                self.queue.task_done()

    async def start(self) -> None:
        """
        Start worker tasks.
        """
        for _ in range(self.max_workers):
            worker_task = asyncio.create_task(self._worker())
            self.workers.append(worker_task)

    async def add_task(self, task: Callable[[], Any]) -> None:
        """
        Add a new task to the queue.
        """
        await self.queue.put(task)

    async def join(self) -> None:
        """
        Wait until all tasks are completed.
        """
        await self.queue.join()

    async def stop(self) -> None:
        """
        Cancel all worker tasks.
        """
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
