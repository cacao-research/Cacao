/**
 * Menu Component JavaScript
 * Handles menu rendering, navigation, and interactions
 */

class MenuRenderer {
    constructor(containerId, props = {}) {
        this.containerId = containerId;
        this.props = props;
        this.menuElement = null;
        this.openSubmenus = new Set();
        this.focusedItem = null;
        this.keydownHandler = null;
        
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
        this.setupKeyboardNavigation();
    }

    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        const menu = this.createMenu();
        container.innerHTML = '';
        container.appendChild(menu);
        
        this.menuElement = menu;
    }

    createMenu() {
        const menu = document.createElement('ul');
        menu.className = this.getMenuClasses();
        menu.setAttribute('role', 'menu');
        menu.setAttribute('aria-orientation', this.props.orientation || 'vertical');

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const menuItem = this.createMenuItem(item);
                menu.appendChild(menuItem);
            });
        }

        return menu;
    }

    createMenuItem(item) {
        const listItem = document.createElement('li');
        listItem.className = this.getMenuItemClasses(item);
        listItem.setAttribute('role', 'none');

        if (item.children && item.children.length > 0) {
            // Create submenu
            const submenuToggle = this.createSubmenuToggle(item);
            const submenu = this.createSubmenu(item);
            
            listItem.appendChild(submenuToggle);
            listItem.appendChild(submenu);
        } else {
            // Create regular menu item
            const menuLink = this.createMenuLink(item);
            listItem.appendChild(menuLink);
        }

        return listItem;
    }

    createMenuLink(item) {
        const element = document.createElement(item.url ? 'a' : 'button');
        element.className = 'menu-link';
        element.setAttribute('role', 'menuitem');
        element.setAttribute('tabindex', '-1');

        if (item.url) {
            element.href = item.url;
        } else {
            element.type = 'button';
        }

        if (item.disabled) {
            element.setAttribute('aria-disabled', 'true');
            element.setAttribute('disabled', 'true');
        }

        if (item.active) {
            element.setAttribute('aria-current', 'page');
        }

        // Create link content
        const linkContent = document.createElement('div');
        linkContent.className = 'menu-link-content';

        // Add icon if present
        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `menu-icon ${item.icon}`;
            linkContent.appendChild(icon);
        }

        // Add label
        const label = document.createElement('span');
        label.className = 'menu-label';
        label.textContent = item.label;
        linkContent.appendChild(label);

        // Add badge if present
        if (item.badge !== undefined && item.badge !== null) {
            const badge = document.createElement('span');
            badge.className = 'menu-badge';
            badge.textContent = item.badge;
            linkContent.appendChild(badge);
        }

        element.appendChild(linkContent);

        // Add click handler
        element.addEventListener('click', (e) => {
            this.handleItemClick(e, item);
        });

        return element;
    }

    createSubmenuToggle(item) {
        const button = document.createElement('button');
        button.className = 'menu-submenu-toggle';
        button.setAttribute('role', 'menuitem');
        button.setAttribute('aria-haspopup', 'true');
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('tabindex', '-1');

        if (item.disabled) {
            button.setAttribute('aria-disabled', 'true');
            button.setAttribute('disabled', 'true');
        }

        // Create toggle content
        const toggleContent = document.createElement('div');
        toggleContent.className = 'menu-submenu-toggle-content';

        // Add icon if present
        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `menu-icon ${item.icon}`;
            toggleContent.appendChild(icon);
        }

        // Add label
        const label = document.createElement('span');
        label.className = 'menu-label';
        label.textContent = item.label;
        toggleContent.appendChild(label);

        // Add badge if present
        if (item.badge !== undefined && item.badge !== null) {
            const badge = document.createElement('span');
            badge.className = 'menu-badge';
            badge.textContent = item.badge;
            toggleContent.appendChild(badge);
        }

        // Add arrow
        const arrow = document.createElement('i');
        arrow.className = 'menu-arrow';
        toggleContent.appendChild(arrow);

        button.appendChild(toggleContent);

        // Add click handler
        button.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleSubmenu(item.key, button);
        });

        return button;
    }

    createSubmenu(item) {
        const submenu = document.createElement('ul');
        submenu.className = 'menu-submenu';
        submenu.setAttribute('role', 'menu');
        submenu.setAttribute('aria-labelledby', item.key);

        if (item.children && item.children.length > 0) {
            item.children.forEach(child => {
                const childItem = this.createMenuItem(child);
                submenu.appendChild(childItem);
            });
        }

        return submenu;
    }

    getMenuClasses() {
        let classes = 'menu';

        if (this.props.orientation) {
            classes += ` menu-${this.props.orientation}`;
        }

        if (this.props.size) {
            classes += ` menu-${this.props.size}`;
        }

        if (this.props.variant) {
            classes += ` menu-${this.props.variant}`;
        }

        if (this.props.theme) {
            classes += ` menu-${this.props.theme}`;
        }

        if (this.props.collapsed) {
            classes += ' menu-collapsed';
        }

        return classes;
    }

    getMenuItemClasses(item) {
        let classes = 'menu-item';

        if (item.active) {
            classes += ' menu-item-active';
        }

        if (item.disabled) {
            classes += ' menu-item-disabled';
        }

        if (item.children && item.children.length > 0) {
            classes += ' menu-item-submenu';
            
            if (this.openSubmenus.has(item.key)) {
                classes += ' menu-item-submenu-open';
            }
        }

        return classes;
    }

    toggleSubmenu(key, button) {
        if (this.openSubmenus.has(key)) {
            this.closeSubmenu(key, button);
        } else {
            this.openSubmenu(key, button);
        }
    }

    openSubmenu(key, button) {
        this.openSubmenus.add(key);
        button.setAttribute('aria-expanded', 'true');
        button.parentElement.classList.add('menu-item-submenu-open');
    }

    closeSubmenu(key, button) {
        this.openSubmenus.delete(key);
        button.setAttribute('aria-expanded', 'false');
        button.parentElement.classList.remove('menu-item-submenu-open');
    }

    handleItemClick(event, item) {
        if (item.disabled) {
            event.preventDefault();
            return;
        }

        // Call click callback if provided
        if (this.props.on_click) {
            this.callCallback(this.props.on_click, { item, event });
        }

        // Handle active state
        if (!item.url) {
            event.preventDefault();
            this.setActiveItem(item.key);
        }
    }

    setActiveItem(key) {
        // Remove active class from all items
        const activeItems = this.menuElement.querySelectorAll('.menu-item-active');
        activeItems.forEach(item => {
            item.classList.remove('menu-item-active');
            const link = item.querySelector('.menu-link, .menu-submenu-toggle');
            if (link) {
                link.removeAttribute('aria-current');
            }
        });

        // Add active class to selected item
        const items = this.menuElement.querySelectorAll('.menu-item');
        items.forEach(item => {
            const link = item.querySelector('.menu-link, .menu-submenu-toggle');
            if (link && this.getItemKey(item) === key) {
                item.classList.add('menu-item-active');
                link.setAttribute('aria-current', 'page');
            }
        });
    }

    getItemKey(element) {
        // Extract key from the data or generate from content
        const link = element.querySelector('.menu-link, .menu-submenu-toggle');
        if (link) {
            const label = link.querySelector('.menu-label');
            return label ? label.textContent : '';
        }
        return '';
    }

    setupEventListeners() {
        // Close submenus when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.menuElement.contains(e.target)) {
                this.closeAllSubmenus();
            }
        });

        // Handle window resize for responsive behavior
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    setupKeyboardNavigation() {
        this.keydownHandler = (e) => {
            this.handleKeydown(e);
        };

        this.menuElement.addEventListener('keydown', this.keydownHandler);

        // Set up initial focus
        this.setupInitialFocus();
    }

    setupInitialFocus() {
        const firstItem = this.menuElement.querySelector('.menu-link, .menu-submenu-toggle');
        if (firstItem) {
            firstItem.setAttribute('tabindex', '0');
            this.focusedItem = firstItem;
        }
    }

    handleKeydown(e) {
        const focusableItems = Array.from(
            this.menuElement.querySelectorAll('.menu-link:not([disabled]), .menu-submenu-toggle:not([disabled])')
        );

        const currentIndex = focusableItems.indexOf(this.focusedItem);
        let newIndex = currentIndex;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                newIndex = currentIndex < focusableItems.length - 1 ? currentIndex + 1 : 0;
                break;

            case 'ArrowUp':
                e.preventDefault();
                newIndex = currentIndex > 0 ? currentIndex - 1 : focusableItems.length - 1;
                break;

            case 'ArrowRight':
                e.preventDefault();
                if (this.focusedItem.classList.contains('menu-submenu-toggle')) {
                    this.focusedItem.click();
                }
                break;

            case 'ArrowLeft':
                e.preventDefault();
                if (this.focusedItem.classList.contains('menu-submenu-toggle')) {
                    const key = this.getItemKey(this.focusedItem.parentElement);
                    if (this.openSubmenus.has(key)) {
                        this.closeSubmenu(key, this.focusedItem);
                    }
                }
                break;

            case 'Enter':
            case ' ':
                e.preventDefault();
                this.focusedItem.click();
                break;

            case 'Escape':
                e.preventDefault();
                this.closeAllSubmenus();
                break;
        }

        if (newIndex !== currentIndex) {
            this.moveFocus(focusableItems[newIndex]);
        }
    }

    moveFocus(newFocusItem) {
        if (this.focusedItem) {
            this.focusedItem.setAttribute('tabindex', '-1');
        }

        this.focusedItem = newFocusItem;
        this.focusedItem.setAttribute('tabindex', '0');
        this.focusedItem.focus();
    }

    closeAllSubmenus() {
        const submenuToggleButtons = this.menuElement.querySelectorAll('.menu-submenu-toggle');
        submenuToggleButtons.forEach(button => {
            const key = this.getItemKey(button.parentElement);
            if (this.openSubmenus.has(key)) {
                this.closeSubmenu(key, button);
            }
        });
    }

    handleResize() {
        // Handle responsive behavior if needed
        if (this.props.responsive) {
            const width = window.innerWidth;
            // Add responsive logic here
        }
    }

    callCallback(callback, data) {
        if (typeof callback === 'function') {
            callback(data);
        } else if (typeof callback === 'string') {
            try {
                const func = new Function('data', callback);
                func(data);
            } catch (e) {
                console.error('Error executing callback:', e);
            }
        }
    }

    updateProps(newProps) {
        this.props = { ...this.props, ...newProps };
        this.render();
    }

    collapse() {
        this.props.collapsed = true;
        this.menuElement.classList.add('menu-collapsed');
        this.closeAllSubmenus();
    }

    expand() {
        this.props.collapsed = false;
        this.menuElement.classList.remove('menu-collapsed');
    }

    destroy() {
        if (this.keydownHandler) {
            this.menuElement.removeEventListener('keydown', this.keydownHandler);
        }

        // Clean up event listeners
        window.removeEventListener('resize', this.handleResize);
    }
}

// Export for use in other components
window.MenuRenderer = MenuRenderer;