"""
Hello World - Minimal Cacao App
===============================
The simplest possible Cacao app: a title, some text, and a row of metrics.
Run with: cacao run hello_world.py
"""

import cacao as c

c.config(title="Hello World", theme="dark")

c.title("Welcome to Cacao")
c.text("A high-performance reactive web framework for Python.", size="lg")

c.divider()

with c.row():
    with c.col(span=4):
        c.metric("Uptime", "99.9%", trend="+0.1%", trend_direction="up")
    with c.col(span=4):
        c.metric("Requests", "12,847", trend="+342", trend_direction="up")
    with c.col(span=4):
        c.metric("Errors", "3", trend="-12", trend_direction="down")

c.spacer(size=4)

with c.card(title="About"):
    c.text("This is the simplest Cacao app you can build.")
    c.text("Edit this file and watch it hot-reload.", color="dimmed")
