"""
Sidebar layout components for Cacao framework.
Provides components for creating a layout with a left navigation sidebar.
"""

from typing import List, Dict, Any, Optional
from .base import Component
from ...core.state import State, get_state
from ...core.mixins.logging import LoggingMixin
from ...core.theme import get_theme, get_color
import json

# Debug flag for SidebarLayout component
SIDEBAR_DEBUG = False

# Use named global states for proper state synchronization
current_page_state = get_state("current_page", "home")
sidebar_expanded_state = get_state("sidebar_expanded", True)

class SidebarLayout(Component, LoggingMixin):
    def __init__(self, nav_items: List[Dict[str, str]], content_components: Dict[str, Any],
                 app_title: str = "Cacao App", styles: Optional[Dict[str, Any]] = None,
                 show_header: bool = True, show_footer: bool = True, 
                 footer_text: str = "© 2025 Cacao Framework") -> None:
        """Initialize sidebar layout with navigation items and content components.
        
        Args:
            nav_items: List of navigation items with id, label and optional icon
            content_components: Dictionary mapping page IDs to component instances
            app_title: Optional title to display in the sidebar header
            styles: Optional dictionary of style overrides for this component
            show_header: Whether to show the page header with title
            show_footer: Whether to show the footer in the sidebar
            footer_text: Custom text to display in the footer (if shown)
        """
        super().__init__()
        self.nav_items_data = nav_items
        self.content_components = content_components
        self.component_type = "sidebar_layout"
        self.app_title = app_title
        self.styles = styles or {}
        self.show_header = show_header
        self.show_footer = show_footer
        self.footer_text = footer_text
        
        # Initialize page state with first nav item if not set
        if not current_page_state.value or current_page_state.value not in self.content_components:
            default_page = self.nav_items_data[0]["id"] if self.nav_items_data else "home"
            current_page_state.set(default_page)
        
        current_page_state.subscribe(self._handle_page_change)
        sidebar_expanded_state.subscribe(self._handle_sidebar_expand)
        
        # Initialize URL hash synchronization
        self._sync_with_url_hash()

    def _sync_with_url_hash(self) -> None:
        """Sync the current page state with URL hash if available, safely handling Flask context."""
        # Try to access Flask request if available, with proper error handling
        try:
            # Only import Flask inside the method to avoid application context issues
            from flask import request, has_request_context
            
            if has_request_context() and request.args and request.args.get('_hash'):
                hash_value = request.args.get('_hash').lstrip('#')
                if hash_value and hash_value in self.content_components:
                    current_page_state.set(hash_value)
                    return
        except (ImportError, RuntimeError):
            # Silently continue if Flask is not available or outside request context
            pass
        
        # Set default if no hash or invalid hash
        if not current_page_state.value or current_page_state.value not in self.content_components:
            # Use first item from nav_items as default if available
            default_page = self.nav_items_data[0]["id"] if self.nav_items_data else "home"
            if default_page in self.content_components:
                current_page_state.set(default_page)

    def _handle_page_change(self, new_page: str) -> None:
        """Handle page state changes."""
        if new_page in self.content_components:
            # Update URL hash without triggering a new state change
            try:
                import flask
                if flask.has_request_context():
                    flask.current_app.update_hash = new_page
            except (ImportError, RuntimeError):
                pass
                
            # Log the page change if debug is enabled
            if SIDEBAR_DEBUG:
                self.log(f"Page changed to: {new_page}", "info", "🔄")

    def _handle_sidebar_expand(self, expanded: bool) -> None:
        """Handle sidebar expand/collapse changes."""
        # Force update of the component tree when sidebar expands/collapses
        pass

    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the complete sidebar layout with content area.
        
        Args:
            ui_state: Optional state from the server that overrides local state
        
        Returns:
            UI definition for the complete layout
        """
        # Add debug logging to track component rendering
        import inspect
        frame = inspect.currentframe()
        caller = inspect.getouterframes(frame)[1]
        if SIDEBAR_DEBUG:
            print(f"SidebarLayout.render called from {caller.function} with ui_state: {ui_state}")
        is_expanded = sidebar_expanded_state.value
        
        # Get global theme
        theme = get_theme()
        
        # Update global state from UI state or server state if provided
        if ui_state:
            from ...core.state import global_state
            if "_state" in ui_state:
                # Complete server state object
                global_state.update_from_server(ui_state["_state"])
            elif "current_page" in ui_state and ui_state["current_page"] in self.content_components:
                # Direct current_page value
                current_page_state.set(ui_state["current_page"])
        
        # Get current page from global state
        current_page = current_page_state.value
        
        # Ensure current_page is valid
        if not current_page or current_page not in self.content_components:
            current_page = self.nav_items_data[0]["id"] if self.nav_items_data else "home"
            current_page_state.set(current_page)
        
        # Log rendering information if debug is enabled
        if SIDEBAR_DEBUG:
            self.log(f"Rendering with current_page: {current_page}", "debug", "🎯")

        # Create nav items
        nav_items = []
        for item in self.nav_items_data:
            nav_item = NavItem(
                id=item["id"],
                label=item["label"],
                icon=item.get("icon"),
                is_active=item["id"] == current_page
            )
            # Set parent reference for theme access
            nav_item.parent = self
            nav_items.append(nav_item)

        # Create sidebar component
        sidebar = Sidebar(
            nav_items=nav_items, 
            app_title=self.app_title,
            show_footer=self.show_footer,
            footer_text=self.footer_text
        )
        # Set parent reference for theme access
        sidebar.parent = self
        
        # Get component for current page
        current_component = self.content_components.get(current_page)
        if not current_component:
            current_content = {
                "type": "text",
                "props": {"content": f"Page not found: {current_page}"}
            }
        else:
            current_content = current_component.render()

        # Prepare content area children
        content_children = []
        
        # Add header if enabled
        if self.show_header:
            content_children.append({
                "type": "div",
                "props": {
                    "style": {
                        "marginBottom": "24px",
                        "paddingBottom": "16px",
                        "borderBottom": f"1px solid {self.styles.get('border_color', get_color('border_color'))}"
                    },
                    "children": [
                        {
                            "type": "h1",
                            "props": {
                                "content": self.nav_items_data[[item["id"] for item in self.nav_items_data].index(current_page)]["label"] if current_page in [item["id"] for item in self.nav_items_data] else "Unknown Page",
                                "style": {
                                    "margin": "0",
                                    "fontSize": self.styles.get("title_size", "24px"),
                                    "fontWeight": self.styles.get("title_weight", "700"),
                                    "color": self.styles.get("title_color", get_color("title_color"))
                                }
                            }
                        }
                    ]
                }
            })
        
        # Add main content wrapper
        content_children.append({
            "type": "div",
            "props": {
                "style": {
                    "backgroundColor": self.styles.get("card_bg", get_color("card_bg")),
                    "borderRadius": "8px",
                    "boxShadow": f"0 1px 3px rgba(107, 66, 38, 0.1)",
                    "padding": self.styles.get("card_padding", "24px"),
                    "border": f"1px solid {self.styles.get('card_border', get_color('card_border'))}"
                },
                "children": [current_content]
            }
        })

        # Return the complete layout
        return {
            "type": "div",
            "component_type": self.component_type,
            "key": f"layout-{current_page}-{is_expanded}",
            "props": {
                "className": "layout-container",
                "style": {
                    "display": "flex",
                    "minHeight": "100vh",
                    "backgroundColor": self.styles.get("content_bg", get_color("content_bg"))
                },
                "children": [
                    sidebar.render(),
                    {
                        "type": "div",
                        "key": f"content-{current_page}",
                        "props": {
                            "className": "content-area",
                            "style": {
                                "flex": "1",
                                "marginLeft": self.styles.get("sidebar_width", "250px") if is_expanded else self.styles.get("sidebar_collapsed_width", "64px"),
                                "padding": self.styles.get("content_padding", "24px 32px"),
                                "transition": "margin-left 0.3s ease",
                                "backgroundColor": self.styles.get("content_bg", get_color("content_bg")),
                                "minHeight": "100vh",
                                "boxSizing": "border-box",
                                "position": "relative"
                            },
                            "children": content_children
                        }
                    }
                ]
            }
        }

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

        if SIDEBAR_DEBUG:
            # --- Debugging Start ---
            print(f"[DEBUG NavItem {self.id}] is_active: {self.is_active}")

        # Ensure hover style doesn't interfere if present
        final_style = {k: v for k, v in base_style.items() if k != "&:hover"}

        if SIDEBAR_DEBUG:
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
            "type": "nav-item",
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
        # The theme will be set by the parent SidebarLayout component
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