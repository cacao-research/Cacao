# Analytics Dashboard - showcase demo
import cacao as c

c.config(title="Analytics", theme="dark", branding=True)

sales = c.sample_sales_data()

c.title("Analytics Dashboard")
c.text("Multi-chart analytics with real-time data visualization", color="muted")
c.spacer()

# --- Top metrics row ---
with c.row():
    c.metric("Total Revenue", "$2.4M", trend="+18.2%", trend_direction="up")
    c.metric("Conversion", "3.24%", trend="+0.8%", trend_direction="up")
    c.metric("Avg Session", "4m 32s", trend="+12%", trend_direction="up")
    c.metric("Bounce Rate", "32.1%", trend="-4.2%", trend_direction="down")

c.spacer()

# --- Main charts ---
with c.row():
    with c.col(span=8):
        with c.card("Revenue Over Time"):
            c.area(sales, x="date", y="revenue")

    with c.col(span=4):
        with c.card("Revenue by Category"):
            c.pie(sales[:6], values="revenue", names="category", donut=True)

c.spacer()

with c.row():
    with c.col(span=6):
        with c.card("Orders by Category"):
            c.bar(sales[:8], x="category", y="orders")

    with c.col(span=6):
        with c.card("Revenue vs Orders"):
            c.scatter(sales, x="orders", y="revenue")

c.spacer()

# --- Detailed breakdown ---
with c.row():
    with c.col(span=4):
        with c.card("Growth Targets"):
            c.progress(87, label="Q1 Revenue Target")
            c.progress(92, label="User Acquisition")
            c.progress(73, label="Market Expansion")
            c.progress(95, label="Customer Retention")

    with c.col(span=4):
        with c.card("Regional Performance"):
            c.metric("North America", "$980K", trend="+15%", trend_direction="up")
            c.divider()
            c.metric("Europe", "$720K", trend="+22%", trend_direction="up")
            c.divider()
            c.metric("Asia Pacific", "$540K", trend="+31%", trend_direction="up")

    with c.col(span=4):
        with c.card("System Status"):
            c.alert("All services operational", variant="success")
            c.alert("CDN cache hit rate: 98.7%", variant="info")
            c.alert("Database replica lag: 2ms", variant="info")
            c.spacer(size=2)
            c.metric("Uptime", "99.99%")

c.spacer()

# --- Full data table ---
with c.card("Transaction Log"):
    c.table(sales, columns=["date", "category", "revenue", "orders"])
