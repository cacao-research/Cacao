"""
State management system for Cacao.
Provides reactive state handling with automatic UI updates.
"""

from typing import Any, Callable, List, TypeVar, Generic
from dataclasses import dataclass
import asyncio
import json
import weakref

T = TypeVar('T')

@dataclass
class StateChange:
    """Represents a change in state."""
    old_value: Any
    new_value: Any
    path: str = ''

class State(Generic[T]):
    """
    Reactive state container that automatically triggers UI updates
    when the value changes.
    
    Usage:
        counter = State(0)
        counter.set(counter.value + 1)  # Triggers UI update
        
        @counter.subscribe
        def on_change(new_value):
            print(f"Counter is now: {new_value}")
    """
    
    def __init__(self, initial_value: T):
        self._value = initial_value
        self._subscribers: List[Callable[[T], None]] = []
        self._ui_subscribers: List[weakref.ref] = []
        self._change_listeners: List[Callable[[T, T], None]] = []
        
    @property
    def value(self) -> T:
        """Get the current state value."""
        return self._value
        
    def set(self, new_value: T) -> None:
        """
        Update the state value and notify subscribers.
        
        Args:
            new_value: The new value to set
        """
        if new_value == self._value:
            return
            
        old_value = self._value
        self._value = new_value
        
        # Notify direct subscribers
        for subscriber in self._subscribers:
            try:
                subscriber(new_value)
            except Exception as e:
                print(f"Error in state subscriber: {e}")
        
        # Notify change listeners
        for listener in self._change_listeners:
            try:
                listener(old_value, new_value)
            except Exception as e:
                print(f"Error in state change listener: {e}")
        
        # Notify UI subscribers
        change = StateChange(old_value, new_value)
        self._notify_ui(change)
    
    def subscribe(self, callback: Callable[[T], None]) -> Callable[[T], None]:
        """
        Subscribe to state changes.
        
        Args:
            callback: Function to call when state changes
            
        Returns:
            The callback function (can be used as a decorator)
        """
        self._subscribers.append(callback)
        return callback
    
    def on_change(self, listener: Callable[[T, T], None]) -> Callable[[T, T], None]:
        """
        Add a change listener that receives both old and new values.
        
        Args:
            listener: Function to call when state changes
            
        Returns:
            The listener function
        """
        self._change_listeners.append(listener)
        return listener
        
    def _notify_ui(self, change: StateChange) -> None:
        """Notify UI subscribers of state changes."""
        # Clean up dead references
        self._ui_subscribers = [ref for ref in self._ui_subscribers if ref() is not None]
        
        # Notify remaining subscribers
        for ref in self._ui_subscribers:
            subscriber = ref()
            if subscriber is not None:
                try:
                    # Use create_task to avoid blocking
                    asyncio.create_task(subscriber.handle_state_change(change))
                except Exception as e:
                    print(f"Error notifying UI subscriber: {e}")

    def to_json(self) -> str:
        """Convert state to JSON string."""
        return json.dumps({
            "value": self._value,
            "subscribers": len(self._subscribers),
            "ui_subscribers": len(self._ui_subscribers)
        })
        
    def __repr__(self) -> str:
        return f"State({self._value})"
