"""
Metrics module for the Cacao framework.
Provides basic performance tracking and metrics reporting functionalities.
"""

import time
from typing import Callable, Dict

class Metrics:
    """
    A simple metrics tracker for timing function executions.
    """
    def __init__(self):
        self.records: Dict[str, float] = {}

    def track(self, name: str, func: Callable, *args, **kwargs):
        """
        Tracks the execution time of the given function.
        """
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        self.records[name] = elapsed
        print(f"Metric [{name}]: {elapsed:.4f} seconds")
        return result

metrics = Metrics()
