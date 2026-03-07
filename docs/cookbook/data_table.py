"""
Data Table Recipe
=================
Displays sample data in a table with search filtering
and summary metrics. Uses c.sample_users_data() for
realistic demo content.

Run: cacao run docs/cookbook/data_table.py
"""

import cacao as c

c.config(title="Data Table", theme="dark")

search = c.signal("", name="search")
users = c.sample_users_data()

c.title("User Directory", level=1)
c.text("Browse and search through the user database.", color="dimmed")
c.divider()

with c.row():
    with c.col(span=3):
        c.metric("Total Users", len(users))
    with c.col(span=3):
        active = sum(1 for u in users if u.get("status") == "active")
        c.metric("Active", active, trend=f"{round(active / len(users) * 100)}%", trend_direction="up")
    with c.col(span=3):
        inactive = len(users) - active
        c.metric("Inactive", inactive)
    with c.col(span=3):
        roles = len(set(u.get("role", "") for u in users))
        c.metric("Unique Roles", roles)

c.spacer(size=2)

with c.card(title="Users Table"):
    c.search_input("Search users", signal="search", placeholder="Filter by name or email...")
    c.spacer(size=2)
    c.table(
        data=users,
        columns=[
            {"key": "id", "label": "ID"},
            {"key": "name", "label": "Name"},
            {"key": "email", "label": "Email"},
            {"key": "role", "label": "Role"},
            {"key": "status", "label": "Status"},
        ],
    )

c.spacer(size=2)
with c.card(title="Raw JSON Preview"):
    c.text("First 3 records shown below:", size="sm", color="dimmed")
    c.json(users[:3])
