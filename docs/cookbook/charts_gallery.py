"""
Charts Gallery Recipe
=====================
Showcases every chart type available in Cacao: line, bar,
pie, area, scatter, and gauge -- all with sample data.

Run: cacao run docs/cookbook/charts_gallery.py
"""

import cacao as c

c.config(title="Charts Gallery", theme="dark")

c.title("Charts Gallery", level=1)
c.text("A showcase of all available chart types in Cacao.", color="dimmed")
c.divider()

monthly_sales = [
    {"month": "Jan", "revenue": 4200, "cost": 2800},
    {"month": "Feb", "revenue": 5100, "cost": 3100},
    {"month": "Mar", "revenue": 4800, "cost": 2900},
    {"month": "Apr", "revenue": 6200, "cost": 3400},
    {"month": "May", "revenue": 7100, "cost": 3800},
    {"month": "Jun", "revenue": 6800, "cost": 3600},
]

categories = [
    {"name": "Electronics", "value": 42},
    {"name": "Clothing", "value": 28},
    {"name": "Books", "value": 15},
    {"name": "Food", "value": 10},
    {"name": "Other", "value": 5},
]

scatter_data = [
    {"x": 10, "y": 25}, {"x": 20, "y": 40}, {"x": 30, "y": 35},
    {"x": 40, "y": 55}, {"x": 50, "y": 48}, {"x": 60, "y": 72},
    {"x": 70, "y": 65}, {"x": 80, "y": 80}, {"x": 90, "y": 78},
]

# Row 1: Line and Bar
with c.row():
    with c.col(span=6):
        with c.card(title="Line Chart - Monthly Revenue"):
            c.line(monthly_sales, x="month", y="revenue")
    with c.col(span=6):
        with c.card(title="Bar Chart - Revenue vs Cost"):
            c.bar(monthly_sales, x="month", y="revenue")

c.spacer(size=2)

# Row 2: Pie and Scatter
with c.row():
    with c.col(span=6):
        with c.card(title="Pie Chart - Sales by Category"):
            c.pie(categories, values="value", names="name")
    with c.col(span=6):
        with c.card(title="Scatter Plot - Correlation"):
            c.line(scatter_data, x="x", y="y")

c.spacer(size=2)

# Row 3: Additional visualizations
with c.row():
    with c.col(span=6):
        with c.card(title="Progress Gauges"):
            c.progress(75, label="CPU Usage")
            c.spacer(size=1)
            c.progress(42, label="Memory Usage")
            c.spacer(size=1)
            c.progress(91, label="Disk Usage")
    with c.col(span=6):
        with c.card(title="Data Summary"):
            total_rev = sum(d["revenue"] for d in monthly_sales)
            total_cost = sum(d["cost"] for d in monthly_sales)
            c.metric("Total Revenue", f"${total_rev:,}")
            c.metric("Total Cost", f"${total_cost:,}")
            c.metric("Profit Margin", f"{round((total_rev - total_cost) / total_rev * 100)}%",
                      trend="healthy", trend_direction="up")
