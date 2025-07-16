"""
Data module for UI components in the Cacao framework.
Provides backward compatibility imports for components that have been migrated to the new folder structure.
"""

# Import all components from the new data package for backward compatibility
from .data import (
    Table,
    Plot,
    List,
    Descriptions,
    Tooltip,
    Popover,
    Card,
    Carousel,
    Collapse,
    Image,
    Badge,
    Avatar,
    Tag,
    Timeline
)

# Export all components for backward compatibility
__all__ = [
    'Table',
    'Plot',
    'List',
    'Descriptions',
    'Tooltip',
    'Popover',
    'Card',
    'Carousel',
    'Collapse',
    'Image',
    'Badge',
    'Avatar',
    'Tag',
    'Timeline'
]
