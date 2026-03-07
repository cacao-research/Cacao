"""Sales Dashboard - charts, tables, sidebar filters, multi-page."""
import cacao as c

c.config(title="Sales Dashboard", theme="dark")

# Signals
category_filter = c.signal("All", name="category")
date_range = c.signal("last_30_days", name="date_range")

# Sample data
sales = c.sample_sales_data(100)
users = c.sample_users_data(50)

total_revenue = sales.sum("revenue")
total_orders = sales.sum("orders")
total_profit = sales.sum("profit")
avg_order = total_revenue / total_orders if total_orders else 0


# --- Page: Overview ---
with c.page("/"):
    c.title("Sales Dashboard")
    c.text("Real-time analytics powered by Cacao", color="muted")

    with c.row(gap=4):
        c.metric("Revenue", f"${total_revenue:,.0f}", trend="+12.5%", trend_direction="up")
        c.metric("Orders", f"{total_orders:,}", trend="+8.2%", trend_direction="up")
        c.metric("Profit", f"${total_profit:,.0f}", trend="+15.3%", trend_direction="up")
        c.metric("Avg Order", f"${avg_order:,.2f}", trend="-2.1%", trend_direction="down")

    c.spacer()

    with c.row(gap=4):
        with c.col(span=8):
            with c.card("Revenue Over Time"):
                c.line(sales.to_dict(), x="date", y="revenue", smooth=True, area=True, height=300)
        with c.col(span=4):
            with c.card("By Category"):
                c.pie(sales.to_dict(), values="revenue", names="category", donut=True, height=300)

    c.spacer()

    with c.card("Recent Transactions"):
        c.table(
            sales.limit(20).to_dict(),
            columns=["date", "category", "orders", "revenue", "profit"],
            searchable=True,
            paginate=True,
            page_size=10,
        )


# --- Page: Users ---
with c.page("/users"):
    c.title("User Management")

    with c.row(gap=4):
        c.metric("Total Users", len(users))
        c.metric("Active", len(users.filter(lambda r: r["status"] == "Active")))
        c.metric("Pending", len(users.filter(lambda r: r["status"] == "Pending")))

    with c.card("All Users"):
        c.table(
            users.to_dict(),
            columns=["id", "name", "email", "role", "status", "created"],
            searchable=True,
            sortable=True,
            paginate=True,
        )


# --- Sidebar ---
with c.sidebar():
    c.title("Filters", level=3)
    c.select("Category", ["All", "Electronics", "Clothing", "Food", "Books", "Home"], signal=category_filter)
    c.select("Date Range", [
        {"label": "Last 7 Days", "value": "last_7_days"},
        {"label": "Last 30 Days", "value": "last_30_days"},
        {"label": "Last 90 Days", "value": "last_90_days"},
    ], signal=date_range)
    c.button("Apply Filters", variant="primary", on_click="apply_filters")
    c.button("Reset", variant="ghost", on_click="reset_filters")


# --- Handlers ---
@c.on("apply_filters")
async def apply_filters(session, event):
    cat = category_filter.get(session)
    dr = date_range.get(session)
    print(f"Filters: category={cat}, date_range={dr}")


@c.on("reset_filters")
async def reset_filters(session, event):
    category_filter.set(session, "All")
    date_range.set(session, "last_30_days")
