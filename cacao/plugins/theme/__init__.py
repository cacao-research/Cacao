"""
Theme system for Cacao documentation.
Provides a clean, modern default theme with Sphinx-like template inheritance.
"""

import os
from typing import Optional

class ThemeManager:
    """
    Manages theme loading and configuration.
    """
    def __init__(self):
        self._theme_dir = os.path.dirname(os.path.abspath(__file__))
        self._default_theme = "default"
        self._current_theme = None
        self._theme_options = {}
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the theme system."""
        if self._initialized:
            return

        # Ensure theme directories exist
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.static_dir, exist_ok=True)

        # Copy default theme files if needed
        if not os.path.exists(os.path.join(self.template_dir, 'layout.html')):
            print("[INFO] Setting up default theme templates...")

        self._initialized = True

    @property
    def current_theme(self) -> str:
        """Get the name of the currently active theme."""
        return self._current_theme or self._default_theme

    @current_theme.setter
    def current_theme(self, theme_name: str) -> None:
        """Set the current theme."""
        theme_path = os.path.join(self._theme_dir, theme_name)
        if not os.path.exists(theme_path):
            raise ValueError(f"Theme not found: {theme_name}")
        self._current_theme = theme_name
        self.initialize()

    @property
    def theme_options(self) -> dict:
        """Get the current theme options."""
        return self._theme_options

    @theme_options.setter
    def theme_options(self, options: dict) -> None:
        """Set the theme options."""
        self._theme_options = options

    @property
    def template_dir(self) -> str:
        """Get the template directory for the current theme."""
        return os.path.join(
            self._theme_dir,
            self.current_theme,
            "templates"
        )

    @property
    def static_dir(self) -> str:
        """Get the static assets directory for the current theme."""
        return os.path.join(
            self._theme_dir,
            self.current_theme,
            "static"
        )

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

# Global theme manager instance
theme_manager = ThemeManager()
