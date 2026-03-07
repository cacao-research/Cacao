"""
Cookbook Index — Browse all Cacao recipes in one app.

Run with: cacao run docs/cookbook_index.py
"""
import cacao as c

c.config(title="Cacao Cookbook", theme="dark")

RECIPES = [
    # Getting Started
    {"name": "Hello World", "file": "hello_world.py", "category": "Getting Started",
     "description": "Absolute minimal Cacao app — title, text, metrics."},
    {"name": "Counter", "file": "counter.py", "category": "Getting Started",
     "description": "Interactive counter with signals and event handlers."},
    {"name": "Todo App", "file": "todo_app.py", "category": "Getting Started",
     "description": "Classic todo list with add, remove, and toggle."},

    # Layout & Navigation
    {"name": "Multi-Page App", "file": "multi_page.py", "category": "Layout",
     "description": "Multi-page app with hash-based routing."},
    {"name": "Sidebar Layout", "file": "sidebar_layout.py", "category": "Layout",
     "description": "App using the sidebar layout preset."},
    {"name": "Tabs Layout", "file": "tabs_layout.py", "category": "Layout",
     "description": "Tabbed interface for organizing content."},

    # Data & Charts
    {"name": "Dashboard", "file": "dashboard.py", "category": "Data",
     "description": "Sales dashboard with metrics, charts, and tables."},
    {"name": "Data Table", "file": "data_table.py", "category": "Data",
     "description": "Interactive data table with sample data."},
    {"name": "Charts Gallery", "file": "charts_gallery.py", "category": "Data",
     "description": "All chart types: line, bar, pie, area, scatter, gauge."},
    {"name": "JSON Viewer", "file": "json_viewer.py", "category": "Data",
     "description": "Explore JSON data with collapsible tree view."},

    # Forms & Input
    {"name": "Form Handling", "file": "form_handling.py", "category": "Forms",
     "description": "Form with validation, various input types, and submit."},
    {"name": "Settings Panel", "file": "settings_panel.py", "category": "Forms",
     "description": "Settings page with switches, selects, and save."},
    {"name": "Markdown Editor", "file": "markdown_editor.py", "category": "Forms",
     "description": "Live markdown editor with split preview."},

    # Display Components
    {"name": "Accordion FAQ", "file": "accordion_faq.py", "category": "Display",
     "description": "FAQ page built with accordion components."},
    {"name": "Progress Tracker", "file": "progress_tracker.py", "category": "Display",
     "description": "Multi-step process with progress and steps."},
    {"name": "Notifications", "file": "notification_system.py", "category": "Display",
     "description": "Toast notifications and alert variants."},

    # Interactive Features
    {"name": "CRUD App", "file": "crud_app.py", "category": "Interactive",
     "description": "Full CRUD operations on a record list."},
    {"name": "Chat App", "file": "chat_app.py", "category": "Interactive",
     "description": "Chat interface with manual message handling."},
    {"name": "Theme Switcher", "file": "theme_switcher.py", "category": "Interactive",
     "description": "Toggle between dark and light themes."},
    {"name": "Keyboard Shortcuts", "file": "keyboard_shortcuts.py", "category": "Interactive",
     "description": "Register and use keyboard shortcuts."},

    # Advanced
    {"name": "Auth Flow", "file": "auth_flow.py", "category": "Advanced",
     "description": "App with login/auth protection."},
    {"name": "Function Wrapper", "file": "function_wrapper.py", "category": "Advanced",
     "description": "Wrap Python functions into auto-generated UIs."},
]

c.title("Cacao Cookbook")
c.text("22 recipes covering every major Cacao feature. Run any recipe with:", color="muted")
c.code("cacao run docs/cookbook/<recipe>.py", language="bash")
c.spacer()

# Group by category
categories = {}
for recipe in RECIPES:
    cat = recipe["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(recipe)

with c.row():
    c.metric("Recipes", str(len(RECIPES)))
    c.metric("Categories", str(len(categories)))

c.spacer()

with c.tabs(default="Getting Started"):
    for cat_name, recipes in categories.items():
        with c.tab(cat_name, label=f"{cat_name} ({len(recipes)})"):
            c.spacer(2)
            for recipe in recipes:
                with c.card(recipe["name"]):
                    c.text(recipe["description"])
                    c.spacer(2)
                    c.code(f"cacao run docs/cookbook/{recipe['file']}", language="bash")
