# State Management

Cacao provides a reactive state system that automatically updates the UI when data changes.

## The State Class

`State[T]` is a generic container for reactive values:

```python
from cacao import State

# Create state with initial values
counter = State(0)
user_name = State("Guest")
items = State([])
settings = State({"theme": "dark", "fontSize": 14})
```

## Reading State

Access the current value with `.value`:

```python
counter = State(10)
print(counter.value)  # 10

user = State({"name": "Alice", "role": "admin"})
print(user.value["name"])  # Alice
```

## Updating State

### Using `set()`

Replace the entire value:

```python
counter = State(0)
counter.set(5)  # counter.value is now 5

items = State(["a", "b"])
items.set(["x", "y", "z"])  # Replace entire list
```

### Using `update()`

For dictionaries and objects, merge updates:

```python
settings = State({"theme": "light", "fontSize": 14})
settings.update({"theme": "dark"})
# settings.value is now {"theme": "dark", "fontSize": 14}
```

## Subscribing to Changes

React to state changes with the `@subscribe` decorator:

```python
counter = State(0)

@counter.subscribe
def on_counter_change(new_value: int) -> None:
    print(f"Counter changed to: {new_value}")
    # Could also trigger side effects like logging, analytics, etc.

counter.set(5)  # Prints: "Counter changed to: 5"
```

Multiple subscribers are supported:

```python
@counter.subscribe
def log_change(value):
    print(f"Log: {value}")

@counter.subscribe
def validate_change(value):
    if value < 0:
        print("Warning: negative value!")
```

## State in Event Handlers

The most common pattern is updating state in event handlers:

```python
from cacao import State
from typing import Dict, Any, Optional

app = cacao.App()
counter = State(0)

@app.event("increment")
def handle_increment(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    counter.set(counter.value + 1)
    return {"counter": counter.value}  # Return updated state to client

@app.event("decrement")
def handle_decrement(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    counter.set(counter.value - 1)
    return {"counter": counter.value}
```

## State in Components

Components can access state and receive UI state from the client:

```python
from cacao import Component, State

counter = State(0)

class Counter(Component):
    def render(self, ui_state=None):
        # ui_state contains client-side state after updates
        value = counter.value
        if ui_state and "counter" in ui_state:
            value = ui_state["counter"]

        return {
            "type": "div",
            "component_type": "counter",  # For state isolation
            "props": {
                "children": [
                    {"type": "text", "props": {"content": str(value)}},
                    {"type": "button", "props": {"label": "+", "action": "increment"}}
                ]
            }
        }
```

## Component Type for State Isolation

The `component_type` field helps isolate state updates to specific components:

```python
{
    "type": "div",
    "component_type": "user-profile",  # Unique identifier
    "props": {...}
}
```

When the server returns state updates, only components matching the `component_type` will re-render.

## Best Practices

### 1. Keep State Close to Where It's Used

```python
# Good: State defined near its usage
class UserProfile(Component):
    def __init__(self):
        self.user = State({"name": "", "email": ""})
```

### 2. Use Meaningful State Names

```python
# Good
user_authenticated = State(False)
cart_items = State([])

# Avoid
x = State(False)
data = State([])
```

### 3. Return State in Event Handlers

Always return the updated state so the client stays in sync:

```python
@app.event("update_user")
def handle_update(event_data=None):
    # Update state
    user.update(event_data)
    # Return updated state
    return {"user": user.value}
```

### 4. Use Type Hints

```python
from cacao import State
from typing import List, Dict

counter: State[int] = State(0)
users: State[List[Dict]] = State([])
```

## Global State Manager

For advanced use cases, access the global state manager:

```python
from cacao.core.state import GlobalStateManager

manager = GlobalStateManager()

# Get all state values
all_state = manager.get_state()

# Reset all state
manager.reset()
```

## Next Steps

- [Routing](routing.md) - Event handlers and navigation
- [Components](components.md) - Building with state-aware components
