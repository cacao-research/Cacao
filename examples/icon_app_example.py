"""
Example of using the icon registry system in Cacao with a sidebar layout.

This demonstrates how to use custom icons and FontAwesome icons in separate tabs
using Cacao's SidebarLayout component.
"""

import cacao
from cacao import Component
from cacao.ui.components.sidebar_layout import SidebarLayout
from typing import Dict, Any, Optional

app = cacao.App()

# Register a custom user icon
custom_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M12,4C14.21,4 16,5.79 16,8C16,10.21 14.21,12 12,12C9.79,12 8,10.21 8,8C8,5.79 9.79,4 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" fill="currentColor"/>
</svg>
"""
cacao.icon_registry.register_icon("user", custom_svg)

class CustomIconsPage(Component):
    def _create_icon_card(self, label: str, icon_markup: str) -> Dict[str, Any]:
        return {
            "type": "div",
            "props": {
                "style": {
                    "backgroundColor": "#F5F5F5",
                    "borderRadius": "8px",
                    "padding": "20px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "15px"
                },
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "60px",
                                "height": "60px",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "backgroundColor": "white",
                                "borderRadius": "12px",
                                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"
                            },
                            "children": [
                                {
                                    "type": "text",
                                    "props": {
                                        "content": icon_markup
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "text",
                        "props": {
                            "content": label,
                            "style": {
                                "fontSize": "16px",
                                "color": "#2D2013"
                            }
                        }
                    }
                ]
            }
        }

    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the custom icons page.
        
        Args:
            ui_state: Optional UI state data
            
        Returns:
            Dict[str, Any]: Component UI definition
        """
        # Define the custom icons to display with their names, icons, colors, and sizes
        custom_icons = [
            ("Home Icon", "home", "#6B4226", 32),
            ("Bean Icon", "bean", "#D4A76A", 32),
            ("User Icon", "user", "#3498db", 32),
            ("Settings Icon", "settings", "#9b59b6", 32),
            ("Cloud Icon", "cloud", "#3498db", 32),
            ("Fire Icon", "fire", "#e74c3c", 32),
            ("Chef Hat", "chef-hat", "#2c3e50", 32),
            ("Star Icon", "star", "#f1c40f", 36),
            ("Trash Icon", "trash", "#e74c3c", 32),
            ("Whisk Icon", "whisk", "#7f8c8d", 36),
            ("Menu Icon", "menu", "#2c3e50", 32),
            ("Hot Drink", "hot-drink", "#6f4e37", 32)
        ]
        
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "content": "Custom Icons",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "grid",
                                "gridTemplateColumns": "repeat(auto-fill, minmax(200px, 1fr))",
                                "gap": "20px"
                            },
                            "children": [
                                self._create_icon_card(
                                    label, 
                                    f"{{%icon-ca-{icon} size={size} color={color}%}}"
                                )
                                for label, icon, color, size in custom_icons
                            ]
                        }
                    }
                ]
            }
        }

class FontAwesomePage(Component):
    """Component for displaying FontAwesome icons with proper naming conventions."""
    
    def _create_fa_icon_card(self, icon_name: str, color: str = "#6B4226", size: int = 32) -> Dict[str, Any]:
        """Create a card displaying a FontAwesome icon with its name.
        
        Args:
            icon_name: The FontAwesome icon name without the fa- prefix
            color: The color for the icon in hex format
            size: The size of the icon in pixels
            
        Returns:
            Dict[str, Any]: The icon card component definition
        """
        return {
            "type": "div",
            "props": {
                "style": {
                    "backgroundColor": "#F5F5F5",
                    "borderRadius": "8px",
                    "padding": "20px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "15px"
                },
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "60px",
                                "height": "60px",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "backgroundColor": "white",
                                "borderRadius": "12px",
                                "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"
                            },
                            "content": f"{{%icon-fa-{icon_name} size={size} color={color}%}}"
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "content": f"fa-{icon_name}",
                            "style": {
                                "fontSize": "16px",
                                "color": "#2D2013"
                            }
                        }
                    }
                ]
            }
        }

    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the FontAwesome icons page.
        
        Args:
            ui_state: Optional UI state data
            
        Returns:
            Dict[str, Any]: Component UI definition
        """
        # Define the FontAwesome icons to display with their colors
        fa_icons = [
            ("star", "#FFD700"),       # Gold
            ("heart", "#ff5555"),      # Red
            ("check", "#4CAF50"),      # Green
            ("user", "#3498db"),       # Blue
            ("cog", "#9b59b6"),        # Purple
            ("bell", "#f39c12"),       # Orange
            ("file", "#2ecc71"),       # Green
            ("calendar", "#e74c3c"),    # Red
            ("home", "#1abc9c"),       # Teal
            ("search", "#34495e"),     # Dark Blue
            ("envelope", "#7f8c8d"),    # Gray
            ("lock", "#f1c40f"),        # Yellow
            ("trash", "#e74c3c"),       # Red
            ("coffee", "#6f4e37"),      # Brown
            ("download", "#2980b9"),    # Blue
            ("upload", "#2980b9"),      # Blue
            ("camera", "#9b59b6"),      # Purple
            ("pencil", "#f39c12"),      # Orange
            ("globe", "#3498db"),       # Blue
            ("microphone", "#e67e22"),  # Orange
            ("music", "#2ecc71"),       # Green
            ("shopping-cart", "#e74c3c"), # Red
            ("plus", "#2c3e50"),        # Dark Blue/Gray
            ("minus", "#2c3e50")        # Dark Blue/Gray
        ]

        
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "content": "FontAwesome Icons",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "grid",
                                "gridTemplateColumns": "repeat(auto-fill, minmax(250px, 1fr))",
                                "gap": "20px"
                            },
                            "children": [
                                self._create_fa_icon_card(icon_name, color) 
                                for icon_name, color in fa_icons
                            ]
                        }
                    }
                ]
            }
        }

class GuidelinePage(Component):
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px"
                },
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "content": "Icon Usage Guidelines",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    {
                        "type": "pre",
                        "props": {
                            "style": {
                                "backgroundColor": "#f5f5f5",
                                "padding": "20px",
                                "borderRadius": "8px",
                                "overflow": "auto",
                                "fontSize": "14px",
                                "lineHeight": "1.5"
                            },
                            "content": """# Custom SVG icons
{%icon-ca-name size=32%}
{%icon-ca-name size=32 color=#ff0000%}

# FontAwesome icons
{%icon-fa-name size=32%}
{%icon-fa-name size=32 color=#00ff00%}"""
                        }
                    }
                ]
            }
        }

# Define navigation items with icons
nav_items = [
    {"id": "custom", "label": "Custom Icons", "icon": "{%icon-ca-home size=16 color=#fff%}"},
    {"id": "fontawesome", "label": "FontAwesome", "icon": "{%icon-fa-star size=16 color=#fff%}"},
    {"id": "guidelines", "label": "Guidelines", "icon": "{%icon-fa-book size=16 color=#fff%}"}
]

# Create page instances
custom_icons_page = CustomIconsPage()
fontawesome_page = FontAwesomePage()
guidelines_page = GuidelinePage()

# Define content components for each page
content_components = {
    "custom": custom_icons_page,
    "fontawesome": fontawesome_page,
    "guidelines": guidelines_page
}

# Create the sidebar layout
sidebar_layout = SidebarLayout(
    nav_items=nav_items,
    content_components=content_components,
    app_title="Cacao Icons"
)

@app.mix("/")
def home() -> Dict[str, Any]:
    """Main route handler for the icon demo app."""
    return sidebar_layout.render()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Icon Registry Example")
    parser.add_argument("--mode", choices=["web", "desktop"], default="web",
                       help="Run mode: 'web' for browser or 'desktop' for PWA window")
    parser.add_argument("--width", type=int, default=1024, help="Window width (desktop mode only)")
    parser.add_argument("--height", type=int, default=768, help="Window height (desktop mode only)")
    
    args = parser.parse_args()
    
    print("Starting icon demo app...")
    app.brew(
        type=args.mode,
        title="Cacao Icons",
        width=args.width,
        height=args.height,
        resizable=True,
        fullscreen=False
    )