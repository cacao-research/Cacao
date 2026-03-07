"""
Todo App - Add, Toggle, and Remove Tasks
==========================================
A simple todo list demonstrating signals, dynamic lists, and multiple events.
Run with: cacao run todo_app.py
"""

import cacao as c

c.config(title="Todo App", theme="dark")

todos = c.signal([], name="todos")
new_task = c.signal("", name="new_task")

c.title("Todo List")

with c.card(title="Add Task"):
    c.input("New task", signal="new_task", placeholder="What needs to be done?")
    c.button("Add", variant="primary", on_click="add_todo")

c.spacer(size=2)

with c.card(title="Tasks"):
    c.table(
        todos,
        columns=[
            {"key": "status", "label": "Status"},
            {"key": "task", "label": "Task"},
            {"key": "actions", "label": "Actions"},
        ],
    )

with c.row():
    with c.col(span=6):
        c.button("Clear Completed", variant="secondary", on_click="clear_completed")
    with c.col(span=6):
        c.button("Clear All", variant="danger", on_click="clear_all")


@c.on("add_todo")
async def add_todo(session, event):
    task_text = session.get("new_task")
    if not task_text or not task_text.strip():
        return
    current = session.get("todos")
    new_id = len(current) + 1
    current.append({"id": new_id, "status": "Pending", "task": task_text.strip(), "actions": "toggle | remove"})
    session.set("todos", current)
    session.set("new_task", "")


@c.on("clear_completed")
async def clear_completed(session, event):
    current = session.get("todos")
    remaining = [t for t in current if t["status"] != "Done"]
    session.set("todos", remaining)


@c.on("clear_all")
async def clear_all(session, event):
    session.set("todos", [])
