"""
Markdown Editor
===============
A live markdown editor with a side-by-side preview pane.
Type markdown in the editor and see rendered output update
in real time using signals.
"""

import cacao as c

c.config(title="Markdown Editor", theme="dark")

default_content = """# Hello, Markdown!

This is a **live preview** editor built with Cacao.

## Features

- Real-time preview as you type
- Full markdown support
- Dark theme friendly

## Code Example

```python
import cacao as c

c.title("Hello World")
c.text("Built with Cacao!")
```

## Table

| Feature   | Status |
|-----------|--------|
| Bold      | Yes    |
| Italics   | Yes    |
| Code      | Yes    |
| Tables    | Yes    |

---

> Markdown is a lightweight markup language that you can use
> to add formatting elements to plaintext text documents.

Enjoy writing!
"""

md_content = c.signal(default_content, name="md_content")

c.title("Markdown Editor", level=1)
c.text("Write markdown on the left, see the rendered preview on the right.", color="gray")

c.spacer(size=2)

with c.row():
    c.button("Clear", variant="danger", on_click="clear_editor")
    c.button("Load Sample", variant="secondary", on_click="load_sample")
    c.button("Heading", variant="ghost", on_click="insert_heading")
    c.button("Bold", variant="ghost", on_click="insert_bold")
    c.button("Code Block", variant="ghost", on_click="insert_code")

c.spacer(size=1)

with c.row():
    with c.col(span=6):
        with c.card(title="Editor"):
            c.textarea(
                label="Markdown Source",
                signal="md_content",
                placeholder="Type your markdown here...",
            )

    with c.col(span=6):
        with c.card(title="Preview"):
            c.markdown(signal="md_content")


@c.on("clear_editor")
async def clear_editor(session, event):
    md_content.set("")
    c.toast("Editor cleared.", variant="info")


@c.on("load_sample")
async def load_sample(session, event):
    md_content.set(default_content)
    c.toast("Sample content loaded.", variant="success")


@c.on("insert_heading")
async def insert_heading(session, event):
    md_content.set(md_content.value + "\n## New Heading\n")


@c.on("insert_bold")
async def insert_bold(session, event):
    md_content.set(md_content.value + "**bold text**")


@c.on("insert_code")
async def insert_code(session, event):
    md_content.set(md_content.value + "\n```python\n# code here\n```\n")
