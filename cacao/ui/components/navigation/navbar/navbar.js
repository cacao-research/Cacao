/**
 * Navbar Component JavaScript
 * Handles rendering and interaction for navbar elements
 */

class NavbarRenderer {
    constructor(containerId, props = {}) {
        this.containerId = containerId;
        this.props = props;
        this.navbarElement = null;
        this.isCollapsed = false;
        this.mobileBreakpoint = 768;
        this.scrollThreshold = 100;
        this.lastScrollY = 0;
        this.isScrolled = false;
        this.resizeObserver = null;
        this.scrollTimeout = null;
        
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
        this.handleResponsive();
        this.handleScroll();
    }

    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        const navbar = this.createNavbar();
        container.innerHTML = '';
        container.appendChild(navbar);
        
        this.navbarElement = navbar;
    }

    createNavbar() {
        const navbar = document.createElement('nav');
        navbar.className = this.getNavbarClasses();
        navbar.setAttribute('role', 'navigation');
        navbar.setAttribute('aria-label', this.props.ariaLabel || 'Main navigation');

        // Create navbar container
        const navContainer = document.createElement('div');
        navContainer.className = 'navbar-container';

        // Create brand section
        if (this.props.brand) {
            const brandElement = this.createBrand();
            navContainer.appendChild(brandElement);
        }

        // Create toggle button for mobile
        const toggleButton = this.createToggleButton();
        navContainer.appendChild(toggleButton);

        // Create navigation items container
        const navItems = this.createNavItems();
        navContainer.appendChild(navItems);

        // Create actions section
        if (this.props.actions && this.props.actions.length > 0) {
            const actionsElement = this.createActions();
            navContainer.appendChild(actionsElement);
        }

        navbar.appendChild(navContainer);
        return navbar;
    }

    createBrand() {
        const brand = document.createElement('div');
        brand.className = 'navbar-brand';

        if (this.props.brand.logo) {
            const logo = document.createElement('img');
            logo.src = this.props.brand.logo;
            logo.alt = this.props.brand.alt || 'Logo';
            logo.className = 'navbar-logo';
            brand.appendChild(logo);
        }

        if (this.props.brand.text) {
            const text = document.createElement('span');
            text.textContent = this.props.brand.text;
            text.className = 'navbar-brand-text';
            brand.appendChild(text);
        }

        if (this.props.brand.url) {
            const link = document.createElement('a');
            link.href = this.props.brand.url;
            link.className = 'navbar-brand-link';
            link.appendChild(brand.cloneNode(true));
            brand.innerHTML = '';
            brand.appendChild(link);
        }

        return brand;
    }

    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'navbar-toggle';
        button.setAttribute('type', 'button');
        button.setAttribute('aria-label', 'Toggle navigation');
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('aria-controls', 'navbar-collapse');

        // Create hamburger icon
        const icon = document.createElement('span');
        icon.className = 'navbar-toggle-icon';
        icon.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;

        button.appendChild(icon);

        button.addEventListener('click', () => {
            this.toggleNavbar();
        });

        return button;
    }

    createNavItems() {
        const navCollapse = document.createElement('div');
        navCollapse.className = 'navbar-collapse';
        navCollapse.id = 'navbar-collapse';

        const navList = document.createElement('ul');
        navList.className = 'navbar-nav';

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const listItem = this.createNavItem(item);
                navList.appendChild(listItem);
            });
        }

        navCollapse.appendChild(navList);
        return navCollapse;
    }

    createNavItem(item) {
        const listItem = document.createElement('li');
        listItem.className = 'navbar-nav-item';

        if (item.dropdown && item.dropdown.length > 0) {
            // Create dropdown
            listItem.className += ' navbar-dropdown';
            const dropdownToggle = this.createDropdownToggle(item);
            const dropdownMenu = this.createDropdownMenu(item.dropdown);
            
            listItem.appendChild(dropdownToggle);
            listItem.appendChild(dropdownMenu);
        } else {
            // Create regular nav item
            const link = document.createElement('a');
            link.href = item.url || '#';
            link.className = 'navbar-nav-link';
            link.textContent = item.text;

            if (item.active) {
                link.className += ' navbar-nav-active';
            }

            if (item.disabled) {
                link.className += ' navbar-nav-disabled';
                link.setAttribute('aria-disabled', 'true');
            }

            if (item.icon) {
                const icon = document.createElement('i');
                icon.className = `navbar-nav-icon ${item.icon}`;
                link.insertBefore(icon, link.firstChild);
            }

            listItem.appendChild(link);
        }

        return listItem;
    }

    createDropdownToggle(item) {
        const toggle = document.createElement('button');
        toggle.className = 'navbar-dropdown-toggle';
        toggle.textContent = item.text;
        toggle.setAttribute('aria-haspopup', 'true');
        toggle.setAttribute('aria-expanded', 'false');

        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `navbar-nav-icon ${item.icon}`;
            toggle.insertBefore(icon, toggle.firstChild);
        }

        const caret = document.createElement('i');
        caret.className = 'navbar-dropdown-caret';
        toggle.appendChild(caret);

        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleDropdown(toggle);
        });

        return toggle;
    }

    createDropdownMenu(items) {
        const menu = document.createElement('ul');
        menu.className = 'navbar-dropdown-menu';
        menu.setAttribute('role', 'menu');

        items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.className = 'navbar-dropdown-item';

            if (item.divider) {
                listItem.className += ' navbar-dropdown-divider';
            } else {
                const link = document.createElement('a');
                link.href = item.url || '#';
                link.className = 'navbar-dropdown-link';
                link.textContent = item.text;
                link.setAttribute('role', 'menuitem');

                if (item.icon) {
                    const icon = document.createElement('i');
                    icon.className = `navbar-dropdown-icon ${item.icon}`;
                    link.insertBefore(icon, link.firstChild);
                }

                listItem.appendChild(link);
            }

            menu.appendChild(listItem);
        });

        return menu;
    }

    createActions() {
        const actions = document.createElement('div');
        actions.className = 'navbar-actions';

        this.props.actions.forEach(action => {
            const button = document.createElement('button');
            button.className = `navbar-action ${action.variant || 'default'}`;
            button.textContent = action.text;

            if (action.icon) {
                const icon = document.createElement('i');
                icon.className = `navbar-action-icon ${action.icon}`;
                button.insertBefore(icon, button.firstChild);
            }

            if (action.onClick) {
                button.addEventListener('click', action.onClick);
            }

            actions.appendChild(button);
        });

        return actions;
    }

    getNavbarClasses() {
        let classes = 'navbar';

        if (this.props.variant) {
            classes += ` navbar-${this.props.variant}`;
        }

        if (this.props.position) {
            classes += ` navbar-${this.props.position}`;
        }

        if (this.props.transparent) {
            classes += ' navbar-transparent';
        }

        if (this.props.shadow) {
            classes += ' navbar-shadow';
        }

        if (this.props.sticky) {
            classes += ' navbar-sticky';
        }

        if (this.isScrolled) {
            classes += ' navbar-scrolled';
        }

        if (this.isCollapsed) {
            classes += ' navbar-collapsed';
        }

        return classes;
    }

    toggleNavbar() {
        this.isCollapsed = !this.isCollapsed;
        const toggle = this.navbarElement.querySelector('.navbar-toggle');
        const collapse = this.navbarElement.querySelector('.navbar-collapse');

        if (this.isCollapsed) {
            this.navbarElement.classList.add('navbar-collapsed');
            toggle.setAttribute('aria-expanded', 'true');
            collapse.style.maxHeight = collapse.scrollHeight + 'px';
        } else {
            this.navbarElement.classList.remove('navbar-collapsed');
            toggle.setAttribute('aria-expanded', 'false');
            collapse.style.maxHeight = '0';
        }
    }

    toggleDropdown(toggle) {
        const menu = toggle.nextElementSibling;
        const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

        // Close all other dropdowns
        const allDropdowns = this.navbarElement.querySelectorAll('.navbar-dropdown-toggle');
        allDropdowns.forEach(dropdown => {
            if (dropdown !== toggle) {
                dropdown.setAttribute('aria-expanded', 'false');
                dropdown.parentElement.classList.remove('navbar-dropdown-open');
            }
        });

        // Toggle current dropdown
        toggle.setAttribute('aria-expanded', !isExpanded);
        toggle.parentElement.classList.toggle('navbar-dropdown-open');
    }

    handleResponsive() {
        const checkWidth = () => {
            const width = window.innerWidth;
            if (width >= this.mobileBreakpoint) {
                this.isCollapsed = false;
                this.navbarElement.classList.remove('navbar-collapsed');
                const collapse = this.navbarElement.querySelector('.navbar-collapse');
                collapse.style.maxHeight = '';
            }
        };

        window.addEventListener('resize', checkWidth);
        checkWidth();
    }

    handleScroll() {
        if (!this.props.sticky) return;

        const handleScrollEvent = () => {
            const currentScrollY = window.scrollY;
            const scrolledPastThreshold = currentScrollY > this.scrollThreshold;

            if (scrolledPastThreshold !== this.isScrolled) {
                this.isScrolled = scrolledPastThreshold;
                this.updateScrollClasses();
            }

            this.lastScrollY = currentScrollY;
        };

        window.addEventListener('scroll', handleScrollEvent);
        handleScrollEvent();
    }

    updateScrollClasses() {
        if (this.isScrolled) {
            this.navbarElement.classList.add('navbar-scrolled');
        } else {
            this.navbarElement.classList.remove('navbar-scrolled');
        }
    }

    setupEventListeners() {
        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar-dropdown')) {
                const dropdowns = this.navbarElement.querySelectorAll('.navbar-dropdown-toggle');
                dropdowns.forEach(dropdown => {
                    dropdown.setAttribute('aria-expanded', 'false');
                    dropdown.parentElement.classList.remove('navbar-dropdown-open');
                });
            }
        });

        // Handle keyboard navigation
        this.navbarElement.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Close all dropdowns
                const dropdowns = this.navbarElement.querySelectorAll('.navbar-dropdown-toggle');
                dropdowns.forEach(dropdown => {
                    dropdown.setAttribute('aria-expanded', 'false');
                    dropdown.parentElement.classList.remove('navbar-dropdown-open');
                });
            }
        });
    }

    updateProps(newProps) {
        this.props = { ...this.props, ...newProps };
        this.render();
    }

    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        
        if (this.scrollTimeout) {
            clearTimeout(this.scrollTimeout);
        }
        
        // Remove event listeners
        window.removeEventListener('resize', this.handleResponsive);
        window.removeEventListener('scroll', this.handleScroll);
    }
}

// Export for use in other components
window.NavbarRenderer = NavbarRenderer;