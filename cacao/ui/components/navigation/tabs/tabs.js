/**
 * Tabs Component JavaScript
 * Handles tab switching, animations, and user interactions
 */

class TabsRenderer {
    constructor(containerId, props = {}) {
        this.containerId = containerId;
        this.props = props;
        this.tabsElement = null;
        this.activeKey = props.active_key || null;
        this.animationDuration = 300;
        this.resizeObserver = null;
        this.keyboardHandlers = new Map();
        
        this.init();
    }

    init() {
        this.render();
        this.setupEventListeners();
        this.setupKeyboardNavigation();
        this.setupResizeObserver();
    }

    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        const tabsContainer = this.createTabsContainer();
        container.innerHTML = '';
        container.appendChild(tabsContainer);
        
        this.tabsElement = tabsContainer;
        this.updateActiveIndicator();
    }

    createTabsContainer() {
        const container = document.createElement('div');
        container.className = this.getContainerClasses();
        container.setAttribute('role', 'tablist');
        container.setAttribute('aria-orientation', this.props.orientation || 'horizontal');

        if (this.props.max_width) {
            container.style.maxWidth = this.props.max_width;
        }

        // Create tab navigation
        const tabNav = this.createTabNavigation();
        container.appendChild(tabNav);

        // Create tab content panels
        const tabContent = this.createTabContent();
        container.appendChild(tabContent);

        return container;
    }

    createTabNavigation() {
        const nav = document.createElement('div');
        nav.className = 'tabs-nav';

        const tabList = document.createElement('div');
        tabList.className = 'tabs-list';

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const tab = this.createTabItem(item);
                tabList.appendChild(tab);
            });
        }

        // Add button for adding new tabs
        if (this.props.show_add_button) {
            const addButton = this.createAddButton();
            tabList.appendChild(addButton);
        }

        nav.appendChild(tabList);

        // Add active indicator for underline variant
        if (this.props.variant === 'underline') {
            const indicator = document.createElement('div');
            indicator.className = 'tabs-indicator';
            nav.appendChild(indicator);
        }

        return nav;
    }

    createTabItem(item) {
        const tab = document.createElement('button');
        tab.className = this.getTabClasses(item);
        tab.setAttribute('role', 'tab');
        tab.setAttribute('aria-selected', item.key === this.activeKey ? 'true' : 'false');
        tab.setAttribute('aria-controls', `${this.containerId}-panel-${item.key}`);
        tab.setAttribute('id', `${this.containerId}-tab-${item.key}`);
        tab.setAttribute('type', 'button');
        tab.setAttribute('data-key', item.key);

        if (item.disabled) {
            tab.setAttribute('disabled', 'true');
            tab.setAttribute('aria-disabled', 'true');
        }

        // Create tab content
        const tabContent = document.createElement('div');
        tabContent.className = 'tab-content';

        // Add icon if present
        if (item.icon) {
            const icon = document.createElement('i');
            icon.className = `tab-icon ${item.icon}`;
            tabContent.appendChild(icon);
        }

        // Add label
        const label = document.createElement('span');
        label.className = 'tab-label';
        label.textContent = item.label;
        tabContent.appendChild(label);

        // Add badge if present
        if (item.badge !== undefined && item.badge !== null) {
            const badge = document.createElement('span');
            badge.className = 'tab-badge';
            badge.textContent = item.badge;
            tabContent.appendChild(badge);
        }

        // Add close button if closable
        if (this.props.closable || item.closable) {
            const closeButton = document.createElement('button');
            closeButton.className = 'tab-close';
            closeButton.setAttribute('type', 'button');
            closeButton.setAttribute('aria-label', `Close ${item.label}`);
            closeButton.innerHTML = '×';
            
            closeButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.closeTab(item.key);
            });
            
            tabContent.appendChild(closeButton);
        }

        tab.appendChild(tabContent);

        // Add click handler
        tab.addEventListener('click', () => {
            if (!item.disabled) {
                this.setActiveTab(item.key);
            }
        });

        return tab;
    }

    createAddButton() {
        const button = document.createElement('button');
        button.className = 'tabs-add-button';
        button.setAttribute('type', 'button');
        button.setAttribute('aria-label', 'Add new tab');
        button.innerHTML = '<i class="tabs-add-icon">+</i>';

        button.addEventListener('click', () => {
            this.addNewTab();
        });

        return button;
    }

    createTabContent() {
        const content = document.createElement('div');
        content.className = 'tabs-content';

        if (this.props.items && this.props.items.length > 0) {
            this.props.items.forEach(item => {
                const panel = this.createTabPanel(item);
                content.appendChild(panel);
            });
        }

        return content;
    }

    createTabPanel(item) {
        const panel = document.createElement('div');
        panel.className = this.getPanelClasses(item);
        panel.setAttribute('role', 'tabpanel');
        panel.setAttribute('aria-labelledby', `${this.containerId}-tab-${item.key}`);
        panel.setAttribute('id', `${this.containerId}-panel-${item.key}`);
        panel.setAttribute('data-key', item.key);

        if (item.key !== this.activeKey) {
            panel.setAttribute('hidden', 'true');
        }

        // Add content
        if (item.content) {
            if (typeof item.content === 'string') {
                panel.innerHTML = item.content;
            } else if (item.content instanceof HTMLElement) {
                panel.appendChild(item.content);
            }
        }

        return panel;
    }

    getContainerClasses() {
        let classes = 'tabs-container';

        if (this.props.orientation) {
            classes += ` tabs-${this.props.orientation}`;
        }

        if (this.props.size) {
            classes += ` tabs-${this.props.size}`;
        }

        if (this.props.variant) {
            classes += ` tabs-${this.props.variant}`;
        }

        if (this.props.animated) {
            classes += ' tabs-animated';
        }

        if (this.props.closable) {
            classes += ' tabs-closable';
        }

        if (this.props.centered) {
            classes += ' tabs-centered';
        }

        if (this.props.show_add_button) {
            classes += ' tabs-has-add-button';
        }

        return classes;
    }

    getTabClasses(item) {
        let classes = 'tab-item';

        if (item.key === this.activeKey) {
            classes += ' tab-active';
        }

        if (item.disabled) {
            classes += ' tab-disabled';
        }

        if (this.props.closable || item.closable) {
            classes += ' tab-closable';
        }

        return classes;
    }

    getPanelClasses(item) {
        let classes = 'tab-panel';

        if (item.key === this.activeKey) {
            classes += ' tab-panel-active';
        }

        return classes;
    }

    setActiveTab(key) {
        if (this.activeKey === key) return;

        const oldKey = this.activeKey;
        this.activeKey = key;

        // Update tab buttons
        const tabs = this.tabsElement.querySelectorAll('.tab-item');
        tabs.forEach(tab => {
            const tabKey = tab.getAttribute('data-key');
            const isActive = tabKey === key;
            
            tab.classList.toggle('tab-active', isActive);
            tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });

        // Update panels
        this.updatePanels(oldKey, key);

        // Update active indicator
        this.updateActiveIndicator();

        // Call change callback
        if (this.props.on_change) {
            this.callCallback(this.props.on_change, { key, oldKey });
        }
    }

    updatePanels(oldKey, newKey) {
        const panels = this.tabsElement.querySelectorAll('.tab-panel');
        
        panels.forEach(panel => {
            const panelKey = panel.getAttribute('data-key');
            const isActive = panelKey === newKey;
            
            panel.classList.toggle('tab-panel-active', isActive);
            
            if (this.props.animated) {
                if (isActive) {
                    panel.removeAttribute('hidden');
                    panel.style.opacity = '0';
                    panel.style.transform = 'translateX(10px)';
                    
                    requestAnimationFrame(() => {
                        panel.style.transition = `opacity ${this.animationDuration}ms ease, transform ${this.animationDuration}ms ease`;
                        panel.style.opacity = '1';
                        panel.style.transform = 'translateX(0)';
                    });
                } else {
                    panel.style.transition = `opacity ${this.animationDuration}ms ease`;
                    panel.style.opacity = '0';
                    
                    setTimeout(() => {
                        panel.setAttribute('hidden', 'true');
                        panel.style.transition = '';
                        panel.style.transform = '';
                    }, this.animationDuration);
                }
            } else {
                if (isActive) {
                    panel.removeAttribute('hidden');
                } else {
                    panel.setAttribute('hidden', 'true');
                }
            }
        });
    }

    updateActiveIndicator() {
        const indicator = this.tabsElement.querySelector('.tabs-indicator');
        if (!indicator) return;

        const activeTab = this.tabsElement.querySelector('.tab-active');
        if (!activeTab) return;

        const tabList = this.tabsElement.querySelector('.tabs-list');
        const tabRect = activeTab.getBoundingClientRect();
        const listRect = tabList.getBoundingClientRect();

        if (this.props.orientation === 'vertical') {
            indicator.style.top = `${activeTab.offsetTop}px`;
            indicator.style.height = `${activeTab.offsetHeight}px`;
            indicator.style.width = '3px';
            indicator.style.left = '0';
        } else {
            indicator.style.left = `${activeTab.offsetLeft}px`;
            indicator.style.width = `${activeTab.offsetWidth}px`;
            indicator.style.height = '3px';
            indicator.style.top = 'auto';
        }
    }

    closeTab(key) {
        if (this.props.items.length <= 1) return; // Don't close if it's the last tab

        // Find the tab to close
        const tabIndex = this.props.items.findIndex(item => item.key === key);
        if (tabIndex === -1) return;

        // Remove from items array
        this.props.items.splice(tabIndex, 1);

        // Update active key if needed
        if (this.activeKey === key) {
            const newActiveIndex = Math.min(tabIndex, this.props.items.length - 1);
            this.activeKey = this.props.items[newActiveIndex]?.key || null;
        }

        // Re-render
        this.render();

        // Call close callback
        if (this.props.on_close) {
            this.callCallback(this.props.on_close, { key });
        }
    }

    addNewTab() {
        if (this.props.on_add) {
            this.callCallback(this.props.on_add, {});
        }
    }

    setupEventListeners() {
        // Handle window resize for indicator positioning
        window.addEventListener('resize', () => {
            this.updateActiveIndicator();
        });

        // Handle tab switching with mouse wheel (on tab navigation)
        const tabNav = this.tabsElement.querySelector('.tabs-nav');
        if (tabNav) {
            tabNav.addEventListener('wheel', (e) => {
                if (e.deltaY !== 0) {
                    e.preventDefault();
                    this.navigateWithWheel(e.deltaY > 0 ? 1 : -1);
                }
            });
        }
    }

    setupKeyboardNavigation() {
        this.tabsElement.addEventListener('keydown', (e) => {
            const tabs = Array.from(this.tabsElement.querySelectorAll('.tab-item:not(.tab-disabled)'));
            const currentIndex = tabs.findIndex(tab => tab.getAttribute('data-key') === this.activeKey);
            
            let newIndex = currentIndex;
            
            switch (e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    newIndex = currentIndex > 0 ? currentIndex - 1 : tabs.length - 1;
                    break;
                    
                case 'ArrowRight':
                case 'ArrowDown':
                    e.preventDefault();
                    newIndex = currentIndex < tabs.length - 1 ? currentIndex + 1 : 0;
                    break;
                    
                case 'Home':
                    e.preventDefault();
                    newIndex = 0;
                    break;
                    
                case 'End':
                    e.preventDefault();
                    newIndex = tabs.length - 1;
                    break;
                    
                case 'Enter':
                case ' ':
                    e.preventDefault();
                    if (tabs[currentIndex]) {
                        tabs[currentIndex].click();
                    }
                    break;
            }
            
            if (newIndex !== currentIndex && tabs[newIndex]) {
                const newKey = tabs[newIndex].getAttribute('data-key');
                this.setActiveTab(newKey);
                tabs[newIndex].focus();
            }
        });
    }

    setupResizeObserver() {
        if (!window.ResizeObserver) return;

        this.resizeObserver = new ResizeObserver(() => {
            this.updateActiveIndicator();
        });

        this.resizeObserver.observe(this.tabsElement);
    }

    navigateWithWheel(direction) {
        const enabledItems = this.props.items.filter(item => !item.disabled);
        const currentIndex = enabledItems.findIndex(item => item.key === this.activeKey);
        
        if (currentIndex === -1) return;
        
        let newIndex;
        if (direction > 0) {
            newIndex = currentIndex < enabledItems.length - 1 ? currentIndex + 1 : 0;
        } else {
            newIndex = currentIndex > 0 ? currentIndex - 1 : enabledItems.length - 1;
        }
        
        this.setActiveTab(enabledItems[newIndex].key);
    }

    callCallback(callback, data) {
        if (typeof callback === 'function') {
            callback(data);
        } else if (typeof callback === 'string') {
            // Try to evaluate as a function
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
        
        if (newProps.active_key !== undefined) {
            this.activeKey = newProps.active_key;
        }
        
        this.render();
    }

    getActiveKey() {
        return this.activeKey;
    }

    getActiveItem() {
        return this.props.items.find(item => item.key === this.activeKey) || null;
    }

    destroy() {
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        
        // Clean up event listeners
        this.keyboardHandlers.clear();
        
        // Remove window resize listener
        window.removeEventListener('resize', this.updateActiveIndicator);
    }
}

// Export for use in other components
window.TabsRenderer = TabsRenderer;