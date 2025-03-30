"""
Icon registry system for Cacao.
Provides a centralized registry for SVG icons and FontAwesome references.
"""

import os
import re
import json
from typing import Dict, Optional, Union, List, Tuple
from pathlib import Path
import xml.etree.ElementTree as ET
from functools import lru_cache

from .cache import cache

# Regex pattern for icon placeholders
# Matches {%icon-prefix-name%} or {% icon-prefix-name %} with optional parameters
# Examples: {%icon-ca-home%}, {% icon-fa-user %}, {%icon-fa-check size=16 color=#ff0000%}
ICON_PATTERN = re.compile(r'\{%\s*icon-([a-z]{2})-([a-zA-Z0-9_-]+)(?:\s+([^%]*))?%\}')

class IconRegistry:
    """
    Central registry for icons in Cacao applications.
    
    Handles registration, retrieval, and rendering of both custom SVG icons
    and FontAwesome references. Icons can be used in content via {%icon-prefix-name%}
    syntax.
    
    Usage:
        # Initialize the registry
        icon_registry = IconRegistry()
        
        # Register a custom icon
        icon_registry.register_icon("home", "<svg>...</svg>")
        
        # Use in content
        return {
            "type": "h1",
            "props": {
                "content": "Welcome Home {%icon-ca-home%}"
            }
        }
    """
    
    def __init__(self):
        self._custom_icons: Dict[str, str] = {}
        self._config: Dict = {}
        self._fontawesome_version: str = "6.4.2"
        self._fontawesome_mode: str = "free"  # or "pro"
        self._custom_icon_dirs: List[str] = []
        self._auto_load_completed = False
        
    def initialize(self, config: Optional[Dict] = None) -> None:
        """
        Initialize the icon registry with configuration settings.
        
        Args:
            config: Icon configuration dictionary, typically from cacao.json
        """
        if config:
            self._config = config
            
            # Set FontAwesome version and mode if provided
            self._fontawesome_version = config.get("fontawesome_version", self._fontawesome_version)
            self._fontawesome_mode = config.get("fontawesome_mode", self._fontawesome_mode)
            
            # Set custom icon directories
            icon_dirs = config.get("icon_directories", [])
            if isinstance(icon_dirs, list):
                self._custom_icon_dirs = icon_dirs
        
        # Auto-load icons from configured directories
        self._auto_load_icons()
    
    def _auto_load_icons(self) -> None:
        """Load icons from configured directories and package static directory automatically."""
        if self._auto_load_completed:
            return

        # First check package static icons directory
        package_icons_dir = self._get_package_icons_dir()
        if package_icons_dir:
            self.load_icons_from_directory(package_icons_dir)
            
        # Then check configured directories
        for directory in self._custom_icon_dirs:
            if not os.path.isdir(directory):
                continue
                
            self.load_icons_from_directory(directory)
        
        self._auto_load_completed = True
    
    def _get_package_icons_dir(self) -> Optional[str]:
        """Get the path to the package's static/icons directory."""
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construct path to static/icons directory
        icons_dir = os.path.join(current_dir, 'core', 'static', 'icons')
        
        if os.path.isdir(icons_dir):
            return icons_dir
        return None
    
    def load_icons_from_directory(self, directory: str) -> int:
        """
        Load all SVG files from a directory as icons.
        
        Args:
            directory: Path to directory containing SVG files
            
        Returns:
            Number of icons loaded
        """
        count = 0
        path = Path(directory)
        
        if not path.exists() or not path.is_dir():
            return 0
            
        for svg_file in path.glob("*.svg"):
            try:
                icon_name = svg_file.stem
                with open(svg_file, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                    
                self.register_icon(icon_name, svg_content)
                count += 1
            except Exception as e:
                print(f"Error loading icon {svg_file}: {str(e)}")
                
        return count
    
    def register_icon(self, name: str, svg_content: str) -> bool:
        """
        Register a custom SVG icon.
        
        Args:
            name: Icon name (without prefix)
            svg_content: SVG markup content
            
        Returns:
            True if registration was successful
        """
        try:
            # Validate SVG content
            ET.fromstring(svg_content)
            
            # Store the icon
            self._custom_icons[name] = svg_content
            return True
        except Exception as e:
            print(f"Error registering icon {name}: {str(e)}")
            return False
    
    def register_icon_from_file(self, name: str, file_path: str) -> bool:
        """
        Register a custom SVG icon from a file.
        
        Args:
            name: Icon name (without prefix)
            file_path: Path to SVG file
            
        Returns:
            True if registration was successful
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            return self.register_icon(name, svg_content)
        except Exception as e:
            print(f"Error registering icon from file {file_path}: {str(e)}")
            return False
    
    @cache
    def get_icon(self, prefix: str, name: str, params: Optional[str] = None) -> str:
        """
        Get HTML for an icon by prefix and name.
        
        Args:
            prefix: Icon prefix ('ca' for custom, 'fa' for FontAwesome)
            name: Icon name
            params: Optional parameters string (e.g., 'size=16 color=#ff0000')
            
        Returns:
            HTML representation of the icon
        """
        if prefix == 'ca':
            return self._get_custom_icon(name, params)
        elif prefix == 'fa':
            return self._get_fontawesome_icon(name, params)
        else:
            return f"<span class='icon-error'>Unknown icon prefix: {prefix}</span>"
    
    def _get_custom_icon(self, name: str, params: Optional[str] = None) -> str:
        """Get a custom SVG icon with applied parameters."""
        if name not in self._custom_icons:
            return f"<span class='icon-error'>Icon not found: {name}</span>"
            
        svg = self._custom_icons[name]
        
        # Apply parameters if provided
        if params:
            parsed_params = self._parse_params(params)
            svg = self._apply_params_to_svg(svg, parsed_params)
        
        # Wrap SVG in a span for consistent rendering
        return f"<span class='cacao-icon'>{svg}</span>"
    
    def _get_fontawesome_icon(self, name: str, params: Optional[str] = None) -> str:
        """Get a FontAwesome icon with applied parameters."""
        # Parse parameters
        parsed_params = self._parse_params(params) if params else {}
        
        # Default class and styles
        classes = ["fa", f"fa-{name}"]
        style = ""
        
        # Extract style and class parameters
        if "class" in parsed_params:
            classes.append(parsed_params["class"])
            del parsed_params["class"]
            
        if "size" in parsed_params:
            size = parsed_params["size"]
            style += f"font-size:{size}px;"
            del parsed_params["size"]
            
        if "color" in parsed_params:
            color = parsed_params["color"]
            style += f"color:{color};"
            del parsed_params["color"]
        
        # Add additional style parameters
        for key, value in parsed_params.items():
            if key.startswith("style-"):
                style_prop = key.replace("style-", "")
                style += f"{style_prop}:{value};"
            else:
                # Add as a data attribute
                classes.append(f"data-{key}=\"{value}\"")
        
        # Build the icon HTML
        class_attr = " ".join(classes)
        style_attr = f" style=\"{style}\"" if style else ""
        
        return f"<span class='cacao-icon'><i class=\"{class_attr}\"{style_attr}></i></span>"
    
    def _parse_params(self, params_str: str) -> Dict[str, str]:
        """Parse a parameter string into a dictionary."""
        params = {}
        
        if not params_str:
            return params
            
        # Split by space, handling quoted values
        parts = re.findall(r'([a-zA-Z0-9_-]+)=(?:"([^"]*)"|\'([^\']*)\'|([^\s]*))', params_str)
        
        for match in parts:
            key = match[0]
            # Get the first non-empty value from the capture groups
            value = next((v for v in match[1:] if v), "")
            params[key] = value
            
        return params
    
    def _apply_params_to_svg(self, svg: str, params: Dict[str, str]) -> str:
        """Apply parameters to an SVG string."""
        try:
            # Clean SVG string to ensure it's properly formatted
            svg = svg.strip()
            
            root = ET.fromstring(svg)
            
            # Force necessary attributes for proper rendering
            root.set("xmlns", "http://www.w3.org/2000/svg")
            
            # Set inline display to ensure proper rendering in HTML
            root.set("style", "display:inline-block;vertical-align:middle")
            
            # Apply width and height if provided
            if "size" in params:
                size = params["size"]
                root.set("width", size)
                root.set("height", size)
            else:
                # Ensure width and height are set
                if "width" not in root.attrib:
                    root.set("width", "24")
                if "height" not in root.attrib:
                    root.set("height", "24")
                
            # Apply color if provided
            if "color" in params:
                color = params["color"]
                # Apply color to the SVG element itself and all paths
                root.set("fill", color)
                # Also set fill attribute for all path elements
                for path in root.findall(".//{http://www.w3.org/2000/svg}path"):
                    if "fill" in path.attrib and path.attrib["fill"] != "none":
                        path.set("fill", color)
            
            # Apply other style parameters
            for key, value in params.items():
                if key.startswith("style-"):
                    style_prop = key.replace("style-", "")
                    root.set(style_prop, value)
            
            # Convert back to string with proper namespace handling
            svg_str = ET.tostring(root, encoding='unicode')
            
            # Ensure the svg tag is properly formatted for inline use
            svg_str = svg_str.replace('ns0:', '').replace(':ns0', '')
            return svg_str
        except Exception as e:
            print(f"Error applying parameters to SVG: {str(e)}")
            return svg
    
    def process_content(self, content: str) -> str:
        """
        Process content string to replace icon placeholders.
        
        Args:
            content: Content string with potential icon placeholders
            
        Returns:
            Processed content with icons replaced
        """
        if not content or ("{%icon-" not in content and "{% icon-" not in content):
            return content
            
        def replace_icon(match):
            prefix = match.group(1)
            name = match.group(2)
            params = match.group(3)
            
            icon_html = self.get_icon(prefix, name, params)
            return icon_html
            
        result = ICON_PATTERN.sub(replace_icon, content)
        return result
    
    def get_all_icon_names(self) -> Dict[str, List[str]]:
        """
        Get all registered icon names grouped by prefix.
        
        Returns:
            Dictionary with prefix keys and lists of icon names
        """
        return {
            "ca": list(self._custom_icons.keys()),
            "fa": []  # FontAwesome icons are not stored but referenced
        }
    
    def clear_cache(self) -> None:
        """Clear the icon cache."""
        # Clear the lru_cache of the get_icon method
        self.get_icon.cache_clear()

# Create global icon registry instance
icon_registry = IconRegistry()

def process_icons_in_component(component: Dict) -> Dict:
    """
    Process all content in a component and its children to replace icon placeholders.
    Process all components except "pre" tags to allow for raw content display.
    
    Args:
        component: Component dictionary
        
    Returns:
        Processed component dictionary
    """
    if not isinstance(component, dict):
        return component
    
    # Deep copy to avoid modifying the original
    processed = component.copy()
    
    # Process content property in props if it exists and component is not a pre tag
    if "props" in processed and isinstance(processed["props"], dict):
        props = processed["props"]
        
        # Process "content" property if present and not in "pre" tag
        if "content" in props and isinstance(props["content"], str) and processed.get("type") != "pre":
            props["content"] = icon_registry.process_content(props["content"])
    
    # Process "children" property recursively if it exists in props
    if "props" in processed and isinstance(processed["props"], dict) and "children" in processed["props"] and isinstance(processed["props"]["children"], list):
        processed["props"]["children"] = [process_icons_in_component(child) for child in processed["props"]["children"]]
    
    # Also process direct "children" property if it exists (for top-level components)
    if "children" in processed and isinstance(processed["children"], list):
        processed["children"] = [process_icons_in_component(child) for child in processed["children"]]
    
    # For icon specifically in the sidebar layout nav items
    if "icon" in processed and isinstance(processed["icon"], str):
        processed["icon"] = icon_registry.process_content(processed["icon"])
    
    return processed