"""
Counter - Interactive Signals Demo
===================================
A classic counter app demonstrating signals and event handlers.
Run with: cacao run counter.py
"""

import cacao as c

c.config(title="Counter App", theme="dark")

count = c.signal(0, name="count")

c.title("Counter")
c.text("Click the buttons to change the count.")

c.spacer(size=2)

with c.card(title="Current Count"):
    c.metric("Count", count)

    with c.row():
        with c.col(span=4):
            c.button("- Decrement", variant="danger", on_click="decrement")
        with c.col(span=4):
            c.button("Reset", variant="secondary", on_click="reset")
        with c.col(span=4):
            c.button("+ Increment", variant="primary", on_click="increment")


@c.on("increment")
async def increment(session, event):
    current = session.get("count")
    session.set("count", current + 1)


@c.on("decrement")
async def decrement(session, event):
    current = session.get("count")
    session.set("count", current - 1)


@c.on("reset")
async def reset(session, event):
    session.set("count", 0)
