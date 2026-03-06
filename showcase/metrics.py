# KPI Metrics — showcase demo
import cacao as c

c.config(title="Company Metrics", theme="dark", branding=True)

c.title("Company Metrics")
c.text("Q4 2025 Performance Overview", color="muted")
c.spacer()

with c.row():
    c.metric("Revenue", "$2.4M", trend="+12.5%", trend_direction="up")
    c.metric("Users", "48,293", trend="+8.2%", trend_direction="up")
    c.metric("Orders", "12,847", trend="+23.1%", trend_direction="up")
    c.metric("Churn", "2.3%", trend="-0.4%", trend_direction="down")

c.spacer()

with c.row():
    with c.col(span=6):
        with c.card("Team Performance"):
            c.metric("Tickets Resolved", "1,842", trend="+15%", trend_direction="up")
            c.progress(78, label="Sprint Progress")
            c.progress(92, label="Test Coverage")
            c.progress(65, label="Documentation")

    with c.col(span=6):
        with c.card("System Health"):
            c.metric("Uptime", "99.97%", trend="+0.02%", trend_direction="up")
            c.alert("All systems operational", variant="success")
            c.alert("Scheduled maintenance: Mar 15", variant="info")
