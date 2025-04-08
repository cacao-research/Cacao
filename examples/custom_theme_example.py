"""
Example of creating and using a completely custom theme in Cacao.

This demonstrates how to create a custom theme for the SidebarLayout component
and apply it to your application.
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
                "children": [
                    {
                        "type": "h1",
                        "props": {
                            "content": "Custom Theme Example",
                            "style": {
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "content": "This example demonstrates how to create and use a completely custom theme.",
                            "style": {
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "content": "The current theme uses a dark mode with purple accents.",
                        }
                    }
                ]
            }
        }

class ThemingPage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "children": [
                    {
                        "type": "h1",
                        "props": {
                            "content": "Theme Customization",
                            "style": {
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "content": "You can customize the following aspects of the theme:",
                            "style": {
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "ul",
                        "props": {
                            "style": {
                                "marginLeft": "20px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "li",
                                    "props": {
                                        "content": "Colors (background, text, borders, etc.)",
                                        "style": {
                                            "marginBottom": "10px"
                                        }
                                    }
                                },
                                {
                                    "type": "li",
                                    "props": {
                                        "content": "Spacing (padding, margins, widths, etc.)",
                                        "style": {
                                            "marginBottom": "10px"
                                        }
                                    }
                                },
                                {
                                    "type": "li",
                                    "props": {
                                        "content": "Fonts (sizes, weights, etc.)",
                                        "style": {
                                            "marginBottom": "10px"
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
    {"id": "theming", "label": "Theming", "icon": "T"}
]

# Create page instances
home_page = HomePage()
theming_page = ThemingPage()

# Define content components for each page
content_components = {
    "home": home_page,
    "theming": theming_page
}

# Create a dark theme with purple accents
dark_purple_theme = {
    "colors": {
        # Background colors
        "content_bg": "#121212",          # Dark background
        "sidebar_bg": "#1E1E1E",          # Slightly lighter dark background
        "sidebar_header_bg": "#6200EE",   # Purple header
        "card_bg": "#2D2D2D",             # Dark gray card background
        
        # Text colors
        "title_color": "#BB86FC",         # Light purple for titles
        "text_color": "#FFFFFF",          # White text
        "sidebar_text": "#BBBBBB",        # Light gray text for sidebar
        "active_text": "#FFFFFF",         # White text for active items
        
        # Border colors
        "border_color": "#333333",        # Dark gray border
        "card_border": "#333333",         # Dark gray card border
        "sidebar_border": "#333333",      # Dark gray sidebar border
        
        # Interactive element colors
        "active_bg": "#6200EE",           # Purple active background
        "active_icon_bg": "#BB86FC",      # Light purple for active icons
        "inactive_icon_bg": "rgba(187, 134, 252, 0.3)",  # Transparent purple for inactive icons
    },
    "spacing": {
        "sidebar_width": "280px",         # Slightly wider sidebar
        "sidebar_collapsed_width": "70px", # Slightly wider collapsed sidebar
        "content_padding": "32px 40px",   # More padding in content area
        "card_padding": "28px",           # More padding in cards
        "nav_item_padding": "14px 18px",  # More padding in nav items
    },
    "fonts": {
        "title_size": "28px",             # Larger titles
        "title_weight": "600",            # Slightly less bold titles
        "nav_item_size": "16px",          # Larger nav items
        "nav_item_weight": "500",         # Medium weight nav items
    }
}

# Create the sidebar layout with app title and custom theme
sidebar_layout = SidebarLayout(
    nav_items=nav_items, 
    content_components=content_components,
    app_title="Theme Demo",
    theme=dark_purple_theme
)

@app.mix("/")
def home():
    """Main route handler - SidebarLayout handles state management internally"""
    return sidebar_layout.render()

if __name__ == "__main__":
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Custom Theme Example")
    parser.add_argument("--mode", choices=["web", "desktop"], default="web",
                       help="Run mode: 'web' for browser or 'desktop' for PWA window")
    parser.add_argument("--width", type=int, default=1000, help="Window width (desktop mode only)")
    parser.add_argument("--height", type=int, default=700, help="Window height (desktop mode only)")
    
    args = parser.parse_args()
    
    # Launch application in the specified mode
    app.brew(
        type=args.mode,
        title="Custom Theme Example",
        width=args.width,
        height=args.height,
        resizable=True,
        fullscreen=False
    )