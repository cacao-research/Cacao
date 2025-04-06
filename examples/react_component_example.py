"""
React Component Example for Cacao.
Demonstrates how to use React components from npm packages in Cacao applications.
This example shows how to integrate CodeMirror, a popular code editor.
"""

import cacao
from cacao.ui import ReactComponent
from cacao.extensions.react_extension import ReactExtension

# Create the app with React extension
app = cacao.App(extensions=[ReactExtension()])

@app.mix("/")
def home():
    """Render the home page with a CodeMirror editor."""
    return {
        "type": "div",
        "props": {
            "style": {
                "padding": "20px",
                "fontFamily": "Arial, sans-serif",
                "maxWidth": "800px",
                "margin": "0 auto"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "React Component Integration Example",
                    "style": {
                        "color": "#6B4226",
                        "marginBottom": "20px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "This example demonstrates how to use React components from npm packages in Cacao applications.",
                    "style": {
                        "marginBottom": "20px"
                    }
                }
            },
            # CodeMirror React component
            # Reverting to original CodeMirror v5
            ReactComponent(
                package="codemirror",
                component="CodeMirror", # The component name is the global object itself for v5
                props={
                    "value": """// CodeMirror Example
function helloWorld() {
    console.log("Hello from CodeMirror in Cacao!");
    return "Hello, world!";
}

// Try editing this code!
const result = helloWorld();
""",
                    "options": {
                        "mode": "javascript",
                        "theme": "material",
                        "lineNumbers": True,
                        "lineWrapping": True
                    }
                },
                css=["lib/codemirror.css", "theme/material.css", "mode/javascript/javascript.css"],
                id="code-editor",
                version="5.65.15",  # Using stable v5
                cdn="https://cdn.jsdelivr.net/npm"  # Use default jsdelivr CDN
            ).render(),
            {
                "type": "div",
                "props": {
                    "style": {
                        "marginTop": "20px",
                        "padding": "15px",
                        "backgroundColor": "#f5f5f5",
                        "borderRadius": "4px"
                    }
                },
                "children": [
                    {
                        "type": "h3",
                        "props": {
                            "content": "How It Works"
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "content": "The ReactComponent class creates a bridge between Cacao and React, allowing you to use React components from npm packages."
                        }
                    },
                    {
                        "type": "pre",
                        "props": {
                            "content": """# Example usage
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
)""",
                            "style": {
                                "backgroundColor": "#f0f0f0",
                                "padding": "10px",
                                "borderRadius": "4px",
                                "overflow": "auto"
                            }
                        }
                    }
                ]
            }
        ]
    }

if __name__ == "__main__":
    app.brew()