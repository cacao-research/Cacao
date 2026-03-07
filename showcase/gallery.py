# Component Gallery - showcase demo
import cacao as c

c.config(title="Component Gallery", theme="dark", branding=True)

c.title("Component Gallery")
c.text("Every component Cacao offers, in one page", color="muted")
c.spacer()

# --- Metrics & KPIs ---
with c.card("Metrics & KPIs"):
    with c.row():
        c.metric("Revenue", "$128K", trend="+18.2%", trend_direction="up")
        c.metric("Users", "12,493", trend="+7.4%", trend_direction="up")
        c.metric("Latency", "42ms", trend="-12%", trend_direction="down")
        c.metric("Errors", "0.02%", trend="-0.01%", trend_direction="down")

c.spacer()

# --- Progress & Badges ---
with c.row():
    with c.col(span=6):
        with c.card("Progress Bars"):
            c.progress(92, label="Build Pipeline")
            c.progress(67, label="Test Coverage")
            c.progress(45, label="Migration Progress")
            c.progress(100, label="Deployment")

    with c.col(span=6):
        with c.card("Alerts & Badges"):
            c.alert("Deployment successful", variant="success")
            c.alert("New version available: v2.4.0", variant="info")
            c.alert("High memory usage detected", variant="warning")
            c.alert("Service unreachable", variant="error")

c.spacer()

# --- Charts ---
sales = c.sample_sales_data()

with c.row():
    with c.col(span=6):
        with c.card("Line Chart"):
            c.line(sales, x="date", y="revenue")

    with c.col(span=6):
        with c.card("Bar Chart"):
            c.bar(sales[:8], x="category", y="orders")

c.spacer()

with c.row():
    with c.col(span=4):
        with c.card("Pie Chart"):
            c.pie(sales[:5], values="revenue", names="category", donut=True)

    with c.col(span=4):
        with c.card("Area Chart"):
            c.area(sales, x="date", y="revenue")

    with c.col(span=4):
        with c.card("Scatter Plot"):
            c.scatter(sales, x="orders", y="revenue")

c.spacer()

# --- Data Display ---
with c.card("Data Table"):
    c.table(sales[:8], columns=["date", "category", "revenue", "orders"])

c.spacer()

# --- Code Block ---
with c.card("Code Display"):
    c.code("""import cacao as c

c.config(title="My App", theme="dark")

with c.row():
    c.metric("Users", "1,247")
    c.metric("Revenue", "$45K")

with c.card("Sales Trend"):
    c.line(data, x="date", y="revenue", area=True)
""", language="python")

c.spacer()

# --- Steps ---
with c.card("Steps Component"):
    with c.steps(current=2):
        c.step("Install", description="pip install cacao")
        c.step("Build", description="Write your Python app")
        c.step("Deploy", description="cacao build app.py")
        c.step("Ship", description="Push to GitHub Pages")

c.spacer()

# --- Timeline ---
with c.card("Timeline"):
    with c.timeline():
        c.timeline_item("Project Started", description="Initial commit and repo setup", color="blue")
        c.timeline_item("v1.0 Released", description="First stable release with core components", color="green")
        c.timeline_item("Static Builds", description="Added serverless deployment support", color="purple")
        c.timeline_item("v2.0 Launch", description="Complete UI overhaul with 50+ components", color="gold")

c.spacer()

# --- Accordion ---
with c.card("Accordion"):
    with c.accordion():
        with c.accordion_item("What is Cacao?"):
            c.text("Cacao is a reactive Python web framework for building dashboards and tools.")
        with c.accordion_item("Do I need JavaScript?"):
            c.text("No. Write pure Python and Cacao handles the frontend automatically.")
        with c.accordion_item("Can I deploy statically?"):
            c.text("Yes! Use `cacao build` to generate a static site for GitHub Pages or any CDN.")

c.spacer()

# --- Layout showcase ---
with c.card("Nested Layouts"):
    with c.row():
        with c.col(span=4):
            c.metric("CPU", "23%")
            c.progress(23, label="Usage")
        with c.col(span=4):
            c.metric("Memory", "61%")
            c.progress(61, label="Usage")
        with c.col(span=4):
            c.metric("Disk", "45%")
            c.progress(45, label="Usage")
