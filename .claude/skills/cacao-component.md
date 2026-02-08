---
name: cacao-component
description: Create new UI components for the Cacao framework. Use when adding form elements, display components, layout containers, or any new Python-to-React component. Handles all layers - Python API, React component, LESS styles, handlers, and exports.
---

# Cacao Component Development

This skill guides you through creating new components for the Cacao framework. Components span multiple layers that must stay in sync.

## Architecture Overview

```
Python API (ui.py)     →  JSON definition  →  React Component (JS)
     ↓                                              ↓
simple.py wrapper                              LESS styles
     ↓                                              ↓
__all__ exports                              handlers (if needed)
```

## Component Categories

Components live in organized folders:

| Category | Python | JavaScript | Use Case |
|----------|--------|------------|----------|
| `layout` | containers | Row, Col, Grid, AppShell | Structure |
| `form` | inputs | Button, Input, Select, Slider | User input |
| `display` | data | Card, Metric, Table, Badge | Show data |
| `typography` | text | Title, Text, Code, Divider | Text content |
| `charts` | charts | LineChart, BarChart, PieChart | Visualization |

## Step-by-Step: Adding a New Component

### 1. Python Component Definition (`cacao/server/ui.py`)

Add the component function. Two patterns exist:

**Leaf Component** (no children):
```python
def my_component(
    value: str,
    size: Literal["sm", "md", "lg"] = "md",
    disabled: bool = False,
    on_change: Callable | str | None = None,
    **props: Any,
) -> Component:
    """
    Brief description.

    Example:
        my_component("Hello", size="lg", on_change="update")
    """
    return _add_to_current_container(Component(
        type="MyComponent",  # Must match JS export name
        props={
            "value": value,
            "size": size,
            "disabled": disabled,
            "on_change": on_change,
            **props
        }
    ))
```

**Container Component** (has children):
```python
@contextmanager
def my_container(
    title: str | None = None,
    **props: Any,
):
    """
    Container description.

    Example:
        with my_container("Section"):
            text("Content inside")
    """
    component = Component(
        type="MyContainer",
        props={"title": title, **props}
    )
    with _container_context(component):
        yield component
```

### 2. Simple API Wrapper (`cacao/simple.py`)

Add a wrapper that calls `_ensure_context()`:

```python
# Import at top (add to existing import list)
from .server.ui import (
    my_component as _my_component,
)

# Add wrapper function
def my_component(
    value: str,
    size: Literal["sm", "md", "lg"] = "md",
    disabled: bool = False,
    on_change: Callable | str | None = None,
    **props: Any,
) -> Component:
    """Same docstring as ui.py."""
    _ensure_context()
    return _my_component(value=value, size=size, disabled=disabled, on_change=on_change, **props)

# Add to __all__ list at bottom
__all__ = [
    # ...existing exports...
    "my_component",
]
```

### 3. React Component (`cacao/frontend/src/components/{category}/MyComponent.js`)

```javascript
/**
 * MyComponent - Brief description
 */

const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function MyComponent({ props }) {
  const {
    value,
    size = 'md',
    disabled = false,
    signal,
    on_change,
  } = props;

  // Local state (if needed)
  const [localValue, setLocalValue] = useState(value || '');

  // Signal subscription (if component uses signals)
  const signalName = signal?.__signal__;

  useEffect(() => {
    if (signalName) {
      const unsubscribe = cacaoWs.subscribe((signals) => {
        if (signals[signalName] !== undefined) {
          setLocalValue(signals[signalName]);
        }
      });
      // Get initial value
      const initial = cacaoWs.getSignal(signalName);
      if (initial !== undefined) {
        setLocalValue(initial);
      }
      return unsubscribe;
    }
  }, [signalName]);

  // Event handler
  const handleChange = (e) => {
    const newValue = e.target.value;
    setLocalValue(newValue);

    // Send event to server/static handler
    const eventName = on_change?.__event__ || on_change;
    if (eventName) {
      cacaoWs.sendEvent(eventName, { value: newValue });
    }
  };

  return h('div', { className: `my-component my-component-${size}` }, [
    h('span', { key: 'content' }, localValue)
  ]);
}
```

### 4. Export Component (`cacao/frontend/src/components/{category}/index.js`)

```javascript
// Add to existing exports
export { MyComponent } from './MyComponent.js';
```

### 5. LESS Styles (`cacao/frontend/src/styles/components/{category}.less`)

```less
// MyComponent
.my-component {
  display: flex;
  padding: 0.5rem;
  border-radius: @radius-md;
  background: var(--bg-secondary);
  color: var(--text-primary);
  transition: all 0.15s ease;

  &:hover {
    background: var(--bg-tertiary);
  }

  &:disabled, &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.my-component-sm { font-size: @font-size-sm; }
.my-component-md { font-size: @font-size-base; }
.my-component-lg { font-size: @font-size-lg; }
```

Make sure to import in `styles/index.less` if creating a new category file.

### 6. Static Handler (if needed) (`cacao/frontend/src/handlers/{category}.js`)

Only needed if component triggers events that need client-side logic for static builds:

```javascript
export const myHandlers = {
  my_component_update: (signals, data) => {
    const value = data.value || '';
    // Process and update signals
    signals.set('my_output', value.toUpperCase());
  },
};
```

Add to `handlers/index.js`:
```javascript
import { myHandlers } from './my-handlers.js';

export const builtinHandlers = {
  ...existingHandlers,
  ...myHandlers,
};
```

### 7. Build and Test

```bash
# Rebuild frontend (from cacao/frontend)
npm run build

# Test with an example
cd examples
python -c "
import cacao as c
c.config(title='Test')
c.my_component('Hello', size='lg')
" > test.py
cacao run test.py
```

## Props Conventions

| Prop Pattern | Python Type | JS Access | Use |
|--------------|-------------|-----------|-----|
| `signal` | `Signal[T]` | `props.signal?.__signal__` | Two-way binding |
| `on_*` | `Callable \| str` | `props.on_*?.__event__ \|\| props.on_*` | Events |
| `variant` | `Literal[...]` | `props.variant` | Visual styles |
| `size` | `Literal["sm","md","lg"]` | `props.size` | Size variations |
| `disabled` | `bool` | `props.disabled` | Disable state |

## CSS Variables (use these, don't hardcode colors)

```less
// Backgrounds
var(--bg-primary)      // Main background
var(--bg-secondary)    // Cards, elevated surfaces
var(--bg-tertiary)     // Inputs, hover states

// Text
var(--text-primary)    // Main text
var(--text-secondary)  // Less prominent
var(--text-muted)      // Labels, hints

// Accent
var(--accent-primary)  // Primary actions, focus
var(--accent-hover)    // Hover state

// Status
var(--success), var(--warning), var(--danger), var(--info)

// Borders
var(--border-color)
```

## Checklist

Before submitting a new component:

- [ ] Python function in `ui.py` with docstring and example
- [ ] Simple API wrapper in `simple.py`
- [ ] Added to `__all__` in `simple.py`
- [ ] React component in `frontend/src/components/{category}/`
- [ ] Exported in `frontend/src/components/{category}/index.js`
- [ ] LESS styles in `frontend/src/styles/components/`
- [ ] Static handler if component triggers custom events
- [ ] `npm run build` runs without errors
- [ ] Component renders correctly in browser
- [ ] Signal binding works (if applicable)
- [ ] Events fire correctly (if applicable)
- [ ] Static build works: `cacao build app.py`

## Common Patterns

### Reading Signal Values in JS
```javascript
const signalName = props.some_signal?.__signal__;
const value = cacaoWs.getSignal(signalName);
```

### Sending Events
```javascript
const eventName = props.on_click?.__event__ || props.on_click;
if (eventName) {
  cacaoWs.sendEvent(eventName, { value: someData });
}
```

### Container with Filtered Children
```javascript
export function MyContainer({ props, children }) {
  const headerChildren = children.filter(c => c?.props?.type === 'Header');
  const bodyChildren = children.filter(c => c?.props?.type !== 'Header');

  return h('div', { className: 'my-container' }, [
    h('header', { key: 'header' }, headerChildren),
    h('main', { key: 'body' }, bodyChildren),
  ]);
}
```
