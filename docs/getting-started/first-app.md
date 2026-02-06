# Your First App

Let's build a todo list app to learn Cacao's core features.

## Setup

Create a new project:

```bash
cacao create todo-app --template minimal
cd todo-app
```

## Step 1: Basic Structure

Replace `app.py` with:

```python
import cacao
from cacao import State
from typing import Dict, Any, Optional, List

app = cacao.App()

# State for our todos
todos: List[str] = []

@app.mix("/")
def home() -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {
                "maxWidth": "500px",
                "margin": "0 auto",
                "padding": "40px 20px",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Todo List",
                    "style": {"color": "#2c1810", "marginBottom": "24px"}
                }
            }
        ]
    }

if __name__ == "__main__":
    app.brew()
```

Run it:

```bash
cacao dev app.py
```

## Step 2: Add Input Form

Add an input field and button:

```python
@app.mix("/")
def home() -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {
                "maxWidth": "500px",
                "margin": "0 auto",
                "padding": "40px 20px",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Todo List",
                    "style": {"color": "#2c1810", "marginBottom": "24px"}
                }
            },
            # Input row
            {
                "type": "div",
                "props": {
                    "style": {"display": "flex", "gap": "8px", "marginBottom": "24px"},
                    "children": [
                        {
                            "type": "input",
                            "props": {
                                "id": "todo-input",
                                "placeholder": "Add a todo...",
                                "style": {
                                    "flex": "1",
                                    "padding": "12px",
                                    "border": "1px solid #ddd",
                                    "borderRadius": "8px",
                                    "fontSize": "16px"
                                }
                            }
                        },
                        {
                            "type": "button",
                            "props": {
                                "label": "Add",
                                "action": "add_todo",
                                "style": {
                                    "padding": "12px 24px",
                                    "background": "#2c1810",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "cursor": "pointer"
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }
```

## Step 3: Add Event Handler

Handle the add button click:

```python
@app.event("add_todo")
def handle_add_todo(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if event_data and "value" in event_data:
        todo_text = event_data["value"].strip()
        if todo_text:
            todos.append(todo_text)
    return {"todos": todos}
```

## Step 4: Display Todos

Create a function to render the todo list:

```python
def render_todo_item(index: int, text: str) -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {
                "display": "flex",
                "alignItems": "center",
                "padding": "12px",
                "background": "#f5f5f5",
                "borderRadius": "8px",
                "marginBottom": "8px"
            },
            "children": [
                {
                    "type": "text",
                    "props": {
                        "content": text,
                        "style": {"flex": "1"}
                    }
                },
                {
                    "type": "button",
                    "props": {
                        "label": "Delete",
                        "action": "delete_todo",
                        "data": {"index": index},
                        "style": {
                            "padding": "6px 12px",
                            "background": "#dc3545",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "4px",
                            "cursor": "pointer"
                        }
                    }
                }
            ]
        }
    }
```

Add the list to your home route:

```python
# Todo list
{
    "type": "div",
    "props": {
        "children": [render_todo_item(i, t) for i, t in enumerate(todos)]
    }
}
```

## Step 5: Delete Handler

Add the delete event handler:

```python
@app.event("delete_todo")
def handle_delete_todo(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if event_data and "index" in event_data:
        index = event_data["index"]
        if 0 <= index < len(todos):
            todos.pop(index)
    return {"todos": todos}
```

## Complete Code

```python
import cacao
from cacao import State
from typing import Dict, Any, Optional, List

app = cacao.App()

todos: List[str] = []


def render_todo_item(index: int, text: str) -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {
                "display": "flex",
                "alignItems": "center",
                "padding": "12px",
                "background": "#f5f5f5",
                "borderRadius": "8px",
                "marginBottom": "8px"
            },
            "children": [
                {"type": "text", "props": {"content": text, "style": {"flex": "1"}}},
                {
                    "type": "button",
                    "props": {
                        "label": "Delete",
                        "action": "delete_todo",
                        "data": {"index": index},
                        "style": {
                            "padding": "6px 12px",
                            "background": "#dc3545",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "4px",
                            "cursor": "pointer"
                        }
                    }
                }
            ]
        }
    }


@app.event("add_todo")
def handle_add_todo(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if event_data and "value" in event_data:
        todo_text = event_data["value"].strip()
        if todo_text:
            todos.append(todo_text)
    return {"todos": todos}


@app.event("delete_todo")
def handle_delete_todo(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if event_data and "index" in event_data:
        index = event_data["index"]
        if 0 <= index < len(todos):
            todos.pop(index)
    return {"todos": todos}


@app.mix("/")
def home() -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {
                "maxWidth": "500px",
                "margin": "0 auto",
                "padding": "40px 20px",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            {"type": "h1", "props": {"content": "Todo List", "style": {"color": "#2c1810", "marginBottom": "24px"}}},
            {
                "type": "div",
                "props": {
                    "style": {"display": "flex", "gap": "8px", "marginBottom": "24px"},
                    "children": [
                        {
                            "type": "input",
                            "props": {
                                "id": "todo-input",
                                "placeholder": "Add a todo...",
                                "style": {"flex": "1", "padding": "12px", "border": "1px solid #ddd", "borderRadius": "8px", "fontSize": "16px"}
                            }
                        },
                        {
                            "type": "button",
                            "props": {
                                "label": "Add",
                                "action": "add_todo",
                                "style": {"padding": "12px 24px", "background": "#2c1810", "color": "white", "border": "none", "borderRadius": "8px", "cursor": "pointer"}
                            }
                        }
                    ]
                }
            },
            {"type": "div", "props": {"children": [render_todo_item(i, t) for i, t in enumerate(todos)]}}
        ]
    }


if __name__ == "__main__":
    app.brew()
```

## What You Learned

- Creating routes with `@app.mix()`
- Handling events with `@app.event()`
- Building UI with nested dictionaries
- Passing data between UI and event handlers

## Next Steps

- [State Management](../guide/state.md) - Learn about the `State` class
- [Components](../guide/components.md) - Create reusable components
- [Theming](../guide/theming.md) - Customize your app's appearance
