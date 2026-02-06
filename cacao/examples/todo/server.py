"""
Todo Example - Cacao v2

A todo list demonstrating:
- Form input binding
- List state management
- Computed signals
- Multiple event handlers

Run with: python server.py
"""

import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cacao import App, Signal
from cacao.server.signal import Computed

# Create app
app = App(debug=True)


@dataclass
class Todo:
    id: int
    text: str
    completed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Signals
todos = Signal[list[dict[str, Any]]]([], name="todos")
new_todo_text = Signal("", name="newTodoText")
filter_mode = Signal("all", name="filterMode")  # all, active, completed

# Auto-bind input fields
app.bind("newTodoText:input", new_todo_text)
app.bind("filterMode:input", filter_mode)


# Counter for unique IDs per session
todo_counters: dict[str, int] = {}


def get_next_id(session_id: str) -> int:
    if session_id not in todo_counters:
        todo_counters[session_id] = 0
    todo_counters[session_id] += 1
    return todo_counters[session_id]


@app.on("todo:add")
async def add_todo(session, event):
    """Add a new todo item."""
    text = new_todo_text.get(session).strip()
    if not text:
        return

    current_todos = todos.get(session).copy()
    new_item = Todo(
        id=get_next_id(session.id),
        text=text,
        completed=False,
    )
    current_todos.append(new_item.to_dict())

    todos.set(session, current_todos)
    new_todo_text.set(session, "")  # Clear input


@app.on("todo:toggle")
async def toggle_todo(session, event):
    """Toggle a todo's completed status."""
    todo_id = event.get("id")
    if todo_id is None:
        return

    current_todos = todos.get(session).copy()
    for todo in current_todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            break

    todos.set(session, current_todos)


@app.on("todo:delete")
async def delete_todo(session, event):
    """Delete a todo item."""
    todo_id = event.get("id")
    if todo_id is None:
        return

    current_todos = todos.get(session)
    updated_todos = [t for t in current_todos if t["id"] != todo_id]
    todos.set(session, updated_todos)


@app.on("todo:clear-completed")
async def clear_completed(session, event):
    """Remove all completed todos."""
    current_todos = todos.get(session)
    active_todos = [t for t in current_todos if not t["completed"]]
    todos.set(session, active_todos)


@app.on("todo:toggle-all")
async def toggle_all(session, event):
    """Toggle all todos."""
    current_todos = todos.get(session).copy()
    all_completed = all(t["completed"] for t in current_todos) if current_todos else False

    for todo in current_todos:
        todo["completed"] = not all_completed

    todos.set(session, current_todos)


if __name__ == "__main__":
    app.run(port=1634)
