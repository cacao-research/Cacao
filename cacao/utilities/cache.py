"""
Cache utilities for the Cacao framework.
Provides caching decorators to memoize function results.
"""

from functools import wraps
from typing import Callable, TypeVar, Dict, Tuple, Any

T = TypeVar('T')

def cache(func: Callable[..., T]) -> Callable[..., T]:
    """
    A simple caching decorator that memoizes function results based on arguments.
    """
    cached_results: Dict[Tuple[Any, ...], T] = {}

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = args + tuple(sorted(kwargs.items()))
        if key not in cached_results:
            cached_results[key] = func(*args, **kwargs)
        return cached_results[key]
    
    return wrapper
