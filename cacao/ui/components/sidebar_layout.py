print("DEBUG: Loaded sidebar_layout.py from local source")
"""
Sidebar layout components for Cacao framework.
Provides components for creating a layout with a left navigation sidebar.
"""

from typing import List, Dict, Any, Optional
from .base import Component
from ...core.state import State, get_state
from ...core.mixins.logging import LoggingMixin
from ...core.theme import get_theme, get_color
from .navigation.nav_item.nav_item import NavItem
from .ui.sidebar.sidebar import Sidebar
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
            "type": "section",
            "props": {
                "className": "content-wrapper",
                "style": {
                    "backgroundColor": self.styles.get("card_bg", get_color("card_bg")),
                    "padding": self.styles.get("card_padding", "24px"),
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