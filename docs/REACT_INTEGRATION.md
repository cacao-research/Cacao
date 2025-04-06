# React Integration for Cacao

This document explains how to use React components from npm packages in your Cacao applications.

## Overview

The React integration for Cacao allows you to:

1. Use React components from npm packages directly in your Cacao applications
2. Load CSS files associated with React components
3. Pass props to React components
4. Handle events from React components

## Setup

To use React components in your Cacao application, you need to:

1. Import the ReactComponent class and ReactExtension
2. Add the ReactExtension to your app
3. Use the ReactComponent class to render React components

```python
import cacao
from cacao.ui import ReactComponent
from cacao.extensions.react_extension import ReactExtension

# Create the app with React extension
app = cacao.App(extensions=[ReactExtension()])
```

## Basic Usage

Here's a simple example of using a React component:

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
                    "props": {
                        "content": "CodeMirror Example"
                    }
                },
                # Render the React component
                editor.render()
            ]
        }
    }
```

## ReactComponent Parameters

The `ReactComponent` class accepts the following parameters:

- `package` (required): The npm package name (e.g., "codemirror")
- `component` (required): The React component name to use from the package
- `props` (optional): Props to pass to the React component
- `version` (optional): The package version to use (default: "latest")
- `css` (optional): List of CSS files to load from the package
- `cdn` (optional): The CDN to use for loading the package (default: jsdelivr)
- `id` (optional): ID for the component container (auto-generated if not provided)

## Handling Events

You can handle events from React components by defining event handlers in your Cacao app:

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

## Supported React Components

The React integration should work with most React components that:

1. Are available as UMD builds on a CDN (like jsdelivr)
2. Export the component as a named export or as the default export
3. Are compatible with React 18

Some popular React components that work well with this integration:

- CodeMirror
- React JSON View
- Material-UI components
- React Charts
- React Table

## Advanced Usage

For more advanced usage, see the examples:

- `examples/react_component_example.py`: Basic example with CodeMirror
- `examples/advanced_react_example.py`: Advanced example with multiple React components and state management

## Troubleshooting

If a React component doesn't load properly:

1. Check the browser console for errors
2. Verify that the package and component names are correct
3. Try specifying a specific version of the package
4. Check if the package has a UMD build available on the CDN
5. Try using a different CDN (e.g., unpkg instead of jsdelivr)

## How It Works

The React integration works by:

1. Loading React and ReactDOM from a CDN
2. Loading the specified npm package from a CDN
3. Creating a container element for the React component
4. Rendering the React component into the container
5. Handling events between the React component and Cacao

The integration is implemented using:

- `cacao/ui/components/react.py`: Defines the ReactComponent class
- `cacao/extensions/react_extension.py`: Adds the React bridge script to the HTML template
- `cacao/core/static/js/react-bridge.js`: Client-side code for loading and rendering React components