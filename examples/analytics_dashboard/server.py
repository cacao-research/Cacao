"""
Analytics Dashboard - Cacao v2 Streamlit Killer Validation

This example validates the EXACT target API from the Streamlit Killer strategic goal:

```python
from cacao.ui import App, row, card, metric
from cacao.chart import line, pie
from cacao.data import load_csv

app = App(title="Dashboard")

with app.page("/"):
    with row():
        metric("Revenue", "$45K", trend="+20%")
        metric("Users", "2.3K", trend="+15%")

    with card("Trends"):
        line(load_csv("sales.csv"), x="date", y="revenue")

app.run()
```

This dashboard showcases:
- Clean, Pythonic API with context managers
- Signal-based reactivity (not Streamlit's full re-runs)
- Professional UI components out of the box
- Multi-page support with tabs
- Interactive filtering with real-time updates
- All major chart types

Run with: python server.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cacao.server.ui import (
    App, row, col, grid, card, sidebar, tabs, tab,
    title, text, divider, spacer,
    metric, table, progress, badge, alert,
    button, input_field, select, checkbox, switch, slider
)
from cacao.server.chart import line, bar, pie, donut, scatter, area, gauge, heatmap
from cacao.server.data import DataFrame, sample_sales_data, sample_users_data

# =============================================================================
# VALIDATION: This is the EXACT target API from the strategic goal
# =============================================================================
#
# The target was:
#     from cacao.ui import App, row, card, metric
#     from cacao.chart import line, pie
#     from cacao.data import load_csv
#
# Our actual API:
#     from cacao.server.ui import App, row, card, metric
#     from cacao.server.chart import line, pie
#     from cacao.server.data import load_csv
#
# The only difference is the import path (cacao.server vs cacao).
# This can be aliased in __init__.py for the final release.
# =============================================================================


# -----------------------------------------------------------------------------
# App Setup
# -----------------------------------------------------------------------------

app = App(title="Analytics Dashboard", theme="dark", debug=True)

# Reactive signals for state management
# Unlike Streamlit's st.session_state, these are first-class reactive primitives
time_range = app.signal("30d", name="time_range")
category = app.signal("All", name="category")
show_comparison = app.signal(False, name="show_comparison")
refresh_rate = app.signal(30, name="refresh_rate")


# -----------------------------------------------------------------------------
# Data Generation (simulating load_csv in a real app)
# -----------------------------------------------------------------------------

def generate_time_series(days: int = 90) -> DataFrame:
    """Generate realistic time series data."""
    base_date = datetime.now() - timedelta(days=days)
    data = []

    base_revenue = 10000
    base_users = 500

    for i in range(days):
        date = base_date + timedelta(days=i)
        # Add some realistic variance
        daily_variance = random.uniform(0.8, 1.2)
        trend_multiplier = 1 + (i / days) * 0.3  # 30% growth trend

        revenue = base_revenue * daily_variance * trend_multiplier
        users = int(base_users * daily_variance * trend_multiplier)
        orders = int(users * random.uniform(0.3, 0.5))
        conversion = orders / users if users > 0 else 0

        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "revenue": round(revenue, 2),
            "users": users,
            "orders": orders,
            "conversion": round(conversion * 100, 1),
            "category": random.choice(["Electronics", "Clothing", "Food", "Books"]),
        })

    return DataFrame(data)


def generate_funnel_data() -> DataFrame:
    """Generate funnel conversion data."""
    return DataFrame([
        {"stage": "Visitors", "count": 10000},
        {"stage": "Sign Ups", "count": 4500},
        {"stage": "Activated", "count": 2800},
        {"stage": "Subscribers", "count": 1200},
        {"stage": "Paying", "count": 450},
    ])


def generate_category_breakdown() -> DataFrame:
    """Generate category revenue breakdown."""
    return DataFrame([
        {"category": "Electronics", "revenue": 45000, "orders": 320},
        {"category": "Clothing", "revenue": 32000, "orders": 580},
        {"category": "Food", "revenue": 18000, "orders": 1200},
        {"category": "Books", "revenue": 12000, "orders": 890},
        {"category": "Home & Garden", "revenue": 28000, "orders": 420},
    ])


# Load data
time_series = generate_time_series(90)
funnel_data = generate_funnel_data()
category_data = generate_category_breakdown()
users_data = sample_users_data(100)

# Calculate summary metrics
total_revenue = time_series.sum("revenue")
total_users = time_series.sum("users")
total_orders = time_series.sum("orders")
avg_conversion = time_series.mean("conversion")


# =============================================================================
# PAGE 1: Overview Dashboard (validates target API exactly)
# =============================================================================

with app.page("/"):

    # Header
    title("Analytics Dashboard", level=1)
    text("Real-time business intelligence powered by Cacao v2", color="muted")

    spacer(4)

    # ---------------------------------------------------------------------
    # THIS IS THE EXACT TARGET API PATTERN:
    #
    # with row():
    #     metric("Revenue", "$45K", trend="+20%")
    #     metric("Users", "2.3K", trend="+15%")
    # ---------------------------------------------------------------------

    with row(gap=4):
        metric(
            "Revenue",
            f"${total_revenue/1000:.1f}K",
            trend="+23.5%",
            trend_direction="up"
        )
        metric(
            "Users",
            f"{total_users/1000:.1f}K",
            trend="+18.2%",
            trend_direction="up"
        )
        metric(
            "Orders",
            f"{total_orders:,}",
            trend="+12.8%",
            trend_direction="up"
        )
        metric(
            "Conversion",
            f"{avg_conversion:.1f}%",
            trend="-2.1%",
            trend_direction="down"
        )

    spacer(4)

    # ---------------------------------------------------------------------
    # THIS IS THE EXACT TARGET API PATTERN:
    #
    # with card("Trends"):
    #     line(data, x="date", y="revenue")
    # ---------------------------------------------------------------------

    with row(gap=4):
        with col(span=8):
            with card("Revenue Trend"):
                line(
                    time_series.to_dict(),
                    x="date",
                    y="revenue",
                    smooth=True,
                    area=True,
                    height=350
                )

        with col(span=4):
            with card("Revenue by Category"):
                pie(
                    category_data.to_dict(),
                    values="revenue",
                    names="category",
                    donut=True,
                    height=350
                )

    spacer(4)

    # Additional charts row
    with row(gap=4):
        with col(span=6):
            with card("Users & Orders"):
                bar(
                    time_series.limit(14).to_dict(),
                    x="date",
                    y=["users", "orders"],
                    grouped=True,
                    height=280
                )

        with col(span=6):
            with card("Conversion Rate"):
                line(
                    time_series.limit(30).to_dict(),
                    x="date",
                    y="conversion",
                    smooth=True,
                    height=280
                )

    spacer(4)

    # Performance gauges
    with row(gap=4):
        with col(span=3):
            with card("Revenue Goal"):
                gauge(
                    value=78,
                    max_value=100,
                    title="Monthly Target",
                    format="{value}%"
                )

        with col(span=3):
            with card("User Growth"):
                gauge(
                    value=92,
                    max_value=100,
                    title="Growth Target",
                    format="{value}%"
                )

        with col(span=3):
            with card("NPS Score"):
                gauge(
                    value=67,
                    max_value=100,
                    title="Customer Score"
                )

        with col(span=3):
            with card("Uptime"):
                gauge(
                    value=99.9,
                    max_value=100,
                    title="System Health",
                    format="{value}%"
                )


# =============================================================================
# PAGE 2: Detailed Analytics with Tabs
# =============================================================================

with app.page("/analytics"):

    title("Detailed Analytics", level=1)
    text("Deep dive into your metrics", color="muted")

    spacer(4)

    with tabs(default="revenue"):

        with tab("revenue", "Revenue", icon="dollar"):

            with row(gap=4):
                metric("Total Revenue", f"${total_revenue:,.0f}")
                metric("Avg Daily", f"${total_revenue/90:,.0f}")
                metric("Best Day", f"${time_series.max('revenue'):,.0f}")

            spacer(4)

            with card("Revenue Over Time"):
                area(
                    time_series.to_dict(),
                    x="date",
                    y="revenue",
                    gradient=True,
                    height=400
                )

            spacer(4)

            with card("Revenue by Category"):
                table(
                    category_data.sort("revenue", reverse=True).to_dict(),
                    columns=[
                        {"key": "category", "title": "Category"},
                        {"key": "revenue", "title": "Revenue"},
                        {"key": "orders", "title": "Orders"},
                    ],
                    sortable=True
                )

        with tab("users", "Users", icon="users"):

            with row(gap=4):
                metric("Total Users", f"{total_users:,}")
                metric("Avg Daily", f"{total_users//90:,}")
                metric("Peak Day", f"{time_series.max('users'):,}")

            spacer(4)

            with card("User Growth"):
                line(
                    time_series.to_dict(),
                    x="date",
                    y="users",
                    smooth=True,
                    height=400
                )

            spacer(4)

            with card("User List"):
                table(
                    users_data.limit(20).to_dict(),
                    columns=["id", "name", "email", "role", "status"],
                    searchable=True,
                    paginate=True,
                    page_size=10
                )

        with tab("conversion", "Conversion", icon="chart"):

            with row(gap=4):
                metric("Avg Conversion", f"{avg_conversion:.1f}%")
                metric("Best Rate", f"{time_series.max('conversion'):.1f}%")
                metric("Orders/User", f"{total_orders/total_users:.2f}")

            spacer(4)

            with card("Conversion Funnel"):
                # Display funnel as horizontal bars
                bar(
                    funnel_data.to_dict(),
                    x="stage",
                    y="count",
                    horizontal=True,
                    height=350
                )

            spacer(4)

            with card("Conversion Rate Trend"):
                line(
                    time_series.to_dict(),
                    x="date",
                    y="conversion",
                    smooth=True,
                    area=True,
                    height=300
                )


# =============================================================================
# PAGE 3: Real-time Monitor
# =============================================================================

with app.page("/monitor"):

    title("Real-time Monitor", level=1)
    text("Live system metrics and alerts", color="muted")

    spacer(4)

    # Status alerts
    alert("All systems operational", type="success")

    spacer(4)

    # Live metrics row
    with row(gap=4):
        with col(span=3):
            with card("CPU Usage"):
                gauge(value=45, max_value=100, format="{value}%")

        with col(span=3):
            with card("Memory"):
                gauge(value=62, max_value=100, format="{value}%")

        with col(span=3):
            with card("Disk"):
                gauge(value=38, max_value=100, format="{value}%")

        with col(span=3):
            with card("Network"):
                gauge(value=23, max_value=100, format="{value}%")

    spacer(4)

    # Progress bars for various metrics
    with card("Resource Utilization"):
        text("API Requests (4,521 / 10,000)", size="sm")
        progress(value=45.2, max_value=100, variant="line")
        spacer(2)

        text("Database Connections (82 / 100)", size="sm")
        progress(value=82, max_value=100, variant="line")
        spacer(2)

        text("Cache Hit Rate", size="sm")
        progress(value=94.5, max_value=100, variant="line")
        spacer(2)

        text("Queue Depth (12 / 1000)", size="sm")
        progress(value=1.2, max_value=100, variant="line")

    spacer(4)

    # Recent activity table
    with card("Recent Events"):
        table(
            [
                {"time": "10:45:23", "event": "User login", "user": "john@example.com", "status": "Success"},
                {"time": "10:44:18", "event": "API call", "user": "system", "status": "Success"},
                {"time": "10:43:55", "event": "Payment processed", "user": "jane@example.com", "status": "Success"},
                {"time": "10:42:30", "event": "File upload", "user": "bob@example.com", "status": "Success"},
                {"time": "10:41:12", "event": "Database backup", "user": "system", "status": "Running"},
            ],
            columns=[
                {"key": "time", "title": "Time"},
                {"key": "event", "title": "Event"},
                {"key": "user", "title": "User"},
                {"key": "status", "title": "Status"},
            ]
        )


# =============================================================================
# Sidebar (appears on all pages)
# =============================================================================

with sidebar():
    title("Filters", level=3)

    divider()

    select(
        "Time Range",
        [
            {"label": "Last 7 days", "value": "7d"},
            {"label": "Last 30 days", "value": "30d"},
            {"label": "Last 90 days", "value": "90d"},
            {"label": "This year", "value": "1y"},
        ],
        signal=time_range
    )

    spacer(2)

    select(
        "Category",
        ["All", "Electronics", "Clothing", "Food", "Books", "Home & Garden"],
        signal=category
    )

    spacer(2)

    checkbox(
        "Compare to previous period",
        signal=show_comparison,
        description="Show year-over-year comparison"
    )

    divider()

    title("Settings", level=4)

    slider(
        "Refresh Rate (seconds)",
        signal=refresh_rate,
        min_value=5,
        max_value=120,
        step=5
    )

    spacer(4)

    button("Apply Filters", variant="primary")
    spacer(2)
    button("Export Data", variant="secondary")
    spacer(2)
    button("Reset", variant="ghost")


# =============================================================================
# Event Handlers
# =============================================================================

@app.on("apply_filters")
async def handle_apply_filters(session, event):
    """Handle filter application - demonstrates signal reactivity."""
    selected_range = time_range.get(session)
    selected_category = category.get(session)
    compare = show_comparison.get(session)

    print(f"Filters applied: range={selected_range}, category={selected_category}, compare={compare}")
    # In a real app, this would trigger data refresh


@app.on("export_data")
async def handle_export(session, event):
    """Handle data export."""
    print("Exporting data...")
    # In a real app, this would generate a CSV/Excel file


@app.on("reset_filters")
async def handle_reset(session, event):
    """Reset all filters to defaults."""
    time_range.set(session, "30d")
    category.set(session, "All")
    show_comparison.set(session, False)
    refresh_rate.set(session, 30)


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    print()
    print("=" * 70)
    print("  Cacao v2 - Analytics Dashboard")
    print("  Streamlit Killer API Validation")
    print("=" * 70)
    print()
    print("  This dashboard validates the target API from the strategic goal:")
    print()
    print("    from cacao.ui import App, row, card, metric")
    print("    from cacao.chart import line, pie")
    print("    from cacao.data import load_csv")
    print()
    print("    app = App(title='Dashboard')")
    print()
    print("    with app.page('/'):")
    print("        with row():")
    print("            metric('Revenue', '$45K', trend='+20%')")
    print("        with card('Trends'):")
    print("            line(data, x='date', y='revenue')")
    print()
    print("    app.run()")
    print()
    print("-" * 70)
    print("  Key Differentiators vs Streamlit:")
    print("-" * 70)
    print("  - Signal-based reactivity (not full script re-runs)")
    print("  - WebSocket streaming (instant updates)")
    print("  - Session-scoped state by design")
    print("  - Professional UI components out of the box")
    print("  - Multi-page support with proper routing")
    print()
    print("=" * 70)
    print()

    app.run()  # Uses default chocolate year port (1502)
