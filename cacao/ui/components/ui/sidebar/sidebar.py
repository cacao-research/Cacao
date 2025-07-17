"""
Sidebar Component Python Integration
"""

from typing import Dict, Any, Optional, List
from ...base import Component
from .....core.theme import get_theme, get_color
from .....core.state import State, get_state
from ...navigation.nav_item.nav_item import NavItem

import json

# Debug flag for Sidebar component
SIDEBAR_DEBUG = False

# Use named global states for proper state synchronization
current_page_state = get_state("current_page", "home")
sidebar_expanded_state = get_state("sidebar_expanded", True)

class Sidebar(Component):
    def __init__(self, nav_items: List[NavItem], app_title: str = "Cacao App", 
                 show_footer: bool = True, footer_text: str = "© 2025 Cacao Framework") -> None:
        """Initialize sidebar with navigation items.
        
        Args:
            nav_items: List of NavItem components
            app_title: Title to display in the sidebar header
            show_footer: Whether to show the footer in the sidebar
            footer_text: Custom text to display in the footer (if shown)
        """
        # The theme will be set by the parent Sidebar component
        super().__init__()
        self.nav_items = nav_items
        self.app_title = app_title
        self.show_footer = show_footer
        self.footer_text = footer_text
        
    def render(self) -> Dict[str, Any]:
        # Get theme colors
        theme = get_theme()
        theme_colors = theme.get('colors', {})
        
        children = [
            # App header/brand section
            {
                "type": "div",
                "props": {
                    "style": {
                        "padding": "20px 16px",
                        "borderBottom": f"1px solid {self.parent.styles.get('sidebar_border', get_color('sidebar_border'))}",
                        "display": "flex",
                        "alignItems": "center",
                        "height": "64px",
                        "backgroundColor": self.parent.styles.get("sidebar_header_bg", get_color("sidebar_header_bg"))
                    },
                    "children": [
                        {
                            "type": "h2",
                            "props": {
                                "content": self.app_title,
                                "style": {
                                    "margin": 0,
                                    "fontSize": "18px",
                                    "fontWeight": "600",
                                    "color": self.parent.styles.get("app_title_color", theme_colors.get("app_title_color", "#D6C3B6"))
                                }
                            }
                        }
                    ]
                }
            },
            # Navigation items container
            {
                "type": "div",
                "props": {
                    "style": {
                        "padding": "16px 0",
                        "flex": 1,
                        "overflowY": "auto"
                    },
                    "children": [nav_item.render() for nav_item in self.nav_items]
                }
            }
        ]
        
        # Add footer if enabled
        if self.show_footer:
            children.append({
                "type": "div",
                "props": {
                    "style": {
                        "borderTop": f"1px solid {self.parent.styles.get('sidebar_border', get_color('sidebar_border'))}",
                        "padding": "16px",
                        "fontSize": "12px",
                        "color": self.parent.styles.get("sidebar_text", get_color("sidebar_text"))
                    },
                    "children": [
                        {
                            "type": "text",
                            "props": {
                                "content": self.footer_text,
                                "style": {
                                    "margin": 0
                                }
                            }
                        }
                    ]
                }
            })
        
        return {
            "type": "sidebar",
            "key": "sidebar",
            "props": {
                "style": {
                    "width": self.parent.styles.get("sidebar_width", "250px") if sidebar_expanded_state.value else self.parent.styles.get("sidebar_collapsed_width", "64px"),
                    "height": "100vh",
                    "position": "fixed",
                    "top": 0,
                    "left": 0,
                    "backgroundColor": self.parent.styles.get("sidebar_bg", get_color("sidebar_bg")),
                    "color": self.parent.styles.get("active_text", get_color("active_text")),
                    "boxShadow": "0 0 15px rgba(107, 66, 38, 0.15)",
                    "transition": "width 0.3s ease",
                    "padding": "0",
                    "display": "flex",
                    "flexDirection": "column",
                    "zIndex": 1000
                },
                "children": children
            }
        }