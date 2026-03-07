"""
Chat App Recipe
===============
A simple chat interface with a manual on_send handler.
No LLM provider needed -- the bot echoes messages back
with some fun transformations.

Run: cacao run docs/cookbook/chat_app.py
"""

import cacao as c
from datetime import datetime

c.config(title="Chat App", theme="dark")

messages = c.signal([], name="messages")
user_input = c.signal("", name="user_input")

c.title("Simple Chat", level=1)
c.text("Type a message and press Send. The bot will echo it back.", color="dimmed")
c.divider()

with c.card(title="Chat Room"):
    c.json(messages)
    c.spacer(size=2)
    with c.row():
        with c.col(span=9):
            c.input("Message", signal="user_input", placeholder="Type something...")
        with c.col(span=3):
            c.button("Send", variant="primary", on_click="send_message")
            c.button("Clear", variant="ghost", on_click="clear_chat")


def bot_reply(text: str) -> str:
    """Generate a simple bot response."""
    lower = text.lower().strip()
    if lower in ("hello", "hi", "hey"):
        return "Hey there! How can I help?"
    if "time" in lower:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    if lower.endswith("?"):
        return "Good question! Let me think about that..."
    return f'You said: "{text}" -- interesting!'


@c.on("send_message")
async def handle_send(session, event):
    text = session.get("user_input", "").strip()
    if not text:
        return
    current = session.get("messages", [])
    current.append({"role": "user", "text": text, "time": datetime.now().strftime("%H:%M")})
    reply = bot_reply(text)
    current.append({"role": "bot", "text": reply, "time": datetime.now().strftime("%H:%M")})
    session.set("messages", current)
    session.set("user_input", "")


@c.on("clear_chat")
async def handle_clear(session, event):
    session.set("messages", [])
