"""
Theme module for the Cacao framework.
Provides functionality for loading and serving theme CSS.
"""

from typing import Dict, Any, Optional
from ..ui.themes.theme_loader import load_theme, get_sidebar_theme
from ..ui.themes.default_theme import DefaultTheme

def get_theme_css() -> str:
    """
    Get the combined CSS from all active themes.
    
    Returns:
        str: The combined CSS from all active themes.
    """
    # Load base theme CSS
    theme_assets = load_theme("default")
    css = theme_assets["css"] or DefaultTheme.CSS
    
    # Add component-specific themes
    sidebar_theme = get_sidebar_theme()
    if hasattr(sidebar_theme, 'CSS'):
        css += f"\n/* Sidebar Theme */\n{sidebar_theme.CSS}"
    
    return css

# Add a route decorator to handle theme CSS requests
from .decorators import mix

@mix('/api/theme-css')
def serve_theme_css(request, response):
    """
    Serve the theme CSS.
    
    Args:
        request: The HTTP request.
        response: The HTTP response.
        
    Returns:
        dict: The response data.
    """
    css = get_theme_css()
    
    # Set response headers
    response.headers['Content-Type'] = 'text/css'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    # Return the CSS
    return css

def get_theme(component: Optional[str] = None) -> Dict[str, Any]:
    """
    Get theme settings for a specific component or the default theme.
    
    Args:
        component: Optional component name to get specific theme settings
        
    Returns:
        dict: The theme settings
    """
    if component == 'sidebar':
        return get_sidebar_theme().DEFAULT_COLORS
    
    # Return default theme CSS variables as a dict
    css_vars = {}
    for line in DefaultTheme.CSS.split('\n'):
        if '--' in line and ':' in line:
            var = line.split('--')[1].split(':')[0].strip()
            value = line.split(':')[1].split(';')[0].strip()
            css_vars[var] = value
            
    return css_vars

def get_color(color_name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a specific color from the theme.
    
    Args:
        color_name (str): Name of the color to get. Can be:
            - CSS variable name with or without -- prefix
            - Sidebar theme color name (e.g. 'sidebar_bg', 'active_text')
        default (str, optional): Default value if color is not found
        
    Returns:
        str: The color value or default if not found
    """
    # Remove -- prefix if present
    clean_name = color_name.replace('--', '')
    
    # First try sidebar theme colors
    sidebar_colors = get_sidebar_theme().DEFAULT_COLORS
    if clean_name in sidebar_colors:
        return sidebar_colors[clean_name]
        
    # Then try default theme CSS variables
    theme_vars = get_theme()
    if clean_name in theme_vars:
        return theme_vars[clean_name]
    
    # Try direct color names without CSS variable syntax
    colors_map = {
        'primary': 'primary-color',
        'secondary': 'secondary-color',
        'text': 'font-color',
        'background': 'bg-color'
    }
    if clean_name in colors_map and colors_map[clean_name] in theme_vars:
        return theme_vars[colors_map[clean_name]]
        
    return default

def set_theme(theme_settings: Dict[str, Any], component: Optional[str] = None):
    """
    Update theme settings.
    
    Args:
        theme_settings (dict): Dictionary of theme settings to update
        component (str, optional): Component to update theme for (e.g. 'sidebar')
    """
    if component == 'sidebar':
        sidebar_theme = get_sidebar_theme(theme_settings)
        # Theme will be applied on next render
        return
        
    # Default theme updates are handled via CSS variables
    # Changes will be reflected when CSS is served
    pass

def reset_theme() -> Dict[str, Any]:
    """
    Reset theme to default settings.
    
    This resets both the default theme and any component-specific themes
    back to their original states.
    
    Returns:
        dict: The default theme settings
    """
    # Reset sidebar theme
    _ = get_sidebar_theme(None)  # Passing None resets to defaults
    
    # Reset default theme (returns CSS variables as dict)
    return get_theme()