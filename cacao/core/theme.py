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