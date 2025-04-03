"""
Example of using the global theme system in Cacao.

This demonstrates how to set a custom theme at the application level
and have components inherit these properties.
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
                            "content": "Global Theme Example",
                            "style": {
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "content": "This example demonstrates the global theme system.",
                            "style": {
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "content": "The theme is set at the application level in app.brew() and components inherit these properties.",
                            "style": {
                                "marginBottom": "20px"
                            }
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
                                        "content": "Component-specific styles (sidebar, cards, etc.)",
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

# Create the sidebar layout with optional component-specific styles
sidebar_layout = SidebarLayout(
    nav_items=nav_items, 
    content_components=content_components,
    app_title="Theme Example",
    # Optional component-specific styles
    styles={
        "sidebar_header_bg": "#9b59b6"  # Purple header (overrides the global theme)
    }
)

@app.mix("/")
def home():
    """Main route handler"""
    return sidebar_layout.render()

if __name__ == "__main__":
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Theme Example")
    parser.add_argument("--mode", choices=["web", "desktop"], default="web",
                       help="Run mode: 'web' for browser or 'desktop' for PWA window")
    parser.add_argument("--theme", choices=["default", "dark", "blue"], default="default",
                       help="Theme to use: 'default', 'dark', or 'blue'")
    
    args = parser.parse_args()
    
    # Define custom themes
    themes = {
        "default": None,  # Use default theme
        "dark": {
            "colors": {
                "primary": "#BB86FC",
                "secondary": "#03DAC6",
                "background": "#121212",
                "text": "#FFFFFF",
                "accent": "#CF6679",
                "sidebar_bg": "#1E1E1E",
                "sidebar_header_bg": "#6200EE",
                "sidebar_text": "#BBBBBB",
                "content_bg": "#121212",
                "card_bg": "#2D2D2D",
                "border_color": "#333333"
            }
        },
        "blue": {
            "colors": {
                "primary": "#2196F3",
                "secondary": "#03A9F4",
                "background": "#F0F8FF",
                "text": "#2C3E50",
                "accent": "#FF5722",
                "sidebar_bg": "#1A365D",
                "sidebar_header_bg": "#2C5282",
                "sidebar_text": "#A0AEC0",
                "content_bg": "#F0F8FF",
                "card_bg": "#FFFFFF",
                "border_color": "#BEE3F8"
            }
        }
    }
    
    # Launch application with selected theme
    app.brew(
        type=args.mode,
        title="Theme Example",
        width=800,
        height=600,
        resizable=True,
        fullscreen=False,
        theme=themes[args.theme]
    )