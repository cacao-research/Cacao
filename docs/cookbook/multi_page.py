"""
Multi-Page App - Sidebar Navigation
=====================================
Demonstrates c.page() and c.layout("sidebar") for multi-page applications.
Run with: cacao run multi_page.py
"""

import cacao as c

c.config(title="Multi-Page App", theme="dark")
c.layout("sidebar")

# --- Home Page ---
with c.page("/"):
    c.title("Home")
    c.text("Welcome to the multi-page Cacao app.", size="lg")

    with c.row():
        with c.col(span=4):
            c.metric("Pages", "3")
        with c.col(span=4):
            c.metric("Components", "12")
        with c.col(span=4):
            c.metric("Status", "Live")

    c.spacer(size=2)
    with c.card(title="Getting Started"):
        c.text("Use the sidebar to navigate between pages.")
        c.text("Each page is defined with c.page('/path') as a context manager.", color="dimmed")

# --- Analytics Page ---
with c.page("/analytics"):
    c.title("Analytics")
    c.text("Track your key metrics here.", size="lg")

    c.divider()

    with c.row():
        with c.col(span=6):
            with c.card(title="Weekly Visitors"):
                c.line(
                    [
                        {"day": "Mon", "visitors": 120},
                        {"day": "Tue", "visitors": 185},
                        {"day": "Wed", "visitors": 210},
                        {"day": "Thu", "visitors": 195},
                        {"day": "Fri", "visitors": 260},
                    ],
                    x="day",
                    y="visitors",
                )
        with c.col(span=6):
            with c.card(title="Traffic Sources"):
                c.pie(
                    [
                        {"source": "Organic", "count": 420},
                        {"source": "Direct", "count": 310},
                        {"source": "Referral", "count": 180},
                        {"source": "Social", "count": 90},
                    ],
                    values="count",
                    names="source",
                )

# --- Settings Page ---
with c.page("/settings"):
    c.title("Settings")
    c.text("Configure your application preferences.", size="lg")

    c.divider()

    with c.card(title="Preferences"):
        c.switch("Enable notifications", signal="notifications")
        c.switch("Dark mode", signal="dark_mode")
        c.select(
            "Language",
            options=["English", "Spanish", "French", "German"],
            signal="language",
        )
        c.slider("Font size", signal="font_size", min=12, max=24, step=1)

    c.spacer(size=2)

    with c.card(title="Profile"):
        c.input("Display Name", signal="display_name", placeholder="Your name")
        c.textarea("Bio", signal="bio")
        c.button("Save Settings", variant="primary", on_click="save_settings")

    @c.on("save_settings")
    async def save_settings(session, event):
        c.toast("Settings saved!", variant="success")
