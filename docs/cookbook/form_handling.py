"""
Form Handling Recipe
====================
Demonstrates a form with various input types, validation logic,
and a submit handler that processes the collected data.

Run: cacao run docs/cookbook/form_handling.py
"""

import cacao as c

c.config(title="Form Handling", theme="dark")

name = c.signal("", name="name")
email = c.signal("", name="email")
role = c.signal("developer", name="role")
experience = c.signal(3, name="experience")
newsletter = c.signal(False, name="newsletter")
bio = c.signal("", name="bio")
submitted = c.signal(False, name="submitted")
error_msg = c.signal("", name="error_msg")

c.title("Registration Form", level=1)
c.text("Fill out the form below and click Submit.", color="dimmed")
c.divider()

with c.row():
    with c.col(span=6):
        with c.card(title="Your Details"):
            c.input("Full Name", signal="name", placeholder="Jane Doe")
            c.input("Email Address", signal="email", placeholder="jane@example.com")
            c.select("Role", options=["developer", "designer", "manager", "other"], signal="role")
            c.slider("Years of Experience", signal="experience", min=0, max=30, step=1)
            c.switch("Subscribe to newsletter", signal="newsletter")
            c.textarea("Short Bio", signal="bio", placeholder="Tell us about yourself...")
            c.spacer(size=2)
            c.button("Submit", variant="primary", on_click="submit_form")
            c.button("Reset", variant="ghost", on_click="reset_form")

    with c.col(span=6):
        with c.card(title="Form Preview"):
            c.text("Check your details before submitting.", size="sm", color="dimmed")
            c.divider()
            c.json({
                "name": name,
                "email": email,
                "role": role,
                "experience": experience,
                "newsletter": newsletter,
                "bio": bio,
            })
            c.alert(error_msg, title="Validation Error", variant="error")
            c.alert("Registration submitted successfully!", title="Success", variant="success")


@c.on("submit_form")
async def handle_submit(session, event):
    n = session.get("name", "")
    e = session.get("email", "")
    if not n.strip():
        session.set("error_msg", "Name is required.")
        session.set("submitted", False)
        return
    if not e.strip() or "@" not in e:
        session.set("error_msg", "A valid email is required.")
        session.set("submitted", False)
        return
    session.set("error_msg", "")
    session.set("submitted", True)


@c.on("reset_form")
async def handle_reset(session, event):
    session.set("name", "")
    session.set("email", "")
    session.set("role", "developer")
    session.set("experience", 3)
    session.set("newsletter", False)
    session.set("bio", "")
    session.set("submitted", False)
    session.set("error_msg", "")
