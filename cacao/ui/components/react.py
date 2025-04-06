"""
React component integration for Cacao.
Provides a bridge to use React components from npm packages in Cacao applications.
"""

from typing import Any, Dict, List, Optional, Union
from .base import Component

class ReactComponent(Component):
    """
    A component that renders a React component from an npm package.
    
    This component creates a bridge between Cacao and React, allowing
    developers to use React components from npm packages in their Cacao apps.
    
    Usage:
        editor = ReactComponent(
            package="codemirror",
            component="CodeMirror",
            props={
                "value": "const hello = 'world';",
                "options": {
                    "mode": "javascript",
                    "theme": "material",
                    "lineNumbers": True
                }
            }
        )
    """
    
    def __init__(
        self, 
        package: str, 
        component: str, 
        props: Dict[str, Any] = None,
        version: str = "latest",
        css: Optional[List[str]] = None,
        cdn: str = "https://cdn.jsdelivr.net/npm",
        id: Optional[str] = None
    ):
        """
        Initialize a React component.
        
        Args:
            package: The npm package name (e.g., "codemirror")
            component: The React component name to use from the package
            props: Props to pass to the React component
            version: The package version to use (default: "latest")
            css: Optional list of CSS files to load from the package
            cdn: The CDN to use for loading the package (default: jsdelivr)
            id: Optional ID for the component container
        """
        super().__init__()
        self.package = package
        self.component = component
        self.props = props or {}
        self.version = version
        self.css = css or []
        self.cdn = cdn
        self.id = id or f"react-{package}-{component}-{id(self)}"
        
    def render(self) -> Dict[str, Any]:
        """Render the React component bridge."""
        return {
            "type": "react-component",
            "props": {
                "id": self.id,
                "package": self.package,
                "component": self.component,
                "props": self.props,
                "version": self.version,
                "css": self.css,
                "cdn": self.cdn
            }
        }