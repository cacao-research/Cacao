"""
Counter Example - Cacao v2

A simple counter demonstrating:
- Signal state management
- Event handling
- Session isolation

Run with: python server.py
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cacao_v2 import App, Signal

# Create app
app = App(debug=True)

# Create a signal for the counter
# Each session gets its own count value
count = Signal(0, name="count")


@app.on("increment")
async def increment(session, event):
    """Handle increment event."""
    amount = event.get("amount", 1)
    current = count.get(session)
    count.set(session, current + amount)


@app.on("decrement")
async def decrement(session, event):
    """Handle decrement event."""
    amount = event.get("amount", 1)
    current = count.get(session)
    count.set(session, current - amount)


@app.on("reset")
async def reset(session, event):
    """Handle reset event."""
    count.set(session, 0)


if __name__ == "__main__":
    app.run(port=8080)
