"""
Keyboard Shortcuts
==================
Demonstrates keyboard shortcut bindings for common actions.
Shows how to register shortcuts, display a help overlay,
and trigger application behavior from key combinations.
"""

import cacao as c

c.config(title="Keyboard Shortcuts", theme="dark")

counter = c.signal(0, name="counter")
last_action = c.signal("None yet", name="last_action")
theme_mode = c.signal("dark", name="theme_mode")

# Register keyboard shortcuts
c.shortcut("ctrl+k", "open_search", description="Open search")
c.shortcut("ctrl+s", "save_document", description="Save document")
c.shortcut("ctrl+z", "undo_action", description="Undo last action")
c.shortcut("ctrl+shift+n", "new_item", description="Create new item")
c.shortcut("ctrl+up", "increment", description="Increment counter")
c.shortcut("ctrl+down", "decrement", description="Decrement counter")
c.shortcut("ctrl+shift+t", "toggle_theme", description="Toggle theme")
c.shortcut("escape", "clear_all", description="Clear / Reset")

c.title("Keyboard Shortcuts Demo")
c.text("Use keyboard shortcuts to interact with this app. Press any combo below.")

c.spacer(size=2)

with c.row():
    with c.col(span=6):
        with c.card(title="Shortcut Reference"):
            c.table(
                [
                    {"shortcut": "Ctrl + K", "action": "Open search"},
                    {"shortcut": "Ctrl + S", "action": "Save document"},
                    {"shortcut": "Ctrl + Z", "action": "Undo last action"},
                    {"shortcut": "Ctrl + Shift + N", "action": "Create new item"},
                    {"shortcut": "Ctrl + Up", "action": "Increment counter"},
                    {"shortcut": "Ctrl + Down", "action": "Decrement counter"},
                    {"shortcut": "Ctrl + Shift + T", "action": "Toggle theme"},
                    {"shortcut": "Escape", "action": "Clear / Reset"},
                ],
                columns=["shortcut", "action"],
            )

    with c.col(span=6):
        with c.card(title="Status"):
            c.metric("Counter", signal="counter")
            c.spacer(size=2)
            c.text("Last Action:", size="sm", color="gray")
            c.text(signal="last_action", size="lg")

c.spacer(size=2)

with c.card(title="Or Use Buttons"):
    c.text("If you prefer clicking, these buttons trigger the same actions.", size="sm", color="gray")
    c.spacer(size=1)
    with c.row():
        c.button("Search (Ctrl+K)", variant="primary", on_click="open_search")
        c.button("Save (Ctrl+S)", variant="primary", on_click="save_document")
        c.button("New (Ctrl+Shift+N)", variant="secondary", on_click="new_item")
        c.button("Reset (Esc)", variant="danger", on_click="clear_all")


@c.on("open_search")
async def open_search(session, event):
    last_action.set("Opened search dialog")
    c.toast("Search opened! (Ctrl+K)", variant="info")


@c.on("save_document")
async def save_document(session, event):
    last_action.set("Document saved")
    c.toast("Document saved! (Ctrl+S)", variant="success")


@c.on("undo_action")
async def undo_action(session, event):
    last_action.set("Undo performed")
    c.toast("Undo! (Ctrl+Z)", variant="warning")


@c.on("new_item")
async def new_item(session, event):
    last_action.set("New item created")
    c.toast("New item created! (Ctrl+Shift+N)", variant="success")


@c.on("increment")
async def increment(session, event):
    counter.set(counter.value + 1)
    last_action.set(f"Incremented to {counter.value}")


@c.on("decrement")
async def decrement(session, event):
    counter.set(counter.value - 1)
    last_action.set(f"Decremented to {counter.value}")


@c.on("toggle_theme")
async def toggle_theme(session, event):
    new_mode = "light" if theme_mode.value == "dark" else "dark"
    theme_mode.set(new_mode)
    last_action.set(f"Theme set to {new_mode}")
    c.toast(f"Theme toggled to {new_mode} mode!", variant="info")


@c.on("clear_all")
async def clear_all(session, event):
    counter.set(0)
    last_action.set("Everything reset")
    c.toast("Reset complete! (Escape)", variant="info")
