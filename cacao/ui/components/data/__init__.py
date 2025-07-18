"""
Data components package for the Cacao framework.
Contains all data display components migrated from the monolithic data.py file.
"""

# Import the merged table component
from .table.table import (
    Table,
    create_simple_table,
    create_advanced_table,
    create_simple_datatable,
    create_server_side_datatable,
    create_export_datatable
)

# Import other components from their locations
from .plot.plot import Plot
from .list.list import List
from .descriptions.descriptions import Descriptions
from .tooltip.tooltip import Tooltip
from .tree_viewer.tree_viewer import TreeViewer
from .popover.popover import Popover
from .card.card import Card
from .carousel.carousel import Carousel
from .collapse.collapse import Collapse
from .image.image import Image
from .badge.badge import Badge
from .avatar.avatar import Avatar
from .tag.tag import Tag
from .timeline.timeline import Timeline

# Export all components for backward compatibility
__all__ = [
    # Merged table component (both simple and advanced)
    'Table',
    
    # Table factory functions
    'create_simple_table',
    'create_advanced_table',
    'create_simple_datatable',
    'create_server_side_datatable',
    'create_export_datatable',
    
    # Other data components
    'Plot',
    'List',
    'Descriptions',
    'Tooltip',
    'TreeViewer',
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