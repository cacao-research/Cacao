"""
Sales Dashboard - Metrics, Charts, and Tables
===============================================
A realistic dashboard with KPI metrics, line/bar/pie charts, and a data table.
Run with: cacao run dashboard.py
"""

import cacao as c

c.config(title="Sales Dashboard", theme="dark")

sales = c.sample_sales_data()

c.title("Sales Dashboard")
c.text("Q1 2026 Performance Overview", size="lg", color="dimmed")

c.spacer(size=2)

# --- KPI Row ---
with c.row():
    with c.col(span=3):
        c.metric("Revenue", "$142,800", trend="+18.2%", trend_direction="up")
    with c.col(span=3):
        c.metric("Orders", "1,847", trend="+124", trend_direction="up")
    with c.col(span=3):
        c.metric("Avg Order", "$77.30", trend="+$4.10", trend_direction="up")
    with c.col(span=3):
        c.metric("Returns", "32", trend="-8", trend_direction="down")

c.divider()

# --- Charts Row ---
with c.row():
    with c.col(span=8):
        with c.card(title="Monthly Revenue"):
            c.line(
                [
                    {"month": "Jan", "revenue": 38200},
                    {"month": "Feb", "revenue": 45100},
                    {"month": "Mar", "revenue": 59500},
                ],
                x="month",
                y="revenue",
            )
    with c.col(span=4):
        with c.card(title="Sales by Category"):
            c.pie(
                [
                    {"category": "Electronics", "sales": 52000},
                    {"category": "Clothing", "sales": 38400},
                    {"category": "Home", "sales": 29800},
                    {"category": "Sports", "sales": 22600},
                ],
                values="sales",
                names="category",
            )

c.spacer(size=2)

# --- Bar Chart + Table ---
with c.row():
    with c.col(span=6):
        with c.card(title="Top Products"):
            c.bar(
                [
                    {"product": "Laptop Pro", "units": 312},
                    {"product": "Wireless Earbuds", "units": 287},
                    {"product": "Smart Watch", "units": 245},
                    {"product": "USB-C Hub", "units": 198},
                    {"product": "Keyboard", "units": 176},
                ],
                x="product",
                y="units",
            )
    with c.col(span=6):
        with c.card(title="Recent Orders"):
            c.table(
                sales,
                columns=[
                    {"key": "date", "label": "Date"},
                    {"key": "product", "label": "Product"},
                    {"key": "amount", "label": "Amount"},
                    {"key": "status", "label": "Status"},
                ],
            )
