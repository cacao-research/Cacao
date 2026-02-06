# Quickstart

Get up and running with Cacao in under 5 minutes.

## Create a Project

The easiest way to start is with the CLI:

```bash
cacao create
```

Follow the interactive prompts to select a template:

1. **Minimal** - A bare-bones hello world app
2. **Counter** - Interactive counter demonstrating state management
3. **Dashboard** - Full dashboard layout with sidebar navigation

Or create directly with options:

```bash
cacao create my-app --template counter
```

## Project Structure

After creation, your project looks like:

```
my-app/
├── app.py           # Your main application
├── requirements.txt # Dependencies (just cacao)
└── static/
    └── css/
        └── custom.css  # Custom styles
```

## Run the App

```bash
cd my-app
pip install -r requirements.txt
cacao dev app.py
```

Open `http://localhost:1634` in your browser.

## Understanding the Code

Here's what a minimal Cacao app looks like:

```python
import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "style": {"padding": "20px"}
        },
        "children": [
            {
                "type": "h1",
                "props": {"content": "Hello, Cacao!"}
            }
        ]
    }

if __name__ == "__main__":
    app.brew()
```

Key concepts:

- **`cacao.App()`** - Creates your application instance
- **`@app.mix("/")`** - Defines a route (similar to Flask/FastAPI)
- **Return dict** - UI is defined as JSON-like Python dictionaries
- **`app.brew()`** - Starts the development server

## Adding Interactivity

Add state and event handlers:

```python
from cacao import State

counter = State(0)

@app.event("increment")
def handle_increment(event_data=None):
    counter.set(counter.value + 1)
    return {"counter": counter.value}
```

Then reference in your UI:

```python
{
    "type": "button",
    "props": {
        "label": "Click me",
        "action": "increment"  # Links to the event handler
    }
}
```

## Next Steps

- [Your First App](first-app.md) - Build a complete app step by step
- [Core Concepts](../guide/concepts.md) - Understand how Cacao works
- [Examples](../examples/index.md) - Browse example applications
