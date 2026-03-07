"""
Notification System
===================
Demonstrates toast notifications and alert components.
Shows different variants, positions, and how to trigger
notifications from event handlers.
"""

import cacao as c

c.config(title="Notification System", theme="dark")

c.title("Notification System")
c.text("Explore different notification types and alert variants.")

c.spacer(size=2)

with c.card(title="Toast Notifications"):
    c.text(
        "Toasts are brief, auto-dismissing messages. Click a button to trigger one.",
        size="sm",
        color="gray",
    )
    c.spacer(size=1)
    with c.row():
        c.button("Success", variant="primary", on_click="toast_success")
        c.button("Error", variant="danger", on_click="toast_error")
        c.button("Warning", variant="secondary", on_click="toast_warning")
        c.button("Info", variant="ghost", on_click="toast_info")

c.spacer(size=2)

with c.card(title="Alert Components"):
    c.text(
        "Alerts are persistent inline messages for important information.",
        size="sm",
        color="gray",
    )
    c.spacer(size=1)
    c.alert(
        "Operation completed successfully! Your changes have been saved.",
        title="Success",
        variant="success",
    )
    c.alert(
        "Failed to connect to the database. Please check your configuration.",
        title="Error",
        variant="error",
    )
    c.alert(
        "Your subscription expires in 3 days. Renew to avoid interruption.",
        title="Warning",
        variant="warning",
    )
    c.alert(
        "A new version of the application is available. Refresh to update.",
        title="Info",
        variant="info",
    )

c.spacer(size=2)

with c.card(title="Notification Scenarios"):
    c.text("Simulate real-world notification patterns.", size="sm", color="gray")
    c.spacer(size=1)
    with c.row():
        c.button("Simulate Save", variant="primary", on_click="sim_save")
        c.button("Simulate Upload", variant="secondary", on_click="sim_upload")
        c.button("Simulate Delete", variant="danger", on_click="sim_delete")
        c.button("Simulate Validation", variant="ghost", on_click="sim_validate")

c.spacer(size=2)

notification_count = c.signal(0, name="notification_count")

with c.card(title="Notification Counter"):
    c.metric("Notifications Sent", signal="notification_count")


@c.on("toast_success")
async def toast_success(session, event):
    c.toast("This is a success notification!", variant="success")
    notification_count.set(notification_count.value + 1)


@c.on("toast_error")
async def toast_error(session, event):
    c.toast("This is an error notification!", variant="error")
    notification_count.set(notification_count.value + 1)


@c.on("toast_warning")
async def toast_warning(session, event):
    c.toast("This is a warning notification!", variant="warning")
    notification_count.set(notification_count.value + 1)


@c.on("toast_info")
async def toast_info(session, event):
    c.toast("This is an informational notification!", variant="info")
    notification_count.set(notification_count.value + 1)


@c.on("sim_save")
async def sim_save(session, event):
    c.toast("Document saved successfully.", variant="success")
    notification_count.set(notification_count.value + 1)


@c.on("sim_upload")
async def sim_upload(session, event):
    c.toast("File uploaded. Processing may take a moment.", variant="info")
    notification_count.set(notification_count.value + 1)


@c.on("sim_delete")
async def sim_delete(session, event):
    c.toast("Item deleted. This action cannot be undone.", variant="warning")
    notification_count.set(notification_count.value + 1)


@c.on("sim_validate")
async def sim_validate(session, event):
    c.toast("Validation failed: email field is required.", variant="error")
    notification_count.set(notification_count.value + 1)
