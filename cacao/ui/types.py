"""
UI Types Module

Common type definitions for UI components.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of component validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class ComponentState:
    """Represents the current state of a component."""
    id: str
    type: str
    props: Dict[str, Any] = field(default_factory=dict)
    css_classes: List[str] = field(default_factory=list)
    validation: Optional[ValidationResult] = None
    children: List[Any] = field(default_factory=list)
    
    def is_valid(self) -> bool:
        """Check if the component state is valid."""
        return self.validation is None or self.validation.is_valid
    
    def get_errors(self) -> List[str]:
        """Get validation errors."""
        return self.validation.errors if self.validation else []
    
    def get_warnings(self) -> List[str]:
        """Get validation warnings."""
        return self.validation.warnings if self.validation else []


@dataclass
class ComponentEvent:
    """Represents a component event."""
    type: str
    component_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[float] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            import time
            self.timestamp = time.time()


@dataclass
class ComponentTheme:
    """Theme configuration for components."""
    primary_color: str = "#1890ff"
    secondary_color: str = "#6c757d"
    success_color: str = "#52c41a"
    warning_color: str = "#faad14"
    error_color: str = "#ff4d4f"
    background_color: str = "#ffffff"
    text_color: str = "#333333"
    border_color: str = "#d9d9d9"
    border_radius: str = "4px"
    font_family: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    font_size: str = "14px"
    line_height: str = "1.5"
    
    def to_css_vars(self) -> Dict[str, str]:
        """Convert theme to CSS variables."""
        return {
            "--primary-color": self.primary_color,
            "--secondary-color": self.secondary_color,
            "--success-color": self.success_color,
            "--warning-color": self.warning_color,
            "--error-color": self.error_color,
            "--background-color": self.background_color,
            "--text-color": self.text_color,
            "--border-color": self.border_color,
            "--border-radius": self.border_radius,
            "--font-family": self.font_family,
            "--font-size": self.font_size,
            "--line-height": self.line_height,
        }