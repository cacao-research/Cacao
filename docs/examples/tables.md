# Data Tables Example

Display and filter tabular data with Cacao.

## Overview

This example demonstrates:

- Displaying data in tables
- Filtering and searching data
- Integrating with Pandas DataFrames

## Running the Example

```bash
cacao dev examples/pandas_table_desktop_app.py
```

For filtering:

```bash
cacao dev examples/pandas_table_with_filters_desktop_app.py
```

## Basic Table

```python
import cacao
from typing import Dict, Any, List

app = cacao.App()

# Sample data
data = [
    {"name": "Alice", "role": "Developer", "status": "Active"},
    {"name": "Bob", "role": "Designer", "status": "Active"},
    {"name": "Carol", "role": "Manager", "status": "Away"},
]


def table_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Render a table row."""
    return {
        "type": "tr",
        "props": {
            "children": [
                {"type": "td", "props": {"content": row["name"], "style": {"padding": "12px"}}},
                {"type": "td", "props": {"content": row["role"], "style": {"padding": "12px"}}},
                {"type": "td", "props": {"content": row["status"], "style": {"padding": "12px"}}}
            ]
        }
    }


@app.mix("/")
def home() -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {"padding": "40px", "fontFamily": "sans-serif"}
        },
        "children": [
            {"type": "h1", "props": {"content": "Team Members"}},
            {
                "type": "table",
                "props": {
                    "style": {
                        "width": "100%",
                        "borderCollapse": "collapse",
                        "marginTop": "20px"
                    },
                    "children": [
                        # Header
                        {
                            "type": "thead",
                            "props": {
                                "children": [{
                                    "type": "tr",
                                    "props": {
                                        "children": [
                                            {"type": "th", "props": {"content": "Name", "style": {"textAlign": "left", "padding": "12px", "borderBottom": "2px solid #ddd"}}},
                                            {"type": "th", "props": {"content": "Role", "style": {"textAlign": "left", "padding": "12px", "borderBottom": "2px solid #ddd"}}},
                                            {"type": "th", "props": {"content": "Status", "style": {"textAlign": "left", "padding": "12px", "borderBottom": "2px solid #ddd"}}}
                                        ]
                                    }
                                }]
                            }
                        },
                        # Body
                        {
                            "type": "tbody",
                            "props": {
                                "children": [table_row(row) for row in data]
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

## Table with Filtering

```python
import cacao
from cacao import State
from typing import Dict, Any, List, Optional

app = cacao.App()

# Sample data
all_data = [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 95000},
    {"id": 2, "name": "Bob", "department": "Design", "salary": 85000},
    {"id": 3, "name": "Carol", "department": "Engineering", "salary": 105000},
    {"id": 4, "name": "David", "department": "Marketing", "salary": 75000},
    {"id": 5, "name": "Eve", "department": "Engineering", "salary": 90000},
]

# Filter state
search_term = State("")
department_filter = State("all")


def get_filtered_data() -> List[Dict]:
    """Filter data based on current state."""
    filtered = all_data

    # Apply search
    if search_term.value:
        term = search_term.value.lower()
        filtered = [r for r in filtered if term in r["name"].lower()]

    # Apply department filter
    if department_filter.value != "all":
        filtered = [r for r in filtered if r["department"] == department_filter.value]

    return filtered


@app.event("search")
def handle_search(event_data: Optional[Dict] = None) -> Dict[str, Any]:
    if event_data and "value" in event_data:
        search_term.set(event_data["value"])
    return {"data": get_filtered_data()}


@app.event("filter_department")
def handle_filter(event_data: Optional[Dict] = None) -> Dict[str, Any]:
    if event_data and "value" in event_data:
        department_filter.set(event_data["value"])
    return {"data": get_filtered_data()}


@app.mix("/")
def home() -> Dict[str, Any]:
    filtered_data = get_filtered_data()
    departments = list(set(r["department"] for r in all_data))

    return {
        "type": "div",
        "props": {
            "style": {"padding": "40px", "fontFamily": "sans-serif", "maxWidth": "900px", "margin": "0 auto"}
        },
        "children": [
            {"type": "h1", "props": {"content": "Employee Directory"}},

            # Filters
            {
                "type": "div",
                "props": {
                    "style": {"display": "flex", "gap": "16px", "margin": "24px 0"},
                    "children": [
                        {
                            "type": "input",
                            "props": {
                                "placeholder": "Search by name...",
                                "onChange": "search",
                                "style": {"padding": "10px", "borderRadius": "8px", "border": "1px solid #ddd", "flex": "1"}
                            }
                        },
                        {
                            "type": "select",
                            "props": {
                                "onChange": "filter_department",
                                "style": {"padding": "10px", "borderRadius": "8px", "border": "1px solid #ddd"},
                                "children": [
                                    {"type": "option", "props": {"value": "all", "content": "All Departments"}}
                                ] + [
                                    {"type": "option", "props": {"value": dept, "content": dept}}
                                    for dept in departments
                                ]
                            }
                        }
                    ]
                }
            },

            # Results count
            {
                "type": "p",
                "props": {
                    "content": f"Showing {len(filtered_data)} of {len(all_data)} employees",
                    "style": {"color": "#666", "marginBottom": "16px"}
                }
            },

            # Table
            {
                "type": "table",
                "props": {
                    "style": {"width": "100%", "borderCollapse": "collapse"},
                    "children": [
                        {
                            "type": "thead",
                            "props": {
                                "children": [{
                                    "type": "tr",
                                    "props": {
                                        "style": {"background": "#f5f5f5"},
                                        "children": [
                                            {"type": "th", "props": {"content": col, "style": {"padding": "12px", "textAlign": "left"}}}
                                            for col in ["Name", "Department", "Salary"]
                                        ]
                                    }
                                }]
                            }
                        },
                        {
                            "type": "tbody",
                            "props": {
                                "children": [
                                    {
                                        "type": "tr",
                                        "props": {
                                            "style": {"borderBottom": "1px solid #eee"},
                                            "children": [
                                                {"type": "td", "props": {"content": row["name"], "style": {"padding": "12px"}}},
                                                {"type": "td", "props": {"content": row["department"], "style": {"padding": "12px"}}},
                                                {"type": "td", "props": {"content": f"${row['salary']:,}", "style": {"padding": "12px"}}}
                                            ]
                                        }
                                    }
                                    for row in filtered_data
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

## Using Pandas

```python
import cacao
import pandas as pd
from typing import Dict, Any

app = cacao.App()

# Create DataFrame
df = pd.DataFrame({
    "Product": ["Widget A", "Widget B", "Gadget X", "Gadget Y"],
    "Category": ["Widgets", "Widgets", "Gadgets", "Gadgets"],
    "Price": [29.99, 39.99, 49.99, 59.99],
    "Stock": [150, 75, 200, 50]
})


def dataframe_to_table(df: pd.DataFrame) -> Dict[str, Any]:
    """Convert a Pandas DataFrame to a Cacao table."""
    headers = df.columns.tolist()
    rows = df.values.tolist()

    return {
        "type": "table",
        "props": {
            "style": {"width": "100%", "borderCollapse": "collapse"},
            "children": [
                # Header
                {
                    "type": "thead",
                    "props": {
                        "children": [{
                            "type": "tr",
                            "props": {
                                "children": [
                                    {"type": "th", "props": {"content": col, "style": {"padding": "12px", "textAlign": "left", "borderBottom": "2px solid #ddd"}}}
                                    for col in headers
                                ]
                            }
                        }]
                    }
                },
                # Body
                {
                    "type": "tbody",
                    "props": {
                        "children": [
                            {
                                "type": "tr",
                                "props": {
                                    "children": [
                                        {"type": "td", "props": {"content": str(cell), "style": {"padding": "12px", "borderBottom": "1px solid #eee"}}}
                                        for cell in row
                                    ]
                                }
                            }
                            for row in rows
                        ]
                    }
                }
            ]
        }
    }


@app.mix("/")
def home() -> Dict[str, Any]:
    return {
        "type": "div",
        "props": {
            "style": {"padding": "40px", "fontFamily": "sans-serif"}
        },
        "children": [
            {"type": "h1", "props": {"content": "Product Inventory"}},
            dataframe_to_table(df)
        ]
    }


if __name__ == "__main__":
    app.brew()
```

## Built-in Table Component

Cacao includes a `Table` component:

```python
from cacao.ui import Table

table = Table(
    headers=["Name", "Role", "Status"],
    rows=[
        ["Alice", "Developer", "Active"],
        ["Bob", "Designer", "Active"],
    ]
)

@app.mix("/")
def home():
    return {
        "type": "div",
        "children": [table.render()]
    }
```

## Key Concepts

### 1. Dynamic Rendering

Generate table rows from data:

```python
"children": [table_row(row) for row in data]
```

### 2. Filter State

Use `State` to track filter values:

```python
search_term = State("")

@app.event("search")
def handle_search(event_data=None):
    search_term.set(event_data.get("value", ""))
    return {"data": get_filtered_data()}
```

### 3. Input Binding

Connect inputs to event handlers:

```python
{
    "type": "input",
    "props": {
        "onChange": "search"
    }
}
```

## Next Steps

- [Dashboard Example](dashboard.md) - Combine tables with dashboards
- [Components Guide](../guide/components.md) - Build reusable table components
