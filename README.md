# Cacao v2

A clean-slate rewrite of Cacao with a clear separation of concerns:
- **Python Server**: Manages state (Signals) and handles events
- **React Client**: Renders the UI and dispatches events
- **WebSocket**: JSON state sync between server and client

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r cacao_v2/requirements.txt
```

### 2. Create a Simple Server

```python
# app.py
from cacao_v2 import App, Signal

app = App()
count = Signal(0, name="count")

@app.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + 1)

if __name__ == "__main__":
    app.run(port=8000)
```

### 3. Set Up the React Client

```bash
cd cacao_v2/client
npm install
npm run dev
```

### 4. Use Signals in React

```tsx
import { CacaoProvider, useSignal, useEvent } from './cacao'

function Counter() {
  const count = useSignal('count', 0)
  const increment = useEvent('increment')

  return (
    <button onClick={() => increment()}>
      Count: {count}
    </button>
  )
}

export default function App() {
  return (
    <CacaoProvider url="ws://localhost:8000/ws">
      <Counter />
    </CacaoProvider>
  )
}
```

## Core Concepts

### Signals (Server-Side State)

Signals are reactive state containers with session scoping:

```python
from cacao_v2 import Signal

# Create a signal with a default value
name = Signal("", name="name")

# Get value for a session
current_name = name.get(session)

# Set value (automatically syncs to client)
name.set(session, "John")

# Update using a function
name.update(session, lambda n: n.upper())
```

### Events (Client-to-Server)

Events are the mechanism for client actions:

```python
@app.on("submit")
async def handle_submit(session, event):
    # event is a dict with the data from the client
    print(event.get("value"))
```

### Auto-Binding (Form Helpers)

Bind events directly to signals for form inputs:

```python
name = Signal("", name="name")
app.bind("name:input", name)  # Auto-updates signal on input

# Client just sends: { type: "event", name: "name:input", data: { value: "..." } }
```

### React Hooks

```tsx
// Subscribe to a signal
const count = useSignal<number>('count', 0)

// Create an event dispatcher
const submit = useEvent('submit')
submit({ value: 'hello' })

// Check connection status
const status = useConnectionStatus()  // 'connecting' | 'connected' | 'disconnected' | 'reconnecting'

// Get session ID
const sessionId = useSessionId()
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PYTHON SERVER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Signals  │  │ Sessions │  │  Events  │  │ WebSocket/HTTP│   │
│  │ (state)  │──│ (per-    │──│ (typed   │──│    Server     │   │
│  │          │  │  client) │  │  async)  │  │               │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────┬───────┘   │
└────────────────────────────────────────────────────┼───────────┘
                                                     │ JSON
                                                     │ WebSocket
┌────────────────────────────────────────────────────┼───────────┐
│                      REACT CLIENT                   │           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┴──────┐    │
│  │  Hooks   │  │Components│  │  Event   │  │   State     │    │
│  │useCacao()│──│ (your UI)│──│Dispatcher│──│   Store     │    │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## WebSocket Protocol

### Server → Client

```json
// Initial state
{ "type": "init", "state": { "count": 0 }, "sessionId": "abc123" }

// State update
{ "type": "update", "changes": { "count": 1 } }
```

### Client → Server

```json
// Event dispatch
{ "type": "event", "name": "increment", "data": {} }
```

## File Structure

```
cacao_v2/
├── server/                 # Python package
│   ├── __init__.py
│   ├── app.py              # App class, decorators
│   ├── signal.py           # Signal, Computed
│   ├── session.py          # Session management
│   ├── events.py           # Event handling
│   └── server.py           # WebSocket server
│
├── client/                 # React + Vite
│   ├── package.json
│   ├── src/
│   │   ├── cacao/          # Cacao client library
│   │   │   ├── index.ts
│   │   │   ├── hooks.ts
│   │   │   ├── store.ts
│   │   │   ├── websocket.ts
│   │   │   └── types.ts
│   │   └── App.tsx
│   └── ...
│
├── examples/
│   └── counter/            # Counter example
│
└── requirements.txt
```

## Examples

See `cacao_v2/examples/counter/` for a working example.
