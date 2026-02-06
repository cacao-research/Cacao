# React Integration

Use React components from npm packages in your Cacao applications.

## Overview

The React integration allows you to:

- Use React components from npm packages
- Load CSS files associated with React components
- Pass props to React components
- Handle events from React components

## Setup

Import the ReactComponent class and ReactExtension, then add the extension to your app:

```python
import cacao
from cacao.ui import ReactComponent
from cacao.extensions.react_extension import ReactExtension

# Create the app with React extension
app = cacao.App(extensions=[ReactExtension()])
```

## Basic Usage

Here's a simple example using a CodeMirror editor:

```python
# Create a CodeMirror editor
editor = ReactComponent(
    package="codemirror",
    component="CodeMirror",
    props={
        "value": "const hello = 'world';",
        "options": {
            "mode": "javascript",
            "theme": "material",
            "lineNumbers": True
        }
    },
    css=["lib/codemirror.css", "theme/material.css"]
)

# Use the component in your UI
@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "children": [
                {
                    "type": "h1",
                    "props": {"content": "CodeMirror Example"}
                },
                editor.render()
            ]
        }
    }
```

## ReactComponent Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `package` | Yes | The npm package name (e.g., "codemirror") |
| `component` | Yes | The React component name from the package |
| `props` | No | Props to pass to the React component |
| `version` | No | Package version (default: "latest") |
| `css` | No | List of CSS files to load from the package |
| `cdn` | No | CDN to use (default: jsdelivr) |
| `id` | No | Container element ID (auto-generated if not provided) |

## Handling Events

Handle events from React components with Cacao event handlers:

```python
# Define an event handler
@app.event("update_code")
def update_code(data):
    if "code" in data:
        app.state.code = data["code"]
        return {"code": app.state.code}
    return {}

# Use the event handler in a React component
editor = ReactComponent(
    package="codemirror",
    component="CodeMirror",
    props={
        "value": app.state.code,
        "options": {
            "mode": "javascript",
            "lineNumbers": True
        },
        "onBeforeChange": {
            "type": "event",
            "name": "update_code",
            "data": {"code": "$value"}
        }
    }
)
```

## Supported Components

The React integration works with most React components that:

1. Are available as UMD builds on a CDN (like jsdelivr)
2. Export the component as a named or default export
3. Are compatible with React 18

### Popular Compatible Components

- CodeMirror
- React JSON View
- Material-UI components
- React Charts
- React Table

## Examples

See the examples directory:

- `examples/react_component_example.py` - Basic CodeMirror example
- `examples/advanced_react_example.py` - Multiple components with state

## How It Works

The React integration:

1. Loads React and ReactDOM from a CDN
2. Loads the specified npm package from a CDN
3. Creates a container element for the React component
4. Renders the React component into the container
5. Handles events between React and Cacao

Implementation files:

- `cacao/ui/components/react.py` - ReactComponent class
- `cacao/extensions/react_extension.py` - React bridge extension
- `cacao/core/static/js/react-bridge.js` - Client-side rendering

## Troubleshooting

If a React component doesn't load:

1. Check the browser console for errors
2. Verify package and component names are correct
3. Try specifying a specific package version
4. Check if the package has a UMD build on the CDN
5. Try a different CDN (e.g., unpkg instead of jsdelivr)
