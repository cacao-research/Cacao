"""
Dashboard Example - Cacao v2

A sales dashboard demonstrating the fluent UI builder API.
This showcases how easy it is to build professional dashboards
with Cacao - simpler than Streamlit but more powerful!

Run with: python server.py
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cacao_v2.server.ui import (
    App, row, col, card, sidebar, tabs, tab,
    title, text, metric, table, button, select, badge, alert, progress
)
from cacao_v2.server.chart import line, bar, pie
from cacao_v2.server.data import sample_sales_data, sample_users_data

# Create app
app = App(title="Sales Dashboard", theme="dark", debug=True)

# Create signals for interactive state
category_filter = app.signal("All", name="category")
date_range = app.signal("last_30_days", name="date_range")

# Load sample data
sales_data = sample_sales_data(100)
users_data = sample_users_data(50)

# Calculate summary stats
total_revenue = sales_data.sum("revenue")
total_orders = sales_data.sum("orders")
total_profit = sales_data.sum("profit")
avg_order_value = total_revenue / total_orders if total_orders else 0


# Define the dashboard layout
with app.page("/"):

    # Header
    title("Sales Dashboard", level=1)
    text("Real-time analytics powered by Cacao v2", size="lg", color="muted")

    # Alert for demo
    alert(
        "This is a demo dashboard with sample data",
        type="info",
        dismissible=True
    )

    # KPI Metrics Row
    with row(gap=4):
        metric(
            "Total Revenue",
            f"${total_revenue:,.0f}",
            trend="+12.5%",
            trend_direction="up"
        )
        metric(
            "Total Orders",
            f"{total_orders:,}",
            trend="+8.2%",
            trend_direction="up"
        )
        metric(
            "Total Profit",
            f"${total_profit:,.0f}",
            trend="+15.3%",
            trend_direction="up"
        )
        metric(
            "Avg Order Value",
            f"${avg_order_value:,.2f}",
            trend="-2.1%",
            trend_direction="down"
        )

    # Charts Row
    with row(gap=4):
        with col(span=8):
            with card("Revenue Over Time"):
                line(
                    sales_data.to_dict(),
                    x="date",
                    y="revenue",
                    smooth=True,
                    area=True,
                    height=300
                )

        with col(span=4):
            with card("Sales by Category"):
                pie(
                    sales_data.to_dict(),
                    values="revenue",
                    names="category",
                    donut=True,
                    height=300
                )

    # Second charts row
    with row(gap=4):
        with col(span=6):
            with card("Orders vs Profit"):
                bar(
                    sales_data.limit(10).to_dict(),
                    x="date",
                    y=["orders", "profit"],
                    grouped=True,
                    height=250
                )

        with col(span=6):
            with card("Daily Performance"):
                line(
                    sales_data.limit(14).to_dict(),
                    x="date",
                    y=["revenue", "profit"],
                    height=250
                )

    # Data Table
    with card("Recent Transactions"):
        table(
            sales_data.limit(20).to_dict(),
            columns=[
                {"key": "date", "title": "Date", "sortable": True},
                {"key": "category", "title": "Category", "sortable": True},
                {"key": "orders", "title": "Orders", "sortable": True},
                {"key": "revenue", "title": "Revenue", "sortable": True},
                {"key": "profit", "title": "Profit", "sortable": True},
            ],
            searchable=True,
            paginate=True,
            page_size=10
        )


# Users page
with app.page("/users"):

    title("User Management", level=1)

    with row(gap=4):
        metric("Total Users", len(users_data))
        metric("Active", len(users_data.filter(lambda r: r["status"] == "Active")))
        metric("Pending", len(users_data.filter(lambda r: r["status"] == "Pending")))

    with card("All Users"):
        table(
            users_data.to_dict(),
            columns=["id", "name", "email", "role", "status", "created"],
            searchable=True,
            sortable=True,
            paginate=True
        )


# Sidebar filters (appears on all pages)
with sidebar():
    title("Filters", level=3)

    select(
        "Category",
        ["All", "Electronics", "Clothing", "Food", "Books", "Home"],
        signal=category_filter
    )

    select(
        "Date Range",
        [
            {"label": "Last 7 Days", "value": "last_7_days"},
            {"label": "Last 30 Days", "value": "last_30_days"},
            {"label": "Last 90 Days", "value": "last_90_days"},
            {"label": "This Year", "value": "this_year"},
        ],
        signal=date_range
    )

    button("Apply Filters", variant="primary")
    button("Reset", variant="ghost")


# Event handlers
@app.on("apply_filters")
async def apply_filters(session, event):
    """Handle filter application."""
    category = category_filter.get(session)
    date = date_range.get(session)
    print(f"Applying filters: category={category}, date_range={date}")


@app.on("reset_filters")
async def reset_filters(session, event):
    """Reset all filters."""
    category_filter.set(session, "All")
    date_range.set(session, "last_30_days")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Cacao v2 - Sales Dashboard Demo")
    print("=" * 60)
    print("\nThis demonstrates the Streamlit-killer fluent UI API!")
    print("\nCompare this code to Streamlit and see how much cleaner it is,")
    print("while being 10x faster with true WebSocket reactivity.\n")
    print("Server starting on http://localhost:1634")
    print("=" * 60 + "\n")

    app.run(port=1634)
