"""
Data components package for the Cacao framework.
Contains all data display components migrated from the monolithic data.py file.
"""


# Import migrated components from their new locations
from .table.table import Table
from .plot.plot import Plot
from .list.list import List
from .descriptions.descriptions import Descriptions
from .tooltip.tooltip import Tooltip
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