"""Monitor page - real-time system metrics."""
import cacao as c

with c.page("/monitor"):
    c.title("Real-time Monitor")
    c.text("Live system metrics and alerts", color="muted")
    c.spacer(4)

    c.alert("All systems operational", type="success")
    c.spacer(4)

    # Gauges
    with c.row(gap=4):
        with c.col(span=3):
            with c.card("CPU Usage"):
                c.gauge(value=45, max_value=100, format="{value}%")
        with c.col(span=3):
            with c.card("Memory"):
                c.gauge(value=62, max_value=100, format="{value}%")
        with c.col(span=3):
            with c.card("Disk"):
                c.gauge(value=38, max_value=100, format="{value}%")
        with c.col(span=3):
            with c.card("Network"):
                c.gauge(value=23, max_value=100, format="{value}%")

    c.spacer(4)

    # Resource utilization
    with c.card("Resource Utilization"):
        c.text("API Requests (4,521 / 10,000)", size="sm")
        c.progress(value=45.2, max_value=100, variant="line")
        c.spacer(2)
        c.text("Database Connections (82 / 100)", size="sm")
        c.progress(value=82, max_value=100, variant="line")
        c.spacer(2)
        c.text("Cache Hit Rate", size="sm")
        c.progress(value=94.5, max_value=100, variant="line")
        c.spacer(2)
        c.text("Queue Depth (12 / 1000)", size="sm")
        c.progress(value=1.2, max_value=100, variant="line")

    c.spacer(4)

    # Events table
    with c.card("Recent Events"):
        c.table([
            {"time": "10:45:23", "event": "User login", "user": "john@example.com", "status": "Success"},
            {"time": "10:44:18", "event": "API call", "user": "system", "status": "Success"},
            {"time": "10:43:55", "event": "Payment processed", "user": "jane@example.com", "status": "Success"},
            {"time": "10:42:30", "event": "File upload", "user": "bob@example.com", "status": "Success"},
            {"time": "10:41:12", "event": "Database backup", "user": "system", "status": "Running"},
        ], columns=[
            {"key": "time", "title": "Time"},
            {"key": "event", "title": "Event"},
            {"key": "user", "title": "User"},
            {"key": "status", "title": "Status"},
        ])
