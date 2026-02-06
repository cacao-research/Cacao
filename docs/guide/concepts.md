# Core Concepts

Understanding the fundamental architecture of Cacao.

## Overview

Cacao is built around a few key concepts:

1. **Routes** - Define pages using `@app.mix()` decorators
2. **JSON UI** - Build interfaces with Python dictionaries
3. **State** - Manage reactive data with the `State` class
4. **Events** - Handle user interactions with event handlers
5. **Components** - Create reusable UI building blocks

## Architecture

```
Python @app.mix route → JSON UI definition → WebSocket → Client renders
         ↑                                              ↓
    State.update() ←── Event handler ←── Client action
```

### Data Flow

1. **Route Definition**: Your Python function returns a dictionary describing the UI
2. **Server Processing**: The server serializes this to JSON
3. **Client Rendering**: The browser receives and renders the UI
4. **User Interaction**: Clicks, inputs, etc. trigger events
5. **Event Handling**: Your Python event handlers process the action
6. **State Update**: State changes trigger UI updates via WebSocket

## Routes

Routes are defined with the `@app.mix()` decorator:

```python
import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {
        "type": "div",
        "children": [
            {"type": "h1", "props": {"content": "Home Page"}}
        ]
    }

@app.mix("/about")
def about():
    return {
        "type": "div",
        "children": [
            {"type": "h1", "props": {"content": "About Page"}}
        ]
    }
```

## JSON UI Definition

UI elements are Python dictionaries with a specific structure:

```python
{
    "type": "element_type",      # Required: div, h1, button, etc.
    "component_type": "unique",  # Optional: for state isolation
    "props": {
        "content": "text",       # Text content
        "style": {...},          # CSS styles
        "children": [...],       # Child elements
        # ... other properties
    },
    "children": [...]            # Alternative to props.children
}
```

### Common Element Types

| Type | Description |
|------|-------------|
| `div` | Generic container |
| `h1` - `h6` | Headings |
| `p`, `text` | Paragraph, text content |
| `button` | Clickable button |
| `input` | Text input field |
| `img` | Image |
| `section` | Section container |

### Styling

Styles use camelCase CSS properties:

```python
{
    "type": "div",
    "props": {
        "style": {
            "backgroundColor": "#f0f0f0",
            "padding": "20px",
            "borderRadius": "8px",
            "display": "flex",
            "flexDirection": "column"
        }
    }
}
```

## State Management

See [State Management](state.md) for details.

```python
from cacao import State

counter = State(0)  # Initial value

# Update state
counter.set(counter.value + 1)

# Subscribe to changes
@counter.subscribe
def on_change(new_value):
    print(f"Counter is now: {new_value}")
```

## Event Handling

See [Routing](routing.md) for details on events.

```python
@app.event("button_clicked")
def handle_click(event_data=None):
    # Process the event
    return {"status": "success"}
```

UI elements trigger events:

```python
{
    "type": "button",
    "props": {
        "label": "Click Me",
        "action": "button_clicked"  # Matches event handler name
    }
}
```

## Components

For reusable UI, create component classes:

```python
from cacao import Component

class Card(Component):
    def __init__(self, title: str, content: str):
        super().__init__()
        self.title = title
        self.content = content

    def render(self, ui_state=None):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px",
                    "background": "white",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                },
                "children": [
                    {"type": "h3", "props": {"content": self.title}},
                    {"type": "p", "props": {"content": self.content}}
                ]
            }
        }

# Use it
card = Card("Title", "Some content")
card.render()  # Returns the JSON UI dict
```

See [Components](components.md) for more.

## Running Your App

### Web Mode (Default)

```python
app.brew()
# or
app.brew(type="web", host="localhost", port=1634)
```

### Desktop Mode

```python
app.brew(type="desktop", title="My App", width=1024, height=768)
```

## Next Steps

- [State Management](state.md) - Deep dive into reactive state
- [Routing](routing.md) - Routes and event handling
- [Components](components.md) - Building reusable components
- [Theming](theming.md) - Customizing appearance
