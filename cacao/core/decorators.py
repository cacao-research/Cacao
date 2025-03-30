"""
Decorators module for the Cacao framework.
Provides syntactic sugar for registering routes and auto-documenting components.
"""

from typing import Callable, Dict, Any
import functools

# Global registry for route handlers
ROUTES: Dict[str, Callable] = {}
# Global registry for event handlers
EVENT_HANDLERS: Dict[str, Callable] = {}

# Import icon processing function
from ..utilities.icons import process_icons_in_component

class MixDecorator:
    """
    Class-based decorator that provides both route and event registration.
    """
    
    def __call__(self, path: str) -> Callable:
        """
        Register a function as a route with the given path.
        
        Usage:
            @mix("/")
            def home():
                return { ... }  # JSON UI definition
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Always call the original function to get fresh data
                result = func(*args, **kwargs)
                
                # Process icons in the component tree
                if isinstance(result, dict):
                    result = process_icons_in_component(result)
                
                return result
            
            # Register the wrapped function
            ROUTES[path] = wrapper
            return wrapper
        return decorator
    
    def event(self, event_name: str) -> Callable:
        """
        Register a function as an event handler.
        
        Usage:
            @mix.event("button_click")
            async def handle_click(event):
                # Handle event
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            # Register the event handler
            EVENT_HANDLERS[event_name] = wrapper
            return wrapper
        return decorator

# Create the singleton instance
mix = MixDecorator()

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

def get_event_handlers():
    """Get all registered event handlers."""
    return EVENT_HANDLERS

def register_event_handler(event_name: str, handler: Callable):
    """Manually register an event handler."""
    EVENT_HANDLERS[event_name] = handler

def handle_event(event_name: str, event_data=None):
    """Process an event with the registered handler."""
    if event_name in EVENT_HANDLERS:
        handler = EVENT_HANDLERS[event_name]
        return handler(event_data)
    return None
