"""Analytics page - detailed breakdowns with tabs."""
import cacao as c

from data import (
    time_series, category_data, funnel_data, users_data,
    total_revenue, total_users, total_orders, avg_conversion,
)

with c.page("/analytics"):
    c.title("Detailed Analytics")
    c.text("Deep dive into your metrics", color="muted")
    c.spacer(4)

    with c.tabs(default="revenue"):

        with c.tab("revenue", "Revenue", icon="dollar"):
            with c.row(gap=4):
                c.metric("Total Revenue", f"${total_revenue:,.0f}")
                c.metric("Avg Daily", f"${total_revenue / 90:,.0f}")
                c.metric("Best Day", f"${time_series.max('revenue'):,.0f}")
            c.spacer(4)
            with c.card("Revenue Over Time"):
                c.area(time_series.to_dict(), x="date", y="revenue", height=400)
            c.spacer(4)
            with c.card("Revenue by Category"):
                c.table(
                    category_data.sort("revenue", reverse=True).to_dict(),
                    columns=[
                        {"key": "category", "title": "Category"},
                        {"key": "revenue", "title": "Revenue"},
                        {"key": "orders", "title": "Orders"},
                    ],
                    sortable=True,
                )

        with c.tab("users", "Users", icon="users"):
            with c.row(gap=4):
                c.metric("Total Users", f"{total_users:,}")
                c.metric("Avg Daily", f"{total_users // 90:,}")
                c.metric("Peak Day", f"{time_series.max('users'):,}")
            c.spacer(4)
            with c.card("User Growth"):
                c.line(time_series.to_dict(), x="date", y="users", smooth=True, height=400)
            c.spacer(4)
            with c.card("User List"):
                c.table(
                    users_data.limit(20).to_dict(),
                    columns=["id", "name", "email", "role", "status"],
                    searchable=True,
                    paginate=True,
                    page_size=10,
                )

        with c.tab("conversion", "Conversion", icon="chart"):
            with c.row(gap=4):
                c.metric("Avg Conversion", f"{avg_conversion:.1f}%")
                c.metric("Best Rate", f"{time_series.max('conversion'):.1f}%")
                c.metric("Orders/User", f"{total_orders / total_users:.2f}")
            c.spacer(4)
            with c.card("Conversion Funnel"):
                c.bar(funnel_data.to_dict(), x="stage", y="count", horizontal=True, height=350)
            c.spacer(4)
            with c.card("Conversion Rate Trend"):
                c.line(time_series.to_dict(), x="date", y="conversion", smooth=True, area=True, height=300)
