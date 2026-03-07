"""
Sidebar Layout
==============
Demonstrates the sidebar layout preset with navigation
and content areas. Shows how to build a multi-section
app with a persistent sidebar.
"""

import cacao as c

c.config(title="Sidebar Layout", theme="dark")
c.layout("sidebar")

current_page = c.signal("dashboard", name="current_page")

with c.page("/"):
    c.title("Dashboard", level=2)
    c.text("Welcome to the dashboard. Select a section from the sidebar.")

    with c.row():
        with c.col(span=4):
            c.metric("Users", "1,284", trend="+12%", trend_direction="up")
        with c.col(span=4):
            c.metric("Revenue", "$48,200", trend="+8.3%", trend_direction="up")
        with c.col(span=4):
            c.metric("Orders", "384", trend="-2.1%", trend_direction="down")

    with c.card(title="Recent Activity"):
        c.table(
            [
                {"time": "2 min ago", "user": "Alice", "action": "Placed order #1042"},
                {"time": "15 min ago", "user": "Bob", "action": "Updated profile"},
                {"time": "1 hr ago", "user": "Carol", "action": "Submitted report"},
                {"time": "3 hr ago", "user": "Dave", "action": "Created account"},
            ],
            columns=["time", "user", "action"],
        )

with c.page("/analytics"):
    c.title("Analytics", level=2)
    c.text("Sales performance over the last 6 months.")

    sales_data = [
        {"month": "Oct", "sales": 4200},
        {"month": "Nov", "sales": 5100},
        {"month": "Dec", "sales": 6800},
        {"month": "Jan", "sales": 5400},
        {"month": "Feb", "sales": 6100},
        {"month": "Mar", "sales": 7200},
    ]
    c.bar(sales_data, x="month", y="sales")

with c.page("/settings"):
    c.title("Settings", level=2)
    with c.card(title="Preferences"):
        c.switch(label="Dark mode", signal="dark_mode")
        c.switch(label="Email notifications", signal="email_notif")
        c.select(
            label="Language",
            options=["English", "Spanish", "French", "German"],
            signal="language",
        )
        c.button("Save Settings", variant="primary", on_click="save_settings")


@c.on("save_settings")
async def save_settings(session, event):
    c.toast("Settings saved successfully!", variant="success")
