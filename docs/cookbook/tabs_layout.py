"""
Tabs Layout Recipe
==================
Organizes different content sections into a tabbed interface.
Each tab contains distinct UI elements to show how tabs work
as a layout pattern.

Run: cacao run docs/cookbook/tabs_layout.py
"""

import cacao as c

c.config(title="Tabs Layout", theme="dark")

c.title("Project Dashboard", level=1)
c.text("Navigate between sections using the tabs below.", color="dimmed")
c.divider()

with c.tabs(default="overview"):
    with c.tab("overview", label="Overview"):
        with c.row():
            with c.col(span=3):
                c.metric("Tasks", "42", trend="+5 this week", trend_direction="up")
            with c.col(span=3):
                c.metric("Completed", "28", trend="67%", trend_direction="up")
            with c.col(span=3):
                c.metric("In Progress", "10")
            with c.col(span=3):
                c.metric("Blocked", "4", trend="+2", trend_direction="down")
        c.spacer(size=2)
        c.progress(67, label="Sprint Progress")
        c.alert("Sprint ends in 3 days. Stay focused!", variant="warning")

    with c.tab("team", label="Team"):
        team = [
            {"name": "Alice", "role": "Lead", "tasks": 8, "status": "active"},
            {"name": "Bob", "role": "Backend", "tasks": 12, "status": "active"},
            {"name": "Carol", "role": "Frontend", "tasks": 10, "status": "active"},
            {"name": "Dave", "role": "QA", "tasks": 6, "status": "away"},
        ]
        c.table(team, columns=[
            {"key": "name", "label": "Name"},
            {"key": "role", "label": "Role"},
            {"key": "tasks", "label": "Assigned Tasks"},
            {"key": "status", "label": "Status"},
        ])

    with c.tab("timeline", label="Timeline"):
        with c.timeline():
            c.timeline_item("Project Kickoff", description="Initial planning completed", status="complete")
            c.timeline_item("Design Phase", description="UI mockups and architecture", status="complete")
            c.timeline_item("Development", description="Core features in progress", status="active")
            c.timeline_item("Testing", description="QA and bug fixing", status="pending")
            c.timeline_item("Launch", description="Production deployment", status="pending")

    with c.tab("settings", label="Settings"):
        with c.card(title="Project Settings"):
            c.input("Project Name", signal="project_name", placeholder="My Project")
            c.select("Priority", options=["low", "medium", "high", "critical"], signal="priority")
            c.switch("Email Notifications", signal="notifications")
            c.switch("Auto-assign Tasks", signal="auto_assign")
            c.spacer(size=2)
            c.button("Save Settings", variant="primary", on_click="save_settings")

        @c.on("save_settings")
        async def handle_save(session, event):
            c.toast("Settings saved successfully!", variant="success")
