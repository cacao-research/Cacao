"""
Settings Panel
==============
Demonstrates a settings page with switches, selects, sliders,
and save/reset functionality. Shows how to build a typical
preferences interface with grouped options.
"""

import cacao as c

c.config(title="Settings Panel", theme="dark")

# Define settings signals with defaults
dark_mode = c.signal(True, name="dark_mode")
notifications = c.signal(True, name="notifications")
email_digest = c.signal(False, name="email_digest")
language = c.signal("English", name="language")
font_size = c.signal(14, name="font_size")
auto_save = c.signal(True, name="auto_save")
timezone = c.signal("UTC", name="timezone")

c.title("Settings")
c.text("Manage your application preferences.", color="gray")

c.spacer(size=2)

with c.tabs(default="general"):
    with c.tab("general", label="General"):
        with c.card(title="Appearance"):
            c.switch(label="Dark mode", signal="dark_mode")
            c.slider(
                label="Font size (px)",
                signal="font_size",
                min=10,
                max=24,
                step=1,
            )
            c.select(
                label="Language",
                options=["English", "Spanish", "French", "German", "Japanese"],
                signal="language",
            )
            c.select(
                label="Timezone",
                options=["UTC", "US/Eastern", "US/Pacific", "Europe/London", "Asia/Tokyo"],
                signal="timezone",
            )

        with c.card(title="Editor"):
            c.switch(label="Auto-save documents", signal="auto_save")
            c.select(
                label="Tab size",
                options=["2 spaces", "4 spaces", "Tab"],
                signal="tab_size",
            )

    with c.tab("notifications", label="Notifications"):
        with c.card(title="Notification Preferences"):
            c.switch(label="Enable notifications", signal="notifications")
            c.switch(label="Daily email digest", signal="email_digest")
            c.select(
                label="Notification sound",
                options=["Default", "Chime", "Bell", "None"],
                signal="notif_sound",
            )
            c.slider(
                label="Quiet hours start",
                signal="quiet_start",
                min=0,
                max=23,
                step=1,
            )
            c.slider(
                label="Quiet hours end",
                signal="quiet_end",
                min=0,
                max=23,
                step=1,
            )

    with c.tab("privacy", label="Privacy"):
        with c.card(title="Data & Privacy"):
            c.switch(label="Share usage analytics", signal="analytics")
            c.switch(label="Show online status", signal="online_status")
            c.switch(label="Allow search engines to index profile", signal="indexable")
            c.spacer(size=2)
            c.button("Download My Data", variant="secondary", on_click="download_data")
            c.button("Delete Account", variant="danger", on_click="delete_account")

c.spacer(size=2)

with c.row():
    c.button("Save Settings", variant="primary", on_click="save_settings")
    c.button("Reset to Defaults", variant="ghost", on_click="reset_settings")


@c.on("save_settings")
async def save_settings(session, event):
    c.toast("Settings saved successfully!", variant="success")


@c.on("reset_settings")
async def reset_settings(session, event):
    dark_mode.set(True)
    notifications.set(True)
    email_digest.set(False)
    language.set("English")
    font_size.set(14)
    auto_save.set(True)
    timezone.set("UTC")
    c.toast("Settings reset to defaults.", variant="info")


@c.on("download_data")
async def download_data(session, event):
    c.toast("Preparing data export... You will be notified when ready.", variant="info")


@c.on("delete_account")
async def delete_account(session, event):
    c.toast("This action requires confirmation. Please contact support.", variant="warning")
