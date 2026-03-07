"""
Auth Flow - Login-Protected App
================================
Demonstrates c.require_auth to protect an app with username/password login.
Run with: cacao run auth_flow.py

Default credentials:
  admin / admin123
  viewer / view456
"""

import cacao as c

c.config(title="Protected App", theme="dark")

c.require_auth(
    users={
        "admin": "admin123",
        "viewer": "view456",
    }
)

c.title("Protected Dashboard")
c.alert(
    "You are logged in! This content is only visible to authenticated users.",
    title="Authenticated",
    variant="success",
)

c.divider()

with c.row():
    with c.col(span=4):
        c.metric("Revenue", "$48,200", trend="+12%", trend_direction="up")
    with c.col(span=4):
        c.metric("Users", "1,024", trend="+89", trend_direction="up")
    with c.col(span=4):
        c.metric("Churn", "2.1%", trend="-0.3%", trend_direction="down")

c.spacer(size=2)

with c.card(title="Admin Notes"):
    c.text("This section contains sensitive information visible only after login.")
    c.text("Cacao handles the login form and session management automatically.", color="dimmed")
