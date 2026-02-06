# Components

Build reusable UI components in Cacao.

## Overview

Components allow you to create reusable pieces of UI. They can be:

1. **Simple functions** - Return UI dictionaries
2. **Component classes** - Inherit from `Component` base class

## Function Components

The simplest way to create reusable UI:

```python
def card(title: str, content: str) -> dict:
    """A reusable card component."""
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
                {"type": "h3", "props": {"content": title}},
                {"type": "p", "props": {"content": content}}
            ]
        }
    }

# Use it
@app.mix("/")
def home():
    return {
        "type": "div",
        "children": [
            card("Welcome", "This is a card"),
            card("Another", "Another card")
        ]
    }
```

## Class Components

For more complex components, use the `Component` base class:

```python
from cacao import Component
from typing import Dict, Any, Optional

class UserCard(Component):
    def __init__(self, name: str, role: str):
        super().__init__()
        self.name = name
        self.role = role
        self.component_type = "user-card"  # For state isolation

    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "type": "div",
            "component_type": self.component_type,
            "props": {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "16px",
                    "background": "#f5f5f5",
                    "borderRadius": "8px"
                },
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "48px",
                                "height": "48px",
                                "borderRadius": "50%",
                                "background": "#2c1810",
                                "marginRight": "16px"
                            }
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "children": [
                                {"type": "h4", "props": {"content": self.name}},
                                {"type": "p", "props": {"content": self.role, "style": {"color": "#666"}}}
                            ]
                        }
                    }
                ]
            }
        }

# Use it
user = UserCard("Alice", "Developer")
user.render()
```

## Component Base Class

The `Component` class provides:

- `__init__()` - Initialize with `component_type` for identification
- `render(ui_state)` - Return the UI dictionary
- Automatic ID generation

```python
from cacao.ui.components.base import Component

class MyComponent(Component):
    def __init__(self):
        super().__init__()
        self.id = id(self)
        self.component_type = "my-component"

    def render(self, ui_state=None):
        # Return UI dictionary
        return {...}
```

## Stateful Components

Components can manage their own state:

```python
from cacao import Component, State

class Counter(Component):
    def __init__(self):
        super().__init__()
        self.component_type = "counter"
        self.count = State(0)

    def render(self, ui_state=None):
        # Use ui_state if available (for client-side updates)
        value = self.count.value
        if ui_state and "counter" in ui_state:
            value = ui_state["counter"]

        return {
            "type": "div",
            "component_type": self.component_type,
            "props": {
                "children": [
                    {"type": "text", "props": {"content": str(value)}},
                    {
                        "type": "button",
                        "props": {"label": "+", "action": "counter_increment"}
                    }
                ]
            }
        }
```

## Component Directory Structure

For JavaScript-rendered components (advanced):

```
cacao/ui/components/
├── data/
│   └── avatar/
│       ├── avatar.js    # Client-side renderer
│       ├── avatar.css   # Styles
│       └── avatar.py    # Python class
└── forms/
    └── input/
        ├── input.js
        ├── input.css
        └── input.py
```

See the [Component Development Guide](components-advanced.md) for details on JavaScript components.

## Available Components

Cacao includes several built-in components:

### Input Components

- **Slider** - Numeric range input
- **Input** - Text input field
- **Form** - Form container

### Data Components

- **Table** - Display tabular data
- **DataTable** - Advanced data table with features

### Layout Components

- **Grid** - Grid layout
- **SidebarLayout** - Sidebar with content area

## Usage Example

```python
from cacao.ui import Slider, Table

# Create a slider
slider = Slider(min_value=0, max_value=100, step=1)

# Create a table
table = Table(
    headers=["Name", "Value"],
    rows=[["Item 1", 10], ["Item 2", 20]]
)

@app.mix("/")
def home():
    return {
        "type": "div",
        "children": [
            slider.render(),
            table.render()
        ]
    }
```

## Composing Components

Components can contain other components:

```python
def page_layout(title: str, children: list) -> dict:
    return {
        "type": "div",
        "props": {
            "style": {"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"}
        },
        "children": [
            {"type": "h1", "props": {"content": title}},
            {"type": "div", "props": {"children": children}}
        ]
    }

def dashboard_card(title: str, value: str) -> dict:
    return {
        "type": "div",
        "props": {
            "style": {"padding": "20px", "background": "white", "borderRadius": "8px"},
            "children": [
                {"type": "h4", "props": {"content": title}},
                {"type": "p", "props": {"content": value, "style": {"fontSize": "32px"}}}
            ]
        }
    }

@app.mix("/")
def home():
    return page_layout("Dashboard", [
        dashboard_card("Users", "1,234"),
        dashboard_card("Revenue", "$45,678"),
    ])
```

## Best Practices

### 1. Use Type Hints

```python
from typing import Dict, Any, List, Optional

def button(label: str, action: str) -> Dict[str, Any]:
    return {...}
```

### 2. Keep Components Focused

Each component should do one thing well:

```python
# Good - focused components
def avatar(url: str, size: int = 40) -> dict: ...
def user_name(name: str) -> dict: ...
def user_card(user: dict) -> dict:
    return {
        "children": [
            avatar(user["avatar"]),
            user_name(user["name"])
        ]
    }
```

### 3. Use Meaningful Component Types

```python
class Header(Component):
    def __init__(self):
        self.component_type = "app-header"  # Descriptive
```

### 4. Document Props

```python
def alert(message: str, type: str = "info") -> dict:
    """
    Display an alert message.

    Args:
        message: The alert text
        type: Alert type - "info", "warning", "error", "success"
    """
    ...
```

## Next Steps

- [Theming](theming.md) - Style your components
- [Icons](icons.md) - Add icons to your UI
