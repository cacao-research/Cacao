"""
Progress Tracker
================
Demonstrates a multi-step process using the steps component
and progress bars. Users advance through a simulated workflow
with visual feedback at each stage.
"""

import cacao as c

c.config(title="Progress Tracker", theme="dark")

current_step = c.signal(0, name="current_step")
overall_progress = c.signal(0, name="overall_progress")

step_labels = ["Upload Data", "Validate", "Process", "Review", "Complete"]

c.title("Data Processing Pipeline")
c.text("Track your data through each stage of the pipeline.")

c.spacer(size=2)

with c.steps():
    for label in step_labels:
        c.step(label)

c.spacer(size=2)

c.progress(signal="overall_progress", label="Overall Progress")

c.spacer(size=2)

with c.card(title="Current Step Details"):
    c.text("Step status and details will update as you advance.", signal="step_info")

    with c.row():
        c.button("Previous Step", variant="secondary", on_click="prev_step")
        c.button("Next Step", variant="primary", on_click="next_step")
        c.button("Reset", variant="danger", on_click="reset_steps")

c.spacer(size=2)

with c.card(title="Step Log"):
    c.table(
        signal="step_log",
        columns=["step", "status", "timestamp"],
    )


@c.on("next_step")
async def next_step(session, event):
    step = current_step.value
    if step < len(step_labels) - 1:
        new_step = step + 1
        current_step.set(new_step)
        overall_progress.set(int((new_step / (len(step_labels) - 1)) * 100))
        c.toast(f"Advanced to: {step_labels[new_step]}", variant="info")
    else:
        c.toast("Pipeline complete!", variant="success")


@c.on("prev_step")
async def prev_step(session, event):
    step = current_step.value
    if step > 0:
        new_step = step - 1
        current_step.set(new_step)
        overall_progress.set(int((new_step / (len(step_labels) - 1)) * 100))
        c.toast(f"Returned to: {step_labels[new_step]}", variant="warning")
    else:
        c.toast("Already at the first step.", variant="warning")


@c.on("reset_steps")
async def reset_steps(session, event):
    current_step.set(0)
    overall_progress.set(0)
    c.toast("Pipeline reset.", variant="info")
