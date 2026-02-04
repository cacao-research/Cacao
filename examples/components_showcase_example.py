import cacao.core.theme  # Ensure theme API routes are registered before app/server starts
"""
Example showcasing all UI components in Cacao.

This demonstrates how to use all the available UI components in Cacao,
organized into different categories using the SidebarLayout component.
"""

import cacao
from cacao.ui.components.sidebar_layout import SidebarLayout

# Diagnostic logging to understand the import error
import sys
import os
print(f"DEBUG: Current working directory: {os.getcwd()}")
print(f"DEBUG: Script file path: {__file__}")
print(f"DEBUG: Python path: {sys.path}")
print(f"DEBUG: __name__: {__name__}")
print(f"DEBUG: __package__: {__package__}")

try:
    from .showcase import (
        TypographyPage,
        InputsPage,
        DataDisplayPage,
        NavigationPage,
        FeedbackPage,
        TablePage
    )
    print("DEBUG: Relative import succeeded")
except ImportError as e:
    print(f"DEBUG: Relative import failed: {e}")
    print("DEBUG: Attempting absolute import...")
    try:
        from examples.showcase import (
            TypographyPage,
            InputsPage,
            DataDisplayPage,
            NavigationPage,
            FeedbackPage,
            TablePage
        )
        print("DEBUG: Absolute import succeeded")
    except ImportError as e2:
        print(f"DEBUG: Absolute import also failed: {e2}")
        raise

app = cacao.App()

# Create page instances
typography_page = TypographyPage()
inputs_page = InputsPage()
data_display_page = DataDisplayPage()
navigation_page = NavigationPage()
feedback_page = FeedbackPage()
table_page = TablePage()

# Define navigation items
nav_items = [
    {"id": "typography", "label": "Typography", "icon": "T"},
    {"id": "inputs", "label": "Inputs", "icon": "I"},
    {"id": "data_display", "label": "Data Display", "icon": "D"},
    {"id": "navigation", "label": "Navigation", "icon": "N"},
    {"id": "feedback", "label": "Feedback", "icon": "F"},
    {"id": "tables", "label": "Tables", "icon": "T"}
]

# Define content components for each page
content_components = {
    "typography": typography_page,
    "inputs": inputs_page,
    "data_display": data_display_page,
    "navigation": navigation_page,
    "feedback": feedback_page,
    "tables": table_page
}

# Create the sidebar layout with app title and custom theme
sidebar_layout = SidebarLayout(
    nav_items=nav_items,
    content_components=content_components,
    app_title="Cacao UI Components",
    show_header=True,
    show_footer=False
)

@app.mix("/")
def home():
    """Main route handler - SidebarLayout handles state management internally"""
    return sidebar_layout.render()

if __name__ == "__main__":
    import argparse
    import sys
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Components Showcase Example")
    parser.add_argument("--mode", choices=["web", "desktop"], default="web",
                       help="Run mode: 'web' for browser or 'desktop' for PWA window")
    parser.add_argument("--width", type=int, default=1024, help="Window width (desktop mode only)")
    parser.add_argument("--height", type=int, default=768, help="Window height (desktop mode only)")
    
    args = parser.parse_args()
    
    # Launch application in the specified mode using the unified brew() method
    app.brew(
        type=args.mode,
        title="Cacao UI Components Showcase",
        width=args.width,
        height=args.height,
        resizable=True,
        fullscreen=False,
    )
