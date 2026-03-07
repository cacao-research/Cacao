"""Todo list - form binding, list state, multiple handlers."""
from __future__ import annotations

import cacao as c
from cacao.server.session import Session

c.config(title="Todo")

todos = c.signal([], name="todos")
new_text = c.signal("", name="new_text")

c.bind("update_text", new_text)

_counters: dict[str, int] = {}


def _next_id(sid: str) -> int:
    _counters[sid] = _counters.get(sid, 0) + 1
    return _counters[sid]


@c.on("add_todo")
async def add_todo(session: Session, event: dict) -> None:
    text = new_text.get(session).strip()
    if not text:
        return
    items = todos.get(session).copy()
    items.append({"id": _next_id(session.id), "text": text, "done": False})
    todos.set(session, items)
    new_text.set(session, "")


@c.on("toggle_todo")
async def toggle_todo(session: Session, event: dict) -> None:
    tid = event.get("id")
    items = [
        {**t, "done": not t["done"]} if t["id"] == tid else t
        for t in todos.get(session)
    ]
    todos.set(session, items)


@c.on("delete_todo")
async def delete_todo(session: Session, event: dict) -> None:
    tid = event.get("id")
    todos.set(session, [t for t in todos.get(session) if t["id"] != tid])


@c.on("clear_done")
async def clear_done(session: Session, event: dict) -> None:
    todos.set(session, [t for t in todos.get(session) if not t["done"]])


# --- UI ---
c.title("Todo")

with c.card():
    with c.row():
        c.input("What needs to be done?", signal=new_text, on_change="update_text")
        c.button("Add", on_click="add_todo")

c.spacer()
c.table(todos, columns=["text", "done"])
c.spacer()
c.button("Clear completed", on_click="clear_done", variant="ghost")
