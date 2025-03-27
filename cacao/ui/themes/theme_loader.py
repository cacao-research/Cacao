"""
Theme loader module for the Cacao framework.
Handles injection of CSS and JS assets into the frontend.
"""

import os
from typing import Dict

def load_theme(theme_name: str, base_path: str = None) -> Dict[str, str]:
    """
    Loads theme assets for the given theme name.
    
    Returns:
        A dictionary with 'css' and 'js' keys containing the theme's CSS and JS.
    """
    base_path = base_path or os.path.join(os.path.dirname(__file__), "themes")
    css_file = os.path.join(base_path, f"{theme_name}.css")
    js_file = os.path.join(base_path, f"{theme_name}.js")
    
    assets = {"css": "", "js": ""}
    
    try:
        with open(css_file, "r", encoding="utf-8") as f:
            assets["css"] = f.read()
    except FileNotFoundError:
        pass

    try:
        with open(js_file, "r", encoding="utf-8") as f:
            assets["js"] = f.read()
    except FileNotFoundError:
        pass

    return assets
