"""Filter event handlers."""
import cacao as c

from components.sidebar import time_range, category, show_comparison, refresh_rate


@c.on("apply_filters")
async def handle_apply(session, event):
    tr = time_range.get(session)
    cat = category.get(session)
    cmp = show_comparison.get(session)
    print(f"Filters applied: range={tr}, category={cat}, compare={cmp}")


@c.on("reset_filters")
async def handle_reset(session, event):
    time_range.set(session, "30d")
    category.set(session, "All")
    show_comparison.set(session, False)
    refresh_rate.set(session, 30)
