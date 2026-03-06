# Sales Dashboard — showcase demo
import cacao as c

c.config(title="Sales Dashboard", theme="dark", branding=True)

sales = c.sample_sales_data()

c.title("Sales Dashboard")
c.text("Real-time sales analytics", color="muted")
c.spacer()

with c.row():
    c.metric("Revenue", "$45,231", trend="+20.1%", trend_direction="up")
    c.metric("Orders", "1,247", trend="+12.5%", trend_direction="up")
    c.metric("Customers", "842", trend="+5.3%", trend_direction="up")
    c.metric("Avg Order", "$36.25", trend="-2.1%", trend_direction="down")

c.spacer()

with c.row():
    with c.col(span=8):
        with c.card("Revenue Trend"):
            c.line(sales, x="date", y="revenue", area=True)

    with c.col(span=4):
        with c.card("Sales by Category"):
            c.pie(sales[:5], values="revenue", names="category", donut=True)

c.spacer()

with c.card("Recent Transactions"):
    c.table(sales[:10], columns=["date", "category", "revenue", "orders"])
