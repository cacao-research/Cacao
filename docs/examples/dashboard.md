# Dashboard Example

A dashboard layout with sidebar navigation and metric cards.

## Overview

This example demonstrates:

- Creating a sidebar navigation layout
- Building reusable card components
- Organizing a multi-section dashboard

## Running the Example

```bash
cacao dev examples/sidebar_layout_example.py
```

Or use the dashboard template:

```bash
cacao create my-dashboard --template dashboard
cd my-dashboard
cacao dev app.py
```

## Code

```python
import cacao
from typing import Dict, Any

app = cacao.App()


def card(title: str, value: str, description: str) -> Dict[str, Any]:
    """Create a dashboard card component."""
    return {
        "type": "div",
        "props": {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "24px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
            },
            "children": [
                {
                    "type": "text",
                    "props": {
                        "content": title,
                        "style": {
                            "fontSize": "14px",
                            "color": "#666",
                            "marginBottom": "8px"
                        }
                    }
                },
                {
                    "type": "text",
                    "props": {
                        "content": value,
                        "style": {
                            "fontSize": "32px",
                            "fontWeight": "bold",
                            "color": "#2c1810",
                            "marginBottom": "4px"
                        }
                    }
                },
                {
                    "type": "text",
                    "props": {
                        "content": description,
                        "style": {
                            "fontSize": "12px",
                            "color": "#999"
                        }
                    }
                }
            ]
        }
    }


def nav_item(label: str, active: bool = False) -> Dict[str, Any]:
    """Create a navigation item."""
    return {
        "type": "text",
        "props": {
            "content": label,
            "style": {
                "padding": "12px",
                "borderRadius": "8px",
                "cursor": "pointer",
                "background": "rgba(255,255,255,0.1)" if active else "transparent"
            }
        }
    }


@app.mix("/")
def home() -> Dict[str, Any]:
    """Dashboard home page."""
    return {
        "type": "div",
        "props": {
            "style": {
                "display": "flex",
                "minHeight": "100vh",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            # Sidebar
            {
                "type": "div",
                "props": {
                    "style": {
                        "width": "250px",
                        "background": "#2c1810",
                        "padding": "24px",
                        "color": "white"
                    },
                    "children": [
                        {
                            "type": "h2",
                            "props": {
                                "content": "Dashboard",
                                "style": {
                                    "fontSize": "24px",
                                    "marginBottom": "32px",
                                    "color": "#f0be9b"
                                }
                            }
                        },
                        {
                            "type": "div",
                            "props": {
                                "style": {
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "gap": "8px"
                                },
                                "children": [
                                    nav_item("Overview", active=True),
                                    nav_item("Analytics"),
                                    nav_item("Reports"),
                                    nav_item("Settings")
                                ]
                            }
                        }
                    ]
                }
            },
            # Main content
            {
                "type": "div",
                "props": {
                    "style": {
                        "flex": "1",
                        "background": "#f5f5f5",
                        "padding": "32px"
                    },
                    "children": [
                        {
                            "type": "h1",
                            "props": {
                                "content": "Overview",
                                "style": {
                                    "fontSize": "28px",
                                    "color": "#2c1810",
                                    "marginBottom": "24px"
                                }
                            }
                        },
                        {
                            "type": "div",
                            "props": {
                                "style": {
                                    "display": "grid",
                                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                                    "gap": "24px"
                                },
                                "children": [
                                    card("Total Users", "1,234", "+12% from last month"),
                                    card("Revenue", "$45,678", "+8% from last month"),
                                    card("Active Sessions", "342", "Currently online"),
                                    card("Conversion Rate", "3.2%", "+0.4% from last week")
                                ]
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

### 1. Component Functions

Create reusable UI pieces as functions:

```python
def card(title: str, value: str, description: str) -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {...}
    }
```

### 2. Flexbox Layout

Use CSS Flexbox for the sidebar layout:

```python
{
    "style": {
        "display": "flex",
        "minHeight": "100vh"
    }
}
```

### 3. CSS Grid for Cards

Use CSS Grid for responsive card layouts:

```python
{
    "style": {
        "display": "grid",
        "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
        "gap": "24px"
    }
}
```

### 4. Composing Components

Build complex UIs by combining components:

```python
"children": [
    card("Users", "1,234", "..."),
    card("Revenue", "$45,678", "..."),
]
```

## Extending the Dashboard

### Add Navigation Events

```python
from cacao import State

current_page = State("overview")

@app.event("navigate")
def handle_navigate(event_data=None):
    if event_data and "page" in event_data:
        current_page.set(event_data["page"])
    return {"page": current_page.value}
```

```python
def nav_item(label: str, page: str, active: bool = False) -> Dict[str, Any]:
    return {
        "type": "text",
        "props": {
            "content": label,
            "action": "navigate",
            "data": {"page": page},
            "style": {...}
        }
    }
```

### Add Data Charts

```python
def chart_card(title: str, data: list) -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "24px",
                "gridColumn": "span 2"  # Double width
            },
            "children": [
                {"type": "h3", "props": {"content": title}},
                # Chart rendering would go here
            ]
        }
    }
```

### Use the SidebarLayout Component

Cacao includes a built-in sidebar layout:

```python
from cacao.ui.components.sidebar_layout import SidebarLayout

nav_items = [
    {"label": "Overview", "route": "/"},
    {"label": "Analytics", "route": "/analytics"},
]

content = [card("Users", "1,234", "...")]

layout = SidebarLayout(
    nav_items=nav_items,
    content_components=content,
    app_title="My Dashboard"
)

@app.mix("/")
def home():
    return layout.render()
```

## Next Steps

- [Data Tables Example](tables.md) - Display and filter data
- [Theming Guide](../guide/theming.md) - Customize dashboard appearance
