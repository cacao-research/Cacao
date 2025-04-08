"""
Example of using the sidebar layout component in Cacao.

This demonstrates how to create a multi-page application with navigation
using Cacao's SidebarLayout component, which handles state management internally.
It also shows how to customize the appearance using the theming system.
"""

import cacao
from cacao.ui.components.sidebar_layout import SidebarLayout

app = cacao.App()

# Define page components
class HomePage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "p",
                        "props": {
                            "content": "Welcome to the Cacao sidebar layout example!",
                            "style": {
                                "color": "#2D2013",
                                "marginBottom": "20px",
                                "fontSize": "16px"
                            }
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "content": "Use the sidebar to navigate between pages.",
                            "style": {
                                "color": "#2D2013"
                            }
                        }
                    }
                ]
            }
        }

class DashboardPage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "grid",
                                "gridTemplateColumns": "repeat(2, 1fr)",
                                "gap": "20px"
                            },
                            "children": [
                                # Card 1
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "backgroundColor": "#F5F5F5",
                                            "borderRadius": "8px",
                                            "padding": "20px",
                                            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                                        },
                                        "children": [
                                            {
                                                "type": "h2",
                                                "props": {
                                                    "content": "Users",
                                                    "style": {
                                                        "color": "#6B4226",
                                                        "marginBottom": "10px"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": "1,234",
                                                    "style": {
                                                        "fontSize": "24px",
                                                        "fontWeight": "bold",
                                                        "color": "#2D2013"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                # Card 2
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "backgroundColor": "#F5F5F5",
                                            "borderRadius": "8px",
                                            "padding": "20px",
                                            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                                        },
                                        "children": [
                                            {
                                                "type": "h2",
                                                "props": {
                                                    "content": "Revenue",
                                                    "style": {
                                                        "color": "#6B4226",
                                                        "marginBottom": "10px"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": "$5,678",
                                                    "style": {
                                                        "fontSize": "24px",
                                                        "fontWeight": "bold",
                                                        "color": "#2D2013"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

class SettingsPage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#F5F5F5",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "h2",
                                    "props": {
                                        "content": "Profile Settings",
                                        "style": {
                                            "color": "#6B4226",
                                            "marginBottom": "10px"
                                        }
                                    }
                                },
                                {
                                    "type": "text",
                                    "props": {
                                        "content": "Update your profile information here.",
                                        "style": {
                                            "marginBottom": "20px"
                                        }
                                    }
                                },
                                {
                                    "type": "button",
                                    "props": {
                                        "label": "Save Changes",
                                        "style": {
                                            "backgroundColor": "#6B4226",
                                            "color": "#FFFFFF",
                                            "border": "none",
                                            "borderRadius": "4px",
                                            "padding": "8px 16px",
                                            "cursor": "pointer"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

# Define navigation items
nav_items = [
    {"id": "home", "label": "Home", "icon": "H"},
    {"id": "dashboard", "label": "Dashboard", "icon": "D"},
    {"id": "settings", "label": "Settings", "icon": "S"}
]

# Create page instances
home_page = HomePage()
dashboard_page = DashboardPage()
settings_page = SettingsPage()

# Define content components for each page
content_components = {
    "home": home_page,
    "dashboard": dashboard_page,
    "settings": settings_page
}


# Create the sidebar layout with app title and custom theme
sidebar_layout = SidebarLayout(
    nav_items=nav_items,
    content_components=content_components,
    app_title="My Cacao App",
    show_header=False,
    show_footer=False
    
)

@app.mix("/")
def home():
    """Main route handler - SidebarLayout handles state management internally"""
    # The SidebarLayout component now handles all state management internally
    return sidebar_layout.render()

if __name__ == "__main__":
    import argparse
    import sys
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Sidebar Layout Example")
    parser.add_argument("--mode", choices=["web", "desktop"], default="web",
                       help="Run mode: 'web' for browser or 'desktop' for PWA window")
    parser.add_argument("--width", type=int, default=800, help="Window width (desktop mode only)")
    parser.add_argument("--height", type=int, default=600, help="Window height (desktop mode only)")
    
    args = parser.parse_args()
    
    # Launch application in the specified mode using the unified brew() method
    app.brew(
        type=args.mode,
        title="Sidebar Layout Example - Desktop Mode",
        width=args.width,
        height=args.height,
        resizable=True,
        fullscreen=False,
    )
