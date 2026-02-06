# Routing

Cacao uses a simple routing system for defining pages and handling events.

## Page Routes

Define pages with the `@app.mix()` decorator:

```python
import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {"type": "h1", "props": {"content": "Home"}}

@app.mix("/about")
def about():
    return {"type": "h1", "props": {"content": "About"}}

@app.mix("/users")
def users():
    return {"type": "h1", "props": {"content": "Users"}}
```

## Route Parameters

Routes can include dynamic parameters:

```python
@app.mix("/user/<user_id>")
def user_profile(user_id: str):
    return {
        "type": "h1",
        "props": {"content": f"User Profile: {user_id}"}
    }
```

## Event Handlers

Handle user interactions with `@app.event()`:

```python
@app.event("button_clicked")
def handle_click(event_data=None):
    print("Button was clicked!")
    return {"status": "success"}

@app.event("form_submitted")
def handle_form(event_data=None):
    if event_data:
        name = event_data.get("name", "")
        email = event_data.get("email", "")
        # Process form data
    return {"message": "Form received"}
```

### Event Data

Event handlers receive data from the client:

```python
@app.event("update_settings")
def handle_settings(event_data=None):
    if event_data:
        # event_data contains client-sent data
        theme = event_data.get("theme")
        font_size = event_data.get("fontSize")
    return {"updated": True}
```

### Returning State

Event handlers should return state updates for the client:

```python
from cacao import State

counter = State(0)

@app.event("increment")
def handle_increment(event_data=None):
    counter.set(counter.value + 1)
    # Return updated state so UI can update
    return {"counter": counter.value}
```

## Linking Events to UI

Connect UI elements to event handlers using the `action` prop:

```python
{
    "type": "button",
    "props": {
        "label": "Click Me",
        "action": "button_clicked"  # Matches @app.event name
    }
}
```

### Passing Data with Actions

Include additional data with the action:

```python
{
    "type": "button",
    "props": {
        "label": "Delete",
        "action": "delete_item",
        "data": {
            "item_id": 123,
            "confirm": True
        }
    }
}
```

The `data` object is included in `event_data`:

```python
@app.event("delete_item")
def handle_delete(event_data=None):
    if event_data:
        item_id = event_data.get("item_id")
        # Delete the item
    return {"deleted": item_id}
```

## Input Events

Form inputs automatically send their values:

```python
{
    "type": "input",
    "props": {
        "id": "username",
        "placeholder": "Enter name",
        "onChange": "username_changed"
    }
}
```

```python
@app.event("username_changed")
def handle_username(event_data=None):
    if event_data:
        value = event_data.get("value", "")
        # Process the input value
    return {"username": value}
```

## Navigation

### Client-Side Links

Use anchor elements for navigation:

```python
{
    "type": "a",
    "props": {
        "href": "/about",
        "content": "Go to About"
    }
}
```

### Programmatic Navigation

Return a navigation instruction from an event handler:

```python
@app.event("go_to_dashboard")
def handle_nav(event_data=None):
    return {"navigate": "/dashboard"}
```

## Route Registry

Routes are stored in a global registry:

```python
from cacao.core.decorators import ROUTES

# List all registered routes
for route, handler in ROUTES.items():
    print(f"{route}: {handler.__name__}")
```

## Event Handler Registry

Similarly for events:

```python
from cacao.core.decorators import EVENT_HANDLERS

# List all event handlers
for event, handler in EVENT_HANDLERS.items():
    print(f"{event}: {handler.__name__}")
```

## Best Practices

### 1. Name Events Clearly

```python
# Good - descriptive action names
@app.event("submit_contact_form")
@app.event("toggle_dark_mode")
@app.event("delete_user_account")

# Avoid - vague names
@app.event("click")
@app.event("submit")
```

### 2. Validate Event Data

```python
@app.event("create_user")
def handle_create(event_data=None):
    if not event_data:
        return {"error": "No data provided"}

    name = event_data.get("name", "").strip()
    if not name:
        return {"error": "Name is required"}

    # Process valid data
    return {"success": True, "name": name}
```

### 3. Return Consistent Response Shapes

```python
# Good - consistent structure
@app.event("action")
def handle_action(event_data=None):
    try:
        # Do something
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Next Steps

- [State Management](state.md) - Managing application state
- [Components](components.md) - Building reusable UI
