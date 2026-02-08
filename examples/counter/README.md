# Counter Example

A simple counter demonstrating Cacao v2's core features:
- **Signal state management** - Session-scoped reactive state
- **Event handling** - Client-to-server events with typed data
- **Session isolation** - Each browser tab gets its own counter

## Running the Example

### 1. Start the Python Server

```bash
cd cacao/examples/counter
python server.py
```

The server will start at `http://localhost:1502` with WebSocket at `ws://localhost:1502/ws`.

### 2. Start the React Client

In a separate terminal:

```bash
cd cacao/client

# Install dependencies (first time only)
npm install

# Copy the example App.tsx (or update src/App.tsx to import from the example)
# Then start the dev server
npm run dev
```

The React app will start at `http://localhost:3000`.

### 3. Test Session Isolation

Open multiple browser tabs to `http://localhost:3000`. Each tab has its own counter that operates independently, demonstrating session isolation.

## How It Works

### Server (Python)

```python
from cacao import App, Signal

app = App()
count = Signal(0, name="count")

@app.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + 1)
```

- `Signal(0, name="count")` creates a session-scoped reactive state
- `@app.on("increment")` registers an async event handler
- `count.get(session)` gets the value for this specific session
- `count.set(session, value)` updates and auto-syncs to the client

### Client (React)

```tsx
import { useSignal, useEvent } from './cacao'

function Counter() {
  const count = useSignal('count', 0)
  const increment = useEvent('increment')

  return (
    <button onClick={() => increment()}>
      Count: {count}
    </button>
  )
}
```

- `useSignal('count', 0)` subscribes to the 'count' signal with default 0
- `useEvent('increment')` returns a function to dispatch 'increment' events
- State updates are automatic via WebSocket
