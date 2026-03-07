"""
Theme Switcher Recipe
=====================
Demonstrates how to let users toggle between light and dark
themes at runtime using signals and event handlers.

Run: cacao run docs/cookbook/theme_switcher.py
"""

import cacao as c

c.config(title="Theme Switcher", theme="dark")

current_theme = c.signal("dark", name="current_theme")

c.title("Theme Switcher", level=1)
c.text("Click the buttons below to switch between themes.", color="dimmed")
c.divider()

with c.row():
    with c.col(span=4):
        with c.card(title="Theme Controls"):
            c.text("Select a theme:", size="md")
            c.spacer(size=1)
            c.button("Dark Theme", variant="primary", on_click="set_dark")
            c.button("Light Theme", variant="secondary", on_click="set_light")
            c.spacer(size=2)
            c.text("Current theme signal value:")
            c.badge(current_theme, variant="info")

    with c.col(span=8):
        with c.card(title="Preview Content"):
            c.text("This content updates to reflect the selected theme.")
            c.divider()
            with c.row():
                with c.col(span=4):
                    c.metric("Users", "1,234", trend="+12%", trend_direction="up")
                with c.col(span=4):
                    c.metric("Revenue", "$56K", trend="+8%", trend_direction="up")
                with c.col(span=4):
                    c.metric("Orders", "892", trend="-3%", trend_direction="down")
            c.spacer(size=2)
            c.alert("Theme changes are applied in real time via WebSocket.", variant="info")
            c.progress(67, label="Sample progress bar")

c.spacer(size=2)
with c.card(title="Sample Code"):
    c.code(
        'c.config(title="My App", theme="dark")  # or theme="light"',
        language="python",
    )


@c.on("set_dark")
async def handle_dark(session, event):
    session.set("current_theme", "dark")
    session.set_theme("dark")


@c.on("set_light")
async def handle_light(session, event):
    session.set("current_theme", "light")
    session.set_theme("light")
