"""
Accordion FAQ
=============
Demonstrates accordion components to build a frequently
asked questions page. Each section expands to reveal
the answer when clicked.
"""

import cacao as c

c.config(title="FAQ - Accordion Demo", theme="dark")

c.title("Frequently Asked Questions")
c.text("Click on any question to reveal the answer.", color="gray")

c.divider()

with c.accordion():
    with c.accordion_item(label="What is Cacao?"):
        c.text(
            "Cacao is a high-performance reactive web framework for Python. "
            "It lets you build interactive dashboards, internal tools, and "
            "data applications using a fluent Python API with real-time updates."
        )

    with c.accordion_item(label="Do I need to know JavaScript?"):
        c.text(
            "No! Cacao handles the frontend automatically. You write pure Python "
            "and the framework generates the UI. However, advanced users can "
            "extend components with custom JavaScript if desired."
        )

    with c.accordion_item(label="How does real-time updating work?"):
        c.text(
            "Cacao uses WebSockets to maintain a persistent connection between "
            "the server and browser. When a signal value changes on the server, "
            "the update is pushed instantly to the client."
        )
        c.code(
            'counter = c.signal(0, name="counter")\n\n'
            '@c.on("increment")\n'
            "async def increment(session, event):\n"
            "    counter.set(counter.value + 1)",
            language="python",
        )

    with c.accordion_item(label="Can I deploy without a server?"):
        c.text(
            "Yes! Cacao supports static builds for serverless deployment on "
            "platforms like GitHub Pages. Use the command:"
        )
        c.code("cacao build app.py --base-path /my-repo", language="bash")
        c.text(
            "Note that static builds have limited interactivity compared to "
            "the WebSocket-powered server mode."
        )

    with c.accordion_item(label="What databases are supported?"):
        c.text(
            "Cacao is database-agnostic. Since your backend is plain Python, "
            "you can use any database library: SQLAlchemy, Peewee, pymongo, "
            "Redis, or direct connections via psycopg2, sqlite3, etc."
        )

    with c.accordion_item(label="Is authentication built-in?"):
        c.text("Yes, Cacao provides a simple authentication mechanism:")
        c.code(
            'c.require_auth(users={\n'
            '    "admin": "secret123",\n'
            '    "viewer": "readonly"\n'
            "})",
            language="python",
        )
        c.text(
            "For production use, you can integrate with OAuth providers "
            "or your own authentication backend."
        )

c.divider()
c.text("Still have questions? Reach out on GitHub.", size="sm", color="gray")
