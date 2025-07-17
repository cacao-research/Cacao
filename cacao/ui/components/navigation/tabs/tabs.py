"""
Tabs Component

A tab navigation component that allows users to switch between different content panels.
Supports horizontal and vertical orientations, various sizes, and customizable styling.
"""

from typing import List, Dict, Any, Optional, Union
from cacao.ui.components.base import Component
from cacao.ui.types import ComponentState, ValidationResult


class Tabs(Component):
    """
    A tab navigation component for switching between content panels.
    
    Features:
    - Multiple tab items with content panels
    - Horizontal and vertical orientations
    - Various sizes and styling options
    - Keyboard navigation support
    - Disabled tabs
    - Custom icons and badges
    - Closable tabs
    - Animated transitions
    """
    
    def __init__(
        self,
        id: str,
        items: List[Dict[str, Any]] = None,
        active_key: Optional[str] = None,
        orientation: str = 'horizontal',
        size: str = 'medium',
        variant: str = 'default',
        animated: bool = True,
        closable: bool = False,
        centered: bool = False,
        show_add_button: bool = False,
        max_width: Optional[str] = None,
        on_change: Optional[str] = None,
        on_close: Optional[str] = None,
        on_add: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize a Tabs component.
        
        Args:
            id: Unique identifier for the component
            items: List of tab items with keys, labels, and content
            active_key: Key of the currently active tab
            orientation: Tab orientation ('horizontal' or 'vertical')
            size: Tab size ('small', 'medium', 'large')
            variant: Tab variant ('default', 'card', 'pill', 'underline')
            animated: Whether to animate tab transitions
            closable: Whether tabs can be closed
            centered: Whether to center the tabs
            show_add_button: Whether to show an add button
            max_width: Maximum width for the tab container
            on_change: JavaScript function to call when tab changes
            on_close: JavaScript function to call when tab closes
            on_add: JavaScript function to call when add button is clicked
        """
        super().__init__(id, **kwargs)
        
        self.items = items or []
        self.active_key = active_key
        self.orientation = orientation
        self.size = size
        self.variant = variant
        self.animated = animated
        self.closable = closable
        self.centered = centered
        self.show_add_button = show_add_button
        self.max_width = max_width
        self.on_change = on_change
        self.on_close = on_close
        self.on_add = on_add
        
        # Set default active key if not provided
        if not self.active_key and self.items:
            self.active_key = self.items[0].get('key')
        
        # Validate component
        self._validate_component()
    
    def _validate_component(self) -> ValidationResult:
        """Validate the tabs component configuration."""
        errors = []
        
        # Validate orientation
        valid_orientations = ['horizontal', 'vertical']
        if self.orientation not in valid_orientations:
            errors.append(f"Invalid orientation: {self.orientation}. Must be one of: {valid_orientations}")
        
        # Validate size
        valid_sizes = ['small', 'medium', 'large']
        if self.size not in valid_sizes:
            errors.append(f"Invalid size: {self.size}. Must be one of: {valid_sizes}")
        
        # Validate variant
        valid_variants = ['default', 'card', 'pill', 'underline']
        if self.variant not in valid_variants:
            errors.append(f"Invalid variant: {self.variant}. Must be one of: {valid_variants}")
        
        # Validate items
        if not self.items:
            errors.append("Tabs must have at least one item")
        else:
            for i, item in enumerate(self.items):
                if not isinstance(item, dict):
                    errors.append(f"Item {i} must be a dictionary")
                    continue
                
                if 'key' not in item:
                    errors.append(f"Item {i} must have a 'key' field")
                
                if 'label' not in item:
                    errors.append(f"Item {i} must have a 'label' field")
        
        # Validate active key exists
        if self.active_key:
            item_keys = [item.get('key') for item in self.items]
            if self.active_key not in item_keys:
                errors.append(f"Active key '{self.active_key}' not found in items")
        
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
    
    def add_item(self, key: str, label: str, content: str = '', icon: str = None, 
                 badge: Union[str, int] = None, disabled: bool = False, 
                 closable: bool = None) -> 'Tabs':
        """
        Add a new tab item.
        
        Args:
            key: Unique key for the tab
            label: Display label for the tab
            content: Content to display in the tab panel
            icon: Icon class for the tab
            badge: Badge content to display
            disabled: Whether the tab is disabled
            closable: Whether this specific tab can be closed
        
        Returns:
            Self for method chaining
        """
        item = {
            'key': key,
            'label': label,
            'content': content,
            'disabled': disabled
        }
        
        if icon:
            item['icon'] = icon
        
        if badge is not None:
            item['badge'] = badge
        
        if closable is not None:
            item['closable'] = closable
        
        self.items.append(item)
        
        # Set as active if it's the first item
        if len(self.items) == 1:
            self.active_key = key
        
        return self
    
    def remove_item(self, key: str) -> 'Tabs':
        """
        Remove a tab item by key.
        
        Args:
            key: Key of the tab to remove
        
        Returns:
            Self for method chaining
        """
        self.items = [item for item in self.items if item.get('key') != key]
        
        # Update active key if removed item was active
        if self.active_key == key and self.items:
            self.active_key = self.items[0].get('key')
        elif not self.items:
            self.active_key = None
        
        return self
    
    def set_active(self, key: str) -> 'Tabs':
        """
        Set the active tab by key.
        
        Args:
            key: Key of the tab to make active
        
        Returns:
            Self for method chaining
        """
        item_keys = [item.get('key') for item in self.items]
        if key in item_keys:
            self.active_key = key
        
        return self
    
    def disable_item(self, key: str, disabled: bool = True) -> 'Tabs':
        """
        Enable or disable a tab item.
        
        Args:
            key: Key of the tab to modify
            disabled: Whether to disable the tab
        
        Returns:
            Self for method chaining
        """
        for item in self.items:
            if item.get('key') == key:
                item['disabled'] = disabled
                break
        
        return self
    
    def get_active_item(self) -> Optional[Dict[str, Any]]:
        """
        Get the currently active tab item.
        
        Returns:
            Active tab item or None if no active tab
        """
        if not self.active_key:
            return None
        
        for item in self.items:
            if item.get('key') == self.active_key:
                return item
        
        return None
    
    def get_enabled_items(self) -> List[Dict[str, Any]]:
        """
        Get all enabled tab items.
        
        Returns:
            List of enabled tab items
        """
        return [item for item in self.items if not item.get('disabled', False)]
    
    def update_state(self, **kwargs) -> 'Tabs':
        """
        Update component state with new values.
        
        Args:
            **kwargs: State updates
        
        Returns:
            Self for method chaining
        """
        if 'active_key' in kwargs:
            self.set_active(kwargs['active_key'])
        
        if 'items' in kwargs:
            self.items = kwargs['items']
        
        if 'orientation' in kwargs:
            self.orientation = kwargs['orientation']
        
        if 'size' in kwargs:
            self.size = kwargs['size']
        
        if 'variant' in kwargs:
            self.variant = kwargs['variant']
        
        if 'animated' in kwargs:
            self.animated = kwargs['animated']
        
        if 'closable' in kwargs:
            self.closable = kwargs['closable']
        
        if 'centered' in kwargs:
            self.centered = kwargs['centered']
        
        if 'show_add_button' in kwargs:
            self.show_add_button = kwargs['show_add_button']
        
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
            type='tabs',
            props={
                'items': self.items,
                'active_key': self.active_key,
                'orientation': self.orientation,
                'size': self.size,
                'variant': self.variant,
                'animated': self.animated,
                'closable': self.closable,
                'centered': self.centered,
                'show_add_button': self.show_add_button,
                'max_width': self.max_width,
                'on_change': self.on_change,
                'on_close': self.on_close,
                'on_add': self.on_add
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
        classes = ['tabs-container']
        
        if self.orientation:
            classes.append(f'tabs-{self.orientation}')
        
        if self.size:
            classes.append(f'tabs-{self.size}')
        
        if self.variant:
            classes.append(f'tabs-{self.variant}')
        
        if self.animated:
            classes.append('tabs-animated')
        
        if self.closable:
            classes.append('tabs-closable')
        
        if self.centered:
            classes.append('tabs-centered')
        
        if self.show_add_button:
            classes.append('tabs-has-add-button')
        
        return classes
    
    def compile(self) -> Dict[str, Any]:
        """
        Compile the component to a dictionary representation.
        
        Returns:
            Compiled component data
        """
        state = self.get_state()
        
        return {
            'type': 'tabs',
            'id': self.id,
            'props': state.props,
            'css_classes': state.css_classes,
            'validation': {
                'is_valid': state.validation.is_valid,
                'errors': state.validation.errors
            }
        }