"""Sidebar filters shared across all pages."""
import cacao as c

# Signals used by sidebar controls
time_range = c.signal("30d", name="time_range")
category = c.signal("All", name="category")
show_comparison = c.signal(False, name="show_comparison")
refresh_rate = c.signal(30, name="refresh_rate")


def render_sidebar() -> None:
    with c.sidebar():
        c.title("Filters", level=3)
        c.divider()

        c.select("Time Range", [
            {"label": "Last 7 days", "value": "7d"},
            {"label": "Last 30 days", "value": "30d"},
            {"label": "Last 90 days", "value": "90d"},
            {"label": "This year", "value": "1y"},
        ], signal=time_range)

        c.spacer(2)
        c.select("Category", [
            "All", "Electronics", "Clothing", "Food", "Books", "Home & Garden",
        ], signal=category)

        c.spacer(2)
        c.checkbox("Compare to previous period", signal=show_comparison,
                    description="Show year-over-year comparison")

        c.divider()
        c.title("Settings", level=4)
        c.slider("Refresh Rate (s)", signal=refresh_rate, min_value=5, max_value=120, step=5)

        c.spacer(4)
        c.button("Apply Filters", variant="primary", on_click="apply_filters")
        c.spacer(2)
        c.button("Reset", variant="ghost", on_click="reset_filters")
