"""
CRUD App - Create, Read, Update, Delete Records
=================================================
Demonstrates form inputs, signals, table display, and event-driven mutations.
Run with: cacao run crud_app.py
"""

import cacao as c

c.config(title="CRUD App", theme="dark")

records = c.signal(
    [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "Editor"},
        {"id": 3, "name": "Carol", "email": "carol@example.com", "role": "Viewer"},
    ],
    name="records",
)
edit_name = c.signal("", name="edit_name")
edit_email = c.signal("", name="edit_email")
edit_role = c.signal("Viewer", name="edit_role")
next_id = c.signal(4, name="next_id")

c.title("User Management")

with c.card(title="Add / Edit User"):
    with c.row():
        with c.col(span=4):
            c.input("Name", signal="edit_name", placeholder="Full name")
        with c.col(span=4):
            c.input("Email", signal="edit_email", placeholder="user@example.com")
        with c.col(span=4):
            c.select(
                "Role",
                options=["Admin", "Editor", "Viewer"],
                signal="edit_role",
            )
    c.spacer(size=2)
    with c.row():
        with c.col(span=6):
            c.button("Add User", variant="primary", on_click="add_record")
        with c.col(span=6):
            c.button("Clear Form", variant="secondary", on_click="clear_form")

c.spacer(size=2)

with c.card(title="Users"):
    c.table(
        records,
        columns=[
            {"key": "id", "label": "ID"},
            {"key": "name", "label": "Name"},
            {"key": "email", "label": "Email"},
            {"key": "role", "label": "Role"},
        ],
    )
    c.button("Delete Last", variant="danger", on_click="delete_last")


@c.on("add_record")
async def add_record(session, event):
    name = session.get("edit_name")
    email = session.get("edit_email")
    role = session.get("edit_role")
    if not name or not email:
        return
    nid = session.get("next_id")
    current = session.get("records")
    current.append({"id": nid, "name": name, "email": email, "role": role})
    session.set("records", current)
    session.set("next_id", nid + 1)
    session.set("edit_name", "")
    session.set("edit_email", "")
    session.set("edit_role", "Viewer")


@c.on("clear_form")
async def clear_form(session, event):
    session.set("edit_name", "")
    session.set("edit_email", "")
    session.set("edit_role", "Viewer")


@c.on("delete_last")
async def delete_last(session, event):
    current = session.get("records")
    if current:
        current.pop()
        session.set("records", current)
