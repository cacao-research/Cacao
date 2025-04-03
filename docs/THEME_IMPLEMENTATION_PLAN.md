# Theme Implementation Plan

This document outlines the plan for implementing a simplified global theming system for the Cacao framework.

## Overview

The goal is to create a global theme system that allows setting theme properties at the application level and having components inherit these properties. Components can also have local style customizations.

## Implementation Steps

### 1. Create Global Theme System

Create a new file `cacao/core/theme.py` with the following content:

```python
"""
Theme module for the Cacao framework.
Provides a global theme system for consistent styling across components.
"""

from typing import Dict, Any, Optional
import copy

# Default theme with basic color properties
DEFAULT_THEME = {
    "colors": {
        "primary": "#3498db",      # Primary color for buttons, links, etc.
        "secondary": "#2ecc71",    # Secondary color for accents
        "background": "#ffffff",   # Main background color
        "text": "#333333",         # Main text color
        "accent": "#e74c3c",       # Accent color for highlights
        
        # Component-specific colors (for backward compatibility)
        "sidebar_bg": "#2D2013",          # Sidebar background
        "sidebar_header_bg": "#6B4226",   # Sidebar header background
        "sidebar_text": "#D6C3B6",        # Sidebar text color
        "content_bg": "#FAF6F3",          # Content area background
        "card_bg": "#FFFFFF",             # Card background
        "border_color": "#D6C3B6",        # Border color
    }
}

# Global theme instance
_global_theme = copy.deepcopy(DEFAULT_THEME)

def get_theme() -> Dict[str, Any]:
    """
    Get the current global theme.
    
    Returns:
        Dict containing the current theme properties
    """
    return _global_theme

def set_theme(theme: Dict[str, Any]) -> None:
    """
    Set the global theme.
    
    Args:
        theme: Dictionary containing theme properties to set
    """
    global _global_theme
    
    # Deep merge the provided theme with the current theme
    if "colors" in theme:
        _global_theme["colors"].update(theme["colors"])
    
    # Add other theme categories as needed (fonts, spacing, etc.)

def reset_theme() -> None:
    """Reset the global theme to default values."""
    global _global_theme
    _global_theme = copy.deepcopy(DEFAULT_THEME)

def get_color(color_name: str, default: Optional[str] = None) -> str:
    """
    Get a color from the global theme.
    
    Args:
        color_name: Name of the color to get
        default: Default value if color is not found
        
    Returns:
        Color value as a string
    """
    return _global_theme["colors"].get(color_name, default)
```

### 2. Update App Class

Modify `cacao/core/app.py` to accept a theme parameter in the `brew()` method:

```python
def brew(self, type: str = "web", host: str = "localhost", http_port: int = 1634, ws_port: int = 1633,
         title: str = "Cacao App", width: int = 800, height: int = 600,
         resizable: bool = True, fullscreen: bool = False, ASCII_debug: bool = False,
         theme: Dict[str, Any] = None):
    """
    Start the application in web or desktop mode.
    Like brewing a delicious cup of hot chocolate!
    
    Args:
        type: Application type, either "web" or "desktop"
        host: Host address to bind the server to
        http_port: Port number for the HTTP server
        ws_port: Port number for the WebSocket server
        title: Window title (desktop mode only)
        width: Window width in pixels (desktop mode only)
        height: Window height in pixels (desktop mode only)
        resizable: Whether window can be resized (desktop mode only)
        fullscreen: Whether to start in fullscreen mode (desktop mode only)
        ASCII_debug: If True, disables emojis in logs for better compatibility
        theme: Dictionary containing theme properties
    """
    # Set the global theme if provided
    if theme:
        from .theme import set_theme
        set_theme(theme)
    
    # Rest of the method remains unchanged
    # ...
```

### 3. Update Core Module Initialization

Update `cacao/core/__init__.py` to expose the theme functions:

```python
from .theme import get_theme, set_theme, reset_theme, get_color

# Add to __all__ list
__all__ = [
    # ... existing exports
    "get_theme",
    "set_theme",
    "reset_theme",
    "get_color"
]
```

### 4. Modify SidebarLayout Component

Update `cacao/ui/components/sidebar_layout.py` to use the global theme:

```python
from typing import List, Dict, Any, Optional
from .base import Component
from ...core.state import State, get_state
from ...core.mixins.logging import LoggingMixin
from ...core.theme import get_theme, get_color

# Rest of the imports...

class SidebarLayout(Component, LoggingMixin):
    def __init__(self, nav_items: List[Dict[str, str]], content_components: Dict[str, Any], 
                 app_title: str = "Cacao App", styles: Optional[Dict[str, Any]] = None) -> None:
        """Initialize sidebar layout with navigation items and content components.
        
        Args:
            nav_items: List of navigation items with id, label and optional icon
            content_components: Dictionary mapping page IDs to component instances
            app_title: Optional title to display in the sidebar header
            styles: Optional dictionary of style overrides for this component
        """
        super().__init__()
        self.nav_items_data = nav_items
        self.content_components = content_components
        self.component_type = "sidebar_layout"
        self.app_title = app_title
        self.styles = styles or {}
        
        # Rest of the initialization...
```

Then update the `render()` method to use the global theme:

```python
def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Render the complete sidebar layout with content area."""
    is_expanded = sidebar_expanded_state.value
    
    # Get global theme
    theme = get_theme()
    
    # Rest of the method...
    
    # Use theme colors with optional style overrides
    content_bg = self.styles.get("content_bg", get_color("content_bg"))
    sidebar_bg = self.styles.get("sidebar_bg", get_color("sidebar_bg"))
    # etc.
    
    # Return the complete layout with theme colors
    return {
        "type": "div",
        "component_type": self.component_type,
        "key": f"layout-{current_page}-{is_expanded}",
        "props": {
            "className": "layout-container",
            "style": {
                "display": "flex",
                "minHeight": "100vh",
                "backgroundColor": content_bg
            },
            # Rest of the layout...
        }
    }
```

Make similar updates to the `NavItem` and `Sidebar` classes.

### 5. Create Example

Create a new example file `examples/theme_example.py`:

```python
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
                    }
                ]
            }
        }

# Define navigation items
nav_items = [
    {"id": "home", "label": "Home", "icon": "H"},
    {"id": "settings", "label": "Settings", "icon": "S"}
]

# Create page instances
home_page = HomePage()

# Define content components for each page
content_components = {
    "home": home_page
}

# Create the sidebar layout
sidebar_layout = SidebarLayout(
    nav_items=nav_items, 
    content_components=content_components,
    app_title="Theme Example",
    # Optional component-specific styles
    styles={
        "sidebar_header_bg": "#9b59b6"  # Purple header
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
```

## Next Steps

After implementing these changes, you'll have a global theme system that:

1. Allows setting theme properties at the application level
2. Makes components inherit these properties automatically
3. Supports component-level style customizations
4. Maintains backward compatibility with existing components

You can expand this system in the future by adding more theme categories like fonts, spacing, borders, etc.