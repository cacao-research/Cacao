"""Overview page - KPIs, charts, gauges."""
import cacao as c

from data import (
    time_series, category_data,
    total_revenue, total_users, total_orders, avg_conversion,
)

with c.page("/"):
    c.title("Analytics Dashboard")
    c.text("Real-time business intelligence powered by Cacao", color="muted")
    c.spacer(4)

    # KPI row
    with c.row(gap=4):
        c.metric("Revenue", f"${total_revenue / 1000:.1f}K", trend="+23.5%", trend_direction="up")
        c.metric("Users", f"{total_users / 1000:.1f}K", trend="+18.2%", trend_direction="up")
        c.metric("Orders", f"{total_orders:,}", trend="+12.8%", trend_direction="up")
        c.metric("Conversion", f"{avg_conversion:.1f}%", trend="-2.1%", trend_direction="down")

    c.spacer(4)

    # Charts
    with c.row(gap=4):
        with c.col(span=8):
            with c.card("Revenue Trend"):
                c.line(time_series.to_dict(), x="date", y="revenue", smooth=True, area=True, height=350)
        with c.col(span=4):
            with c.card("Revenue by Category"):
                c.pie(category_data.to_dict(), values="revenue", names="category", donut=True, height=350)

    c.spacer(4)

    with c.row(gap=4):
        with c.col(span=6):
            with c.card("Users & Orders"):
                c.bar(time_series.limit(14).to_dict(), x="date", y=["users", "orders"], grouped=True, height=280)
        with c.col(span=6):
            with c.card("Conversion Rate"):
                c.line(time_series.limit(30).to_dict(), x="date", y="conversion", smooth=True, height=280)

    c.spacer(4)

    # Gauges
    with c.row(gap=4):
        with c.col(span=3):
            with c.card("Revenue Goal"):
                c.gauge(value=78, max_value=100, title="Monthly Target", format="{value}%")
        with c.col(span=3):
            with c.card("User Growth"):
                c.gauge(value=92, max_value=100, title="Growth Target", format="{value}%")
        with c.col(span=3):
            with c.card("NPS Score"):
                c.gauge(value=67, max_value=100, title="Customer Score")
        with c.col(span=3):
            with c.card("Uptime"):
                c.gauge(value=99.9, max_value=100, title="System Health", format="{value}%")
