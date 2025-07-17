"""
Breadcrumb Component

A breadcrumb navigation component that shows the current page's location within 
a navigational hierarchy. Supports various separators, icons, and styling options.
"""

from typing import List, Dict, Any, Optional, Union
from cacao.ui.components.base import Component
from cacao.ui.types import ComponentState, ValidationResult


class Breadcrumb(Component):
    """
    A breadcrumb navigation component for showing hierarchical navigation paths.
    
    Features:
    - Customizable breadcrumb items with labels and URLs
    - Multiple separator styles (arrow, slash, dot, custom)
    - Icon support for breadcrumb items
    - Clickable and non-clickable items
    - Responsive design with overflow handling
    - Customizable styling and themes
    - Accessibility support with proper ARIA attributes
    """
    
    def __init__(
        self,
        id: str,
        items: List[Dict[str, Any]] = None,
        separator: str = 'arrow',
        separator_icon: Optional[str] = None,
        show_home: bool = True,
        home_url: str = '/',
        home_icon: str = 'home',
        max_items: Optional[int] = None,
        responsive: bool = True,
        size: str = 'medium',
        variant: str = 'default',
        on_click: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize a Breadcrumb component.
        
        Args:
            id: Unique identifier for the component
            items: List of breadcrumb items with labels and URLs
            separator: Type of separator ('arrow', 'slash', 'dot', 'custom')
            separator_icon: Custom icon for separator (when separator='custom')
            show_home: Whether to show a home icon at the beginning
            home_url: URL for the home link
            home_icon: Icon class for the home link
            max_items: Maximum number of items to show before collapsing
            responsive: Whether to enable responsive behavior
            size: Size of the breadcrumb ('small', 'medium', 'large')
            variant: Style variant ('default', 'outlined', 'ghost')
            on_click: JavaScript function to call when item is clicked
        """
        super().__init__(id, **kwargs)
        
        self.items = items or []
        self.separator = separator
        self.separator_icon = separator_icon
        self.show_home = show_home
        self.home_url = home_url
        self.home_icon = home_icon
        self.max_items = max_items
        self.responsive = responsive
        self.size = size
        self.variant = variant
        self.on_click = on_click
        
        # Validate component
        self._validate_component()
    
    def _validate_component(self) -> ValidationResult:
        """Validate the breadcrumb component configuration."""
        errors = []
        
        # Validate separator
        valid_separators = ['arrow', 'slash', 'dot', 'custom']
        if self.separator not in valid_separators:
            errors.append(f"Invalid separator: {self.separator}. Must be one of: {valid_separators}")
        
        # Validate custom separator icon
        if self.separator == 'custom' and not self.separator_icon:
            errors.append("Custom separator requires separator_icon to be specified")
        
        # Validate size
        valid_sizes = ['small', 'medium', 'large']
        if self.size not in valid_sizes:
            errors.append(f"Invalid size: {self.size}. Must be one of: {valid_sizes}")
        
        # Validate variant
        valid_variants = ['default', 'outlined', 'ghost']
        if self.variant not in valid_variants:
            errors.append(f"Invalid variant: {self.variant}. Must be one of: {valid_variants}")
        
        # Validate items
        if self.items:
            for i, item in enumerate(self.items):
                if not isinstance(item, dict):
                    errors.append(f"Item {i} must be a dictionary")
                    continue
                
                if 'label' not in item:
                    errors.append(f"Item {i} must have a 'label' field")
        
        # Validate max_items
        if self.max_items is not None and self.max_items < 1:
            errors.append("max_items must be at least 1")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
    
    def add_item(self, label: str, url: str = None, icon: str = None, 
                 active: bool = False, disabled: bool = False) -> 'Breadcrumb':
        """
        Add a new breadcrumb item.
        
        Args:
            label: Display label for the item
            url: URL for the item (if clickable)
            icon: Icon class for the item
            active: Whether this is the current/active item
            disabled: Whether the item is disabled
        
        Returns:
            Self for method chaining
        """
        item = {
            'label': label,
            'active': active,
            'disabled': disabled
        }
        
        if url:
            item['url'] = url
        
        if icon:
            item['icon'] = icon
        
        self.items.append(item)
        return self
    
    def remove_item(self, index: int) -> 'Breadcrumb':
        """
        Remove a breadcrumb item by index.
        
        Args:
            index: Index of the item to remove
        
        Returns:
            Self for method chaining
        """
        if 0 <= index < len(self.items):
            self.items.pop(index)
        
        return self
    
    def set_active_item(self, index: int) -> 'Breadcrumb':
        """
        Set an item as active (current page).
        
        Args:
            index: Index of the item to make active
        
        Returns:
            Self for method chaining
        """
        for i, item in enumerate(self.items):
            item['active'] = (i == index)
        
        return self
    
    def clear_items(self) -> 'Breadcrumb':
        """
        Clear all breadcrumb items.
        
        Returns:
            Self for method chaining
        """
        self.items = []
        return self
    
    def get_active_item(self) -> Optional[Dict[str, Any]]:
        """
        Get the currently active breadcrumb item.
        
        Returns:
            Active item or None if no active item
        """
        for item in self.items:
            if item.get('active'):
                return item
        return None
    
    def get_clickable_items(self) -> List[Dict[str, Any]]:
        """
        Get all clickable breadcrumb items.
        
        Returns:
            List of clickable items
        """
        return [item for item in self.items if item.get('url') and not item.get('disabled')]
    
    def get_visible_items(self) -> List[Dict[str, Any]]:
        """
        Get the items that should be visible based on max_items setting.
        
        Returns:
            List of visible items
        """
        if not self.max_items or len(self.items) <= self.max_items:
            return self.items
        
        # Show first item, ellipsis, and last (max_items - 1) items
        if self.max_items <= 2:
            return self.items[-self.max_items:]
        
        visible_items = []
        
        # Add first item
        if self.items:
            visible_items.append(self.items[0])
        
        # Add ellipsis if needed
        if len(self.items) > self.max_items:
            visible_items.append({'label': '...', 'ellipsis': True})
        
        # Add last (max_items - 2) items
        start_index = len(self.items) - (self.max_items - 2)
        visible_items.extend(self.items[start_index:])
        
        return visible_items
    
    def get_separator_display(self) -> str:
        """
        Get the display string/icon for the separator.
        
        Returns:
            Separator display string or icon class
        """
        if self.separator == 'custom':
            return self.separator_icon or '/'
        
        separator_map = {
            'arrow': '→',
            'slash': '/',
            'dot': '•'
        }
        
        return separator_map.get(self.separator, '/')
    
    def update_state(self, **kwargs) -> 'Breadcrumb':
        """
        Update component state with new values.
        
        Args:
            **kwargs: State updates
        
        Returns:
            Self for method chaining
        """
        if 'items' in kwargs:
            self.items = kwargs['items']
        
        if 'separator' in kwargs:
            self.separator = kwargs['separator']
        
        if 'separator_icon' in kwargs:
            self.separator_icon = kwargs['separator_icon']
        
        if 'show_home' in kwargs:
            self.show_home = kwargs['show_home']
        
        if 'home_url' in kwargs:
            self.home_url = kwargs['home_url']
        
        if 'home_icon' in kwargs:
            self.home_icon = kwargs['home_icon']
        
        if 'max_items' in kwargs:
            self.max_items = kwargs['max_items']
        
        if 'responsive' in kwargs:
            self.responsive = kwargs['responsive']
        
        if 'size' in kwargs:
            self.size = kwargs['size']
        
        if 'variant' in kwargs:
            self.variant = kwargs['variant']
        
        self._validate_component()
        return self
    
    def get_state(self) -> ComponentState:
        """
        Get the current component state.
        
        Returns:
            Current component state
        """
        return ComponentState(
            id=self.id,
            type='breadcrumb',
            props={
                'items': self.items,
                'separator': self.separator,
                'separator_icon': self.separator_icon,
                'show_home': self.show_home,
                'home_url': self.home_url,
                'home_icon': self.home_icon,
                'max_items': self.max_items,
                'responsive': self.responsive,
                'size': self.size,
                'variant': self.variant,
                'on_click': self.on_click
            },
            css_classes=self.get_css_classes(),
            validation=self._validate_component()
        )
    
    def get_css_classes(self) -> List[str]:
        """
        Get CSS classes for the component.
        
        Returns:
            List of CSS classes
        """
        classes = ['breadcrumb-container']
        
        if self.separator:
            classes.append(f'breadcrumb-separator-{self.separator}')
        
        if self.size:
            classes.append(f'breadcrumb-{self.size}')
        
        if self.variant:
            classes.append(f'breadcrumb-{self.variant}')
        
        if self.responsive:
            classes.append('breadcrumb-responsive')
        
        if self.show_home:
            classes.append('breadcrumb-has-home')
        
        return classes
    
    def compile(self) -> Dict[str, Any]:
        """
        Compile the component to a dictionary representation.
        
        Returns:
            Compiled component data
        """
        state = self.get_state()
        
        return {
            'type': 'breadcrumb',
            'id': self.id,
            'props': state.props,
            'css_classes': state.css_classes,
            'validation': {
                'is_valid': state.validation.is_valid,
                'errors': state.validation.errors
            }
        }