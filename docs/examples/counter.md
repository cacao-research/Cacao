# Counter Example

A simple interactive counter demonstrating state management and event handling.

## Overview

This example shows how to:

- Create reactive state with `State`
- Handle button click events
- Update UI based on state changes

## Running the Example

```bash
cacao dev examples/counter_example.py
```

Open `http://localhost:1634` in your browser.

## Code

```python
import cacao
from cacao import State
from typing import Dict, Any, Optional

app = cacao.App()

# Create counter state
counter = State(0)

@counter.subscribe
def on_counter_change(value: int) -> None:
    """Log counter changes."""
    print(f"Counter: {value}")

@app.event("increment")
def handle_increment(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle increment button click."""
    counter.set(counter.value + 1)
    return {"counter": counter.value}

@app.event("decrement")
def handle_decrement(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle decrement button click."""
    counter.set(counter.value - 1)
    return {"counter": counter.value}

@app.mix("/")
def home() -> Dict[str, Any]:
    """Home page with counter."""
    return {
        "type": "div",
        "props": {
            "style": {
                "minHeight": "100vh",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "background": "linear-gradient(135deg, #2c1810 0%, #3a1f14 100%)",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Cacao Counter",
                    "style": {
                        "fontSize": "36px",
                        "color": "#f0be9b",
                        "marginBottom": "40px"
                    }
                }
            },
            {
                "type": "div",
                "component_type": "counter",
                "props": {
                    "style": {
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "24px",
                        "padding": "32px",
                        "background": "rgba(255, 255, 255, 0.1)",
                        "borderRadius": "16px"
                    },
                    "children": [
                        {
                            "type": "button",
                            "props": {
                                "label": "-",
                                "action": "decrement",
                                "style": {
                                    "fontSize": "24px",
                                    "width": "60px",
                                    "height": "60px",
                                    "borderRadius": "50%",
                                    "border": "2px solid rgba(255,255,255,0.3)",
                                    "background": "rgba(255,255,255,0.1)",
                                    "color": "white",
                                    "cursor": "pointer"
                                }
                            }
                        },
                        {
                            "type": "text",
                            "props": {
                                "content": str(counter.value),
                                "style": {
                                    "fontSize": "64px",
                                    "fontWeight": "bold",
                                    "color": "white",
                                    "minWidth": "120px",
                                    "textAlign": "center"
                                }
                            }
                        },
                        {
                            "type": "button",
                            "props": {
                                "label": "+",
                                "action": "increment",
                                "style": {
                                    "fontSize": "24px",
                                    "width": "60px",
                                    "height": "60px",
                                    "borderRadius": "50%",
                                    "border": "2px solid rgba(255,255,255,0.3)",
                                    "background": "rgba(255,255,255,0.1)",
                                    "color": "white",
                                    "cursor": "pointer"
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }

if __name__ == "__main__":
    app.brew()
```

## Key Concepts

### 1. State Management

```python
from cacao import State

counter = State(0)  # Initial value of 0
```

The `State` class creates a reactive container. When its value changes, subscribed functions are called.

### 2. Subscribing to Changes

```python
@counter.subscribe
def on_counter_change(value: int) -> None:
    print(f"Counter: {value}")
```

The `@subscribe` decorator registers a function to be called whenever the state changes.

### 3. Event Handlers

```python
@app.event("increment")
def handle_increment(event_data=None):
    counter.set(counter.value + 1)
    return {"counter": counter.value}
```

Event handlers:
- Are registered with `@app.event("name")`
- Receive `event_data` from the client
- Should return updated state for the client

### 4. Linking UI to Events

```python
{
    "type": "button",
    "props": {
        "label": "+",
        "action": "increment"  # Links to @app.event("increment")
    }
}
```

The `action` prop connects a button to an event handler.

### 5. Component Type for State Isolation

```python
{
    "type": "div",
    "component_type": "counter",  # Identifies this component
    ...
}
```

The `component_type` helps isolate state updates to specific UI components.

## Variations

### With Reset Button

Add a reset button to set the counter back to zero:

```python
@app.event("reset")
def handle_reset(event_data=None):
    counter.set(0)
    return {"counter": counter.value}
```

```python
{
    "type": "button",
    "props": {
        "label": "Reset",
        "action": "reset"
    }
}
```

### With Step Size

Allow incrementing by different amounts:

```python
@app.event("increment_by")
def handle_increment_by(event_data=None):
    step = event_data.get("step", 1) if event_data else 1
    counter.set(counter.value + step)
    return {"counter": counter.value}
```

```python
{
    "type": "button",
    "props": {
        "label": "+10",
        "action": "increment_by",
        "data": {"step": 10}
    }
}
```

## Next Steps

- [Dashboard Example](dashboard.md) - More complex layout
- [State Management Guide](../guide/state.md) - Deep dive into state
