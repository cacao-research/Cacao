"""
State management system for Cacao.
Provides reactive state handling with automatic UI updates.
"""

from typing import Any, Callable, List, Dict, TypeVar, Generic, Optional
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

class GlobalStateManager:
    """
    Central registry for managing global application state.
    Ensures state consistency across components.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalStateManager, cls).__new__(cls)
            cls._instance._states: Dict[str, 'State'] = {}
            cls._instance._server_state: Dict[str, Any] = {}
        return cls._instance
    
    def register(self, name: str, state: 'State') -> None:
        """Register a named state"""
        self._states[name] = state
    
    def get(self, name: str, default: Optional[Any] = None) -> Optional['State']:
        """Get a state by name"""
        return self._states.get(name)
    
    def update_from_server(self, server_state: Dict[str, Any]) -> None:
        """Update local states from server state dictionary"""
        self._server_state.update(server_state)
        for name, value in server_state.items():
            if name in self._states:
                # Use set method to trigger full state update mechanism
                self._states[name].set(value)
            else:
                # Create new state if it doesn't exist
                new_state = State(value, name=name)
                self.register(name, new_state)
            
    def get_server_state(self) -> Dict[str, Any]:
        """Return current server state"""
        return self._server_state
            
    def get_or_create(self, name: str, initial_value: Any) -> 'State':
        """Get existing state or create a new one"""
        if name in self._states:
            return self._states[name]
        
        # Check if there's a server value for this state
        if name in self._server_state:
            initial_value = self._server_state[name]
            
        # Create new state and register it
        state = State(initial_value)
        self.register(name, state)
        return state


# Global state manager instance
global_state = GlobalStateManager()


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
    
    def __init__(self, initial_value: T, name: Optional[str] = None):
        self._value = initial_value
        self._subscribers: List[Callable[[T], None]] = []
        self._ui_subscribers: List[weakref.ref] = []
        self._change_listeners: List[Callable[[T, T], None]] = []
        self._name = name
        
        # Register with global state manager if named
        if name:
            global_state.register(name, self)
        
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
        # Add logging to track state changes
        import inspect
        frame = inspect.currentframe()
        caller = inspect.getouterframes(frame)[1]
        #print(f"State.set called for {self._name} from {caller.function} in {caller.filename}")
        #print(f"  Old value: {self._value}, New value: {new_value}")
        
        # Delegate to update method to avoid code duplication
        self.update(new_value)
        
    def update(self, new_value: T) -> None:
        """
        Alias for set() - updates the state value and notifies subscribers.
        
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
        
        # Trigger global state update
        if self._name:
            global_state.update_from_server({self._name: new_value})
    
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
                    # Attempt to call handle_state_change synchronously
                    # If it's an async method, it will be handled accordingly
                    if asyncio.iscoroutinefunction(subscriber.handle_state_change):
                        asyncio.create_task(subscriber.handle_state_change(change))
                    else:
                        subscriber.handle_state_change(change)
                except Exception as e:
                    print(f"Error notifying UI subscriber: {e}")
        
        # Broadcast state change to server if named state
        if self._name:
            try:
                # Use global state manager to handle server updates
                global_state._server_state[self._name] = self._value
            except Exception as e:
                print(f"Error updating server state: {e}")

    def to_json(self) -> str:
        """Convert state to JSON string."""
        return json.dumps({
            "value": self._value,
            "name": self._name,
            "subscribers": len(self._subscribers),
            "ui_subscribers": len(self._ui_subscribers)
        })
        
    def __repr__(self) -> str:
        return f"State({self._value})"

# Helper function to get or create a global state
def get_state(name: str, initial_value: T) -> State[T]:
    """
    Get or create a global named state
    
    Args:
        name: The name of the state
        initial_value: Initial value if the state doesn't exist
        
    Returns:
        The state instance
    """
    return global_state.get_or_create(name, initial_value)
