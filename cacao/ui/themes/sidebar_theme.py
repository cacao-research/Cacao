"""
Sidebar theme module for the Cacao framework.
Defines theme variables specifically for the sidebar layout component.
"""

from typing import Dict, Any, Optional

class SidebarTheme:
    """
    Theme configuration for the SidebarLayout component.
    Provides color and style variables for customizing the sidebar appearance.
    """
    
    # Default color palette
    DEFAULT_COLORS = {
        # Background colors
        "content_bg": "#FAF6F3",          # Light cream background for content area
        "sidebar_bg": "#2D2013",          # Dark brown background for sidebar
        "sidebar_header_bg": "#6B4226",   # Cacao brown header
        "card_bg": "#FFFFFF",             # White background for content cards
        
        # Text colors
        "title_color": "#6B4226",         # Cacao brown for titles
        "text_color": "#2D2013",          # Dark brown for text
        "sidebar_text": "#D6C3B6",        # Light brown text for sidebar
        "active_text": "#FFFFFF",         # White text for active items
        "app_title_color": "#D6C3B6",     # Light brown text for app title
        
        # Border colors
        "border_color": "#D6C3B6",        # Light brown border
        "card_border": "#E6D7CC",         # Very light brown border for cards
        "sidebar_border": "#503418",      # Medium brown border for sidebar sections
        
        # Interactive element colors
        "active_bg": "#D6C3B6",           # Light brown active background (was Cacao brown)
        "active_icon_bg": "#8B5E41",      # Slightly lighter brown for active icons
        "inactive_icon_bg": "rgba(107, 66, 38, 0.3)",  # Transparent brown for inactive icons
    }
    
    # Default spacing and sizing
    DEFAULT_SPACING = {
        "sidebar_width": "250px",         # Width of expanded sidebar
        "sidebar_collapsed_width": "64px", # Width of collapsed sidebar
        "content_padding": "24px 32px",   # Padding for content area
        "card_padding": "24px",           # Padding for content cards
        "nav_item_padding": "12px 16px",  # Padding for navigation items
    }
    
    # Default font settings
    DEFAULT_FONTS = {
        "title_size": "24px",             # Size for page titles
        "title_weight": "700",            # Font weight for titles
        "nav_item_size": "15px",          # Size for navigation items
        "nav_item_weight": "500",         # Font weight for navigation items
    }
    
    def __init__(self, 
                 colors: Optional[Dict[str, str]] = None,
                 spacing: Optional[Dict[str, str]] = None,
                 fonts: Optional[Dict[str, str]] = None):
        """
        Initialize a sidebar theme with customizable properties.
        
        Args:
            colors: Optional dictionary of color overrides
            spacing: Optional dictionary of spacing overrides
            fonts: Optional dictionary of font setting overrides
        """
        # Merge provided values with defaults
        self.colors = {**self.DEFAULT_COLORS, **(colors or {})}
        self.spacing = {**self.DEFAULT_SPACING, **(spacing or {})}
        self.fonts = {**self.DEFAULT_FONTS, **(fonts or {})}
    
    def get_all(self) -> Dict[str, Dict[str, str]]:
        """
        Get all theme properties as a dictionary.
        
        Returns:
            Dictionary containing all theme properties
        """
        return {
            "colors": self.colors,
            "spacing": self.spacing,
            "fonts": self.fonts
        }
    
    def get_css_variables(self) -> str:
        """
        Generate CSS variables for this theme.
        
        Returns:
            CSS string with variable definitions
        """
        css = ":root {\n"
        
        # Add color variables
        for key, value in self.colors.items():
            css += f"  --sidebar-{key}: {value};\n"
            
        # Add spacing variables
        for key, value in self.spacing.items():
            css += f"  --sidebar-{key}: {value};\n"
            
        # Add font variables
        for key, value in self.fonts.items():
            css += f"  --sidebar-{key}: {value};\n"
            
        css += "}\n"
        return css