"""
Default theme implementation for Cacao documentation.
"""

import os
from typing import Dict, Any, Optional
from ..theme_base import ThemeBase
from . import get_default_options

class DefaultTheme(ThemeBase):
    """
    Default theme implementation providing a clean, modern look.
    """
    def __init__(self):
        super().__init__()
        self.name = "default"
        self.description = "Clean, modern documentation theme"
        self._options = get_default_options()
        self._theme_dir = os.path.dirname(os.path.abspath(__file__))

    @property
    def template_dir(self) -> str:
        """Get the template directory."""
        return os.path.join(self._theme_dir, 'templates')

    @property
    def static_dir(self) -> str:
        """Get the static assets directory."""
        return os.path.join(self._theme_dir, 'static')

    def get_template_path(self, template: str) -> str:
        """
        Get the full path to a template file.
        
        Args:
            template: Template filename
            
        Returns:
            Full path to template
        """
        return os.path.join(self.template_dir, template)

    def get_static_path(self, filename: str) -> str:
        """
        Get the full path to a static asset file.
        
        Args:
            filename: Static file name
            
        Returns:
            Full path to static file
        """
        return os.path.join(self.static_dir, filename)

    def get_static_url(self, filename: str) -> str:
        """
        Get the URL for a static asset file.
        
        Args:
            filename: Static file name
            
        Returns:
            URL path to static file
        """
        return f"/_static/{filename}"

    def configure(self, options: Dict[str, Any]) -> None:
        """
        Configure theme options.
        
        Args:
            options: Theme options to set
        """
        self._options.update(options)

    def get_option(self, key: str, default: Any = None) -> Any:
        """
        Get a theme option value.
        
        Args:
            key: Option key
            default: Default value if key not found
            
        Returns:
            Option value
        """
        return self._options.get(key, default)

    def get_context(self) -> Dict[str, Any]:
        """
        Get theme context for templates.
        
        Returns:
            Theme context dictionary
        """
        return {
            'theme': {
                'name': self.name,
                'options': self._options,
                'get_static_url': self.get_static_url
            }
        }

    def render_template(self, template: str, context: Dict[str, Any]) -> str:
        """
        Render a template with context.
        
        Args:
            template: Template name
            context: Template context
            
        Returns:
            Rendered template
        """
        # Add theme context
        context.update(self.get_context())
        return super().render_template(template, context)

# Create global theme instance
default_theme = DefaultTheme()
