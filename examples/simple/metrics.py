# KPI Dashboard in 10 lines
import cacao as c

c.config(title="KPI Dashboard", theme="dark")

c.title("Company Metrics")

with c.row():
    c.metric("Revenue", "$2.4M", trend="+12.5%", trend_direction="up")
    c.metric("Users", "48,293", trend="+8.2%", trend_direction="up")
    c.metric("Orders", "12,847", trend="+23.1%", trend_direction="up")
    c.metric("Churn", "2.3%", trend="-0.4%", trend_direction="down")
