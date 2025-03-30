"""
Sidebar layout components for Cacao framework.
Provides components for creating a layout with a left navigation sidebar.
"""

from typing import List, Dict, Any, Optional
from .base import Component
from ...core.state import State, get_state
from ...core.mixins.logging import LoggingMixin

# Debug flag for SidebarLayout component
SIDEBAR_DEBUG = False

# Use named global states for proper state synchronization
current_page_state = get_state("current_page", "home")
sidebar_expanded_state = get_state("sidebar_expanded", True)

class SidebarLayout(Component, LoggingMixin):
    def __init__(self, nav_items: List[Dict[str, str]], content_components: Dict[str, Any], 
                 app_title: str = "Cacao App") -> None:
        """Initialize sidebar layout with navigation items and content components.
        
        Args:
            nav_items: List of navigation items with id, label and optional icon
            content_components: Dictionary mapping page IDs to component instances
            app_title: Optional title to display in the sidebar header
        """
        super().__init__()
        self.nav_items_data = nav_items
        self.content_components = content_components
        self.component_type = "sidebar_layout"
        self.app_title = app_title
        
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
        is_expanded = sidebar_expanded_state.value
        
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
            nav_items.append(NavItem(
                id=item["id"],
                label=item["label"],
                icon=item.get("icon"),
                is_active=item["id"] == current_page
            ))

        # Create sidebar component
        sidebar = Sidebar(nav_items, self.app_title)
        
        # Get component for current page
        current_component = self.content_components.get(current_page)
        if not current_component:
            current_content = {
                "type": "text",
                "props": {"content": f"Page not found: {current_page}"}
            }
        else:
            current_content = current_component.render()

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
                    "backgroundColor": "#FAF6F3"  # Light cream background for content area
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
                                "marginLeft": "250px" if is_expanded else "64px",
                                "padding": "24px 32px",
                                "transition": "margin-left 0.3s ease",
                                "backgroundColor": "#FAF6F3",  # Light cream background
                                "minHeight": "100vh",
                                "boxSizing": "border-box",
                                "position": "relative"
                            },
                            "children": [
                                # Header with page title
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "marginBottom": "24px",
                                            "paddingBottom": "16px",
                                            "borderBottom": "1px solid #D6C3B6"  # Light brown border
                                        },
                                        "children": [
                                            {
                                                "type": "h1",
                                                "props": {
                                                    "content": self.nav_items_data[[item["id"] for item in self.nav_items_data].index(current_page)]["label"] if current_page in [item["id"] for item in self.nav_items_data] else "Unknown Page",
                                                    "style": {
                                                        "margin": "0",
                                                        "fontSize": "24px",
                                                        "fontWeight": "700",
                                                        "color": "#6B4226"  # Cacao brown title
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                # Main content wrapper
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "backgroundColor": "#FFFFFF",
                                            "borderRadius": "8px",
                                            "boxShadow": "0 1px 3px rgba(107, 66, 38, 0.1)",  # Brown shadow
                                            "padding": "24px",
                                            "border": "1px solid #E6D7CC"  # Very light brown border
                                        },
                                        "children": [current_content]
                                    }
                                }
                            ]
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
        # Base and active styles
        base_style = {
            "display": "flex",
            "alignItems": "center",
            "padding": "12px 16px",
            "margin": "4px 8px",
            "borderRadius": "8px",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "color": "#D6C3B6",  # Light brown text for better visibility
            "fontSize": "15px",
            "fontWeight": "500",
            "textDecoration": "none",
        }
        
        # Apply active styles when item is selected
        if self.is_active:
            active_styles = {
                "backgroundColor": "#6B4226",  # Cacao brown active background
                "color": "#FFFFFF",  # White text for active item
                "boxShadow": "0 2px 5px rgba(107, 66, 38, 0.3)"
            }
            # Merge active styles into base styles
            base_style.update(active_styles)
        else:
            # Hover effect will be handled by CSS in the real app
            # Here we're defining the non-active state
            base_style["backgroundColor"] = "transparent"
            base_style["&:hover"] = {
                "backgroundColor": "rgba(107, 66, 38, 0.2)",
                "color": "#FFFFFF"
            }
            
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
                        "backgroundColor": "#8B5E41" if self.is_active else "rgba(107, 66, 38, 0.3)",
                        "color": "#FFFFFF",
                        "borderRadius": "6px",
                        "fontSize": "16px",
                        "fontWeight": "bold"
                    },
                    "children": [{
                        "type": "text",
                        "props": {
                            "content": self.icon,
                            "style": {
                                "color": "#FFFFFF"  # Ensure icon text is white for visibility
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
                    "color": "#FFFFFF" if self.is_active else "#D6C3B6"  # Ensure text is visible
                }
            }
        })
        
        return {
            "type": "nav-item",
            "key": f"nav-{self.id}",
            "props": {
                "style": base_style,
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
    def __init__(self, nav_items: List[NavItem], app_title: str = "Cacao App") -> None:
        """Initialize sidebar with navigation items.
        
        Args:
            nav_items: List of NavItem components
            app_title: Title to display in the sidebar header
        """
        super().__init__()
        self.nav_items = nav_items
        self.app_title = app_title
        
    def render(self) -> Dict[str, Any]:
        return {
            "type": "sidebar",
            "key": "sidebar",
            "props": {
                "style": {
                    "width": "250px" if sidebar_expanded_state.value else "64px",
                    "height": "100vh",
                    "position": "fixed",
                    "top": 0,
                    "left": 0,
                    "backgroundColor": "#2D2013",  # Dark brown background
                    "color": "#FFFFFF",
                    "boxShadow": "0 0 15px rgba(107, 66, 38, 0.15)",
                    "transition": "width 0.3s ease",
                    "padding": "0",
                    "display": "flex",
                    "flexDirection": "column",
                    "zIndex": 1000
                },
                "children": [
                    # App header/brand section
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "padding": "20px 16px",
                                "borderBottom": "1px solid #503418",  # Medium brown border
                                "display": "flex",
                                "alignItems": "center",
                                "height": "64px",
                                "backgroundColor": "#6B4226"  # Cacao brown header
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
                                            "color": "#FFFFFF"
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
                    },
                    # Footer section with user/account info (optional)
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "borderTop": "1px solid #503418",  # Medium brown border
                                "padding": "16px",
                                "fontSize": "12px",
                                "color": "#D6C3B6"  # Light brown text
                            },
                            "children": [
                                {
                                    "type": "text",
                                    "props": {
                                        "content": "© 2025 Cacao Framework",
                                        "style": {
                                            "margin": 0
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }