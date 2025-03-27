"""
Decorators module for the Cacao framework.
Provides syntactic sugar for registering routes and auto-documenting components.
"""

from typing import Callable, Dict
import functools

# Global registry for route handlers
ROUTES: Dict[str, Callable] = {}

def mix(path: str) -> Callable:
    """
    Decorator that registers a function as a route with the given path.
    
    Usage:
        @mix("/")
        def home():
            return { ... }  # JSON UI definition
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Always call the original function to get fresh data
            return func(*args, **kwargs)
        
        # Register the wrapped function
        ROUTES[path] = wrapper
        return wrapper
    return decorator

def page(route: str) -> Callable:
    """
    Alias for mix, for semantic clarity.
    """
    return mix(route)

def documented(func: Callable) -> Callable:
    """
    Decorator that attaches auto-documentation metadata to a function or component.
    """
    func.__doc__ = (func.__doc__ or "") + "\n\n[Auto-documented by Cacao]"
    return func

def clear_routes():
    """Clear all registered routes."""
    ROUTES.clear()

def register_route(path: str, handler: Callable):
    """Manually register a route handler."""
    ROUTES[path] = handler
