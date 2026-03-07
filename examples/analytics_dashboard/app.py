"""Analytics Dashboard - structured multi-file example.

Demonstrates the recommended project structure for larger Cacao apps:
  pages/       One file per page
  components/  Reusable UI blocks
  handlers/    Event handlers
  data/        Data generation / loading

Run with: cacao run examples/analytics_dashboard/app.py
"""
import cacao as c

c.config(title="Analytics Dashboard", theme="dark")

# Import pages (self-registering via c.page)
from pages import overview, analytics, monitor  # noqa: E402, F401

# Import handlers (self-registering via @c.on)
from handlers import filters  # noqa: E402, F401

# Import sidebar component (used on all pages)
from components.sidebar import render_sidebar  # noqa: E402

render_sidebar()
