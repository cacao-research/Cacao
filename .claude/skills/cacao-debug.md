---
name: cacao-debug
description: Debug common Cacao issues. Use when troubleshooting signal sync problems, events not firing, components not rendering, static build failures, or WebSocket disconnections.
---

# Cacao Debugging Guide

Quick reference for diagnosing and fixing common Cacao issues.

## Quick Diagnosis

| Symptom | Likely Cause | Section |
|---------|--------------|---------|
| Component not showing | Missing export, typo in type name | [Rendering](#rendering-issues) |
| Signal not updating UI | Wrong signal name, missing subscription | [Signals](#signal-issues) |
| Button click does nothing | Event name mismatch, handler not registered | [Events](#event-issues) |
| Static build broken | Handler not in JS, missing from bundle | [Static Build](#static-build-issues) |
| WebSocket disconnecting | Server crash, CORS, network | [WebSocket](#websocket-issues) |
| Styles not applied | Class name wrong, LESS not compiled | [Styling](#styling-issues) |

## Rendering Issues

### Component Not Appearing

**Check 1: Python type matches JS export**
```python
# Python (ui.py)
Component(type="MyWidget", ...)  # type="MyWidget"
```
```javascript
// JS - must export same name
export function MyWidget({ props }) { ... }
```

**Check 2: Component exported in index.js**
```javascript
// components/form/index.js
export { MyWidget } from './MyWidget.js';
```

**Check 3: Category imported in main index**
```javascript
// components/index.js
import * as form from './form/index.js';
const renderers = { ...form, ... };
```

**Check 4: Rebuild after changes**
```bash
cd cacao/frontend && npm run build
```

### Component Shows `[TypeName]` Warning

Console shows: `Unknown component type: TypeName`

Fix: The JS component isn't exported or name doesn't match Python `type`.

### Children Not Rendering

```javascript
// Wrong - ignoring children
export function MyContainer({ props }) {
  return h('div', {}, 'content');
}

// Right - render children
export function MyContainer({ props, children }) {
  return h('div', {}, children);
}
```

## Signal Issues

### Signal Value Not Showing

**Check 1: Signal has a name**
```python
# Wrong
count = c.signal(0)

# Right
count = c.signal(0, name="count")
```

**Check 2: Pass signal to component**
```python
# Wrong - passing value
c.metric("Count", count.get())

# Right - passing signal
c.metric("Count", count)
```

**Check 3: JS component subscribes to signal**
```javascript
const signalName = props.value?.__signal__;

useEffect(() => {
  if (signalName) {
    const unsubscribe = cacaoWs.subscribe((signals) => {
      setValue(signals[signalName]);
    });
    return unsubscribe;
  }
}, [signalName]);
```

### Signal Updates Not Reflecting

**Debug: Check WebSocket messages**

Open browser DevTools → Network → WS → Messages

You should see:
```json
{"type": "update", "changes": {"signal_name": "new_value"}}
```

If not seeing updates:
1. Check handler is being called (add print statement)
2. Check signal name matches
3. Check session is correct

**Debug: Check signals in console**
```javascript
// In browser console
window.__cacao_signals__
```

## Event Issues

### Event Not Firing

**Check 1: Event name matches handler**
```python
# Python
c.button("Click", on_click="my_event")

@c.on("my_event")  # Must match exactly
async def handler(session, event):
    print("Fired!")
```

**Check 2: Handler is async**
```python
# Wrong
@c.on("my_event")
def handler(session, event):  # Missing async
    pass

# Right
@c.on("my_event")
async def handler(session, event):
    pass
```

**Check 3: JS sends correct event name**
```javascript
const eventName = props.on_click?.__event__ || props.on_click;
cacaoWs.sendEvent(eventName, { value: data });
```

**Debug: Check console for events**
```
[Cacao] Sending event: {type: "event", name: "my_event", data: {...}}
```

### Event Data Missing

**Check what data the component sends:**
```javascript
// In your JS component
cacaoWs.sendEvent(eventName, { value: inputValue });
                              // ↑ This becomes event.get("value")
```

```python
@c.on("input_change")
async def handler(session, event):
    value = event.get("value")  # Access the data
    print(f"Got: {value}")
```

## Static Build Issues

### Handler Not Working in Static Mode

**Check 1: Handler exists in JS**
```javascript
// handlers/my-handlers.js
export const myHandlers = {
  my_event: (signals, data) => {
    signals.set('output', data.value);
  },
};
```

**Check 2: Handler exported in index.js**
```javascript
// handlers/index.js
import { myHandlers } from './my-handlers.js';

export const builtinHandlers = {
  ...myHandlers,
};
```

**Check 3: Rebuilt after adding handler**
```bash
cd cacao/frontend && npm run build
```

### Static Build Command Fails

**Error: Frontend not built**
```bash
cd cacao/frontend && npm install && npm run build
```

**Error: Module not found**
```bash
pip install -e .  # Reinstall cacao in dev mode
```

**Error: No pages found**
```python
# Make sure app creates components
import cacao as c
c.config(title="App")
c.title("Hello")  # At least one component
```

### Routing Not Working on GitHub Pages

**Check 1: Base path set correctly**
```bash
# For repo: github.com/user/my-repo
cacao build app.py --base-path /my-repo
```

**Check 2: 404.html exists**
The build should create both `index.html` and `404.html`.

**Check 3: Using hash routing**
Static mode uses `#/route` not `/route`.

## WebSocket Issues

### Connection Failed

**Check 1: Server running**
```bash
cacao run app.py
# Should show: [Cacao] Starting server at http://127.0.0.1:1502
```

**Check 2: Correct port**
```javascript
// Browser connects to same host/port as page
ws://127.0.0.1:1502/ws
```

**Check 3: CORS (if different origin)**
Server already has CORS enabled for all origins in dev.

### Frequent Disconnections

**Check: Server errors**
```bash
cacao run app.py --verbose
```

Look for Python exceptions in terminal.

**Check: Handler crashes**
```python
@c.on("my_event")
async def handler(session, event):
    try:
        # your code
    except Exception as e:
        print(f"Error: {e}")
```

## Styling Issues

### Styles Not Applied

**Check 1: Class name correct**
```javascript
// JS component
return h('div', { className: 'my-widget' }, ...);
```
```less
// LESS
.my-widget {
  color: var(--text-primary);
}
```

**Check 2: LESS file imported**
```less
// styles/index.less
@import 'components/my-category.less';
```

**Check 3: Rebuilt CSS**
```bash
cd cacao/frontend && npm run build
```

### Theme Variables Not Working

Use CSS variables, not LESS variables for colors:

```less
// Wrong - won't respond to theme
.my-widget {
  color: #ffffff;
}

// Right - theme-aware
.my-widget {
  color: var(--text-primary);
  background: var(--bg-secondary);
}
```

## Debug Tools

### Browser Console Commands

```javascript
// Check all signals
window.__cacao_signals__

// Check if static mode
window.__CACAO_STATIC__

// Check component tree
window.__CACAO_PAGES__

// Manual event trigger
Cacao.dispatcher.dispatch('event_name', { value: 'test' })
```

### Server Logging

```bash
# Verbose mode
cacao run app.py --verbose
```

Or in code:
```python
app = c.get_app()
app.debug = True
```

### Python Debug

```python
@c.on("my_event")
async def handler(session, event):
    print(f"Session: {session.id}")
    print(f"Event: {event}")

    # Check signal value
    print(f"Current value: {my_signal.get(session)}")
```

## Common Fixes Summary

| Problem | Fix |
|---------|-----|
| Component not rendering | Check type name, exports, rebuild |
| Signal not updating | Check name, subscription, WebSocket |
| Event not firing | Check async, name match, handler registered |
| Static build fails | Check JS handler exists, exports, rebuild |
| Styles missing | Check class name, imports, rebuild |
| WebSocket error | Check server running, no handler crashes |
