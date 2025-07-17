"""
Nav Item Component Python Integration
"""

from typing import Dict, Any, Optional
import json
from ...base import Component
from .....core.theme import get_theme, get_color

# Debug flag for NavItem component
NAV_ITEM_DEBUG = False

class NavItem(Component):
    def __init__(self, id: str, label: str, icon: Optional[str] = None, is_active: bool = False) -> None:
        super().__init__()
        self.id = id
        self.label = label
        self.icon = icon
        self.is_active = is_active

    def render(self) -> Dict[str, Any]:
        # Get styles from parent component or use global theme
        parent_styles = {}
        if hasattr(self, 'parent') and hasattr(self.parent, 'styles'):
            parent_styles = self.parent.styles
        
        # Get global theme and colors
        theme = get_theme()
        theme_colors = theme.get('colors', {})
        
        # Base and active styles
        base_style = {
            "display": "flex",
            "alignItems": "center",
            "padding": parent_styles.get("nav_item_padding", "12px 16px"),
            "margin": "4px 8px",
            "borderRadius": "8px",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "color": parent_styles.get("sidebar_text", theme_colors.get("sidebar_text", "#D6C3B6")),
            "fontSize": parent_styles.get("nav_item_size", "15px"),
            "fontWeight": parent_styles.get("nav_item_weight", "500"),
            "textDecoration": "none",
        }
        
        # Apply active styles when item is selected
        if self.is_active:
            # Get theme colors with proper fallbacks
            theme = get_theme()
            theme_colors = theme.get('colors', {})
            active_styles = {
                "backgroundColor": parent_styles.get("active_bg", theme_colors.get("active_bg", "#D6C3B6")),
                "color": parent_styles.get("active_text", theme_colors.get("active_text", "#FFFFFF")),
                "boxShadow": "0 2px 5px rgba(107, 66, 38, 0.3)"
            }
            # Merge active styles into base styles
            base_style.update(active_styles)
        else:
            # Hover effect will be handled by CSS in the real app
            # Here we're defining the non-active state
            base_style["backgroundColor"] = "transparent"

        if NAV_ITEM_DEBUG:
            # --- Debugging Start ---
            print(f"[DEBUG NavItem {self.id}] is_active: {self.is_active}")

        # Ensure hover style doesn't interfere if present
        final_style = {k: v for k, v in base_style.items() if k != "&:hover"}

        if NAV_ITEM_DEBUG:
            print(f"[DEBUG NavItem {self.id}] Final style prop: {json.dumps(final_style, indent=2)}")
            # --- Debugging End ---
                
        # Create the icon element if provided
        icon_element = None
        if self.icon:
            icon_element = {
                "type": "div",
                "props": {
                    "style": {
                        "width": "28px",
                        "height": "28px", 
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "marginRight": "14px",
                        "backgroundColor": parent_styles.get("active_icon_bg", theme_colors.get("active_icon_bg", "#8B5E41")) if self.is_active else parent_styles.get("inactive_icon_bg", theme_colors.get("inactive_icon_bg", "rgba(107, 66, 38, 0.3)")),
                        "color": parent_styles.get("active_text", theme_colors.get("active_text", "#FFFFFF")),
                        "borderRadius": "6px",
                        "fontSize": "16px",
                        "fontWeight": "bold"
                    },
                    "children": [{
                        "type": "text",
                        "props": {
                            "content": self.icon,
                            "style": {
                                "color": parent_styles.get("active_text", get_color("active_text"))
                            }
                        }
                    }]
                }
            }

        children = []
        if icon_element:
            children.append(icon_element)
            
        # Add the label with improved visibility
        children.append({
            "type": "text",
            "props": {
                "content": self.label,
                "style": {
                    "whiteSpace": "nowrap",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "fontWeight": "500",
                    "fontSize": "15px",
                    "color": parent_styles.get("active_text", get_color("active_text")) if self.is_active else parent_styles.get("sidebar_text", get_color("sidebar_text"))
                }
            }
        })
        
        return {
            "type": "nav_item",
            "key": f"nav-{self.id}",
            "props": {
                "style": final_style, # Use the debugged style dict
                "children": children,
                "onClick": {
                    "action": "set_state",
                    "state": "current_page",
                    "value": self.id,
                    "immediate": True  # Signal that this state change should be applied immediately
                }
            }
        }