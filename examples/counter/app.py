"""Counter - signals and event handling."""
import cacao as c

c.config(title="Counter")

count = c.signal(0, name="count")


@c.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + event.get("amount", 1))


@c.on("decrement")
async def decrement(session, event):
    count.set(session, count.get(session) - event.get("amount", 1))


@c.on("reset")
async def reset(session, event):
    count.set(session, 0)


c.title("Counter")

with c.card():
    c.metric("Count", count)
    with c.row():
        c.button("-", on_click="decrement", variant="secondary")
        c.button("+", on_click="increment")
        c.button("Reset", on_click="reset", variant="ghost")
