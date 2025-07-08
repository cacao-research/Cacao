/*
  cacao/core/static/js/cacao-core.js
  Provides client-side logic for dynamically rendering the UI
  based on the JSON definition provided by the server.
*/

(function() {
    // Keep track of the last rendered version
    let lastVersion = null;
    let errorCount = 0;
    const MAX_ERROR_ALERTS = 3;

    // Extend the existing CacaoWS object instead of replacing it
    if (!window.CacaoWS) {
        window.CacaoWS = {};
    }
    
    // Add or update the requestServerRefresh method
    window.CacaoWS.requestServerRefresh = async function() {
        try {
            // Include current hash in refresh requests
            const hash = window.location.hash.slice(1);
            console.log("[CacaoCore] Requesting refresh with hash:", hash);
            
            const response = await fetch(`/api/refresh?_hash=${hash}&t=${Date.now()}`, {
                method: 'GET',
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                }
            });
            
            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }
            
            // Get updated UI
            await fetch(`/api/ui?force=true&_hash=${hash}&t=${Date.now()}`, {
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`UI update failed with status ${response.status}`);
                }
                return response.json();
            })
            .then(uiData => {
                console.log("[CacaoCore] Refreshed UI data:", uiData);
                window.CacaoCore.render(uiData);
            })
            .catch(error => {
                console.error("[CacaoCore] Error fetching UI update:", error);
                // Hide overlay on error
                const overlay = document.querySelector('.refresh-overlay');
                if (overlay) overlay.classList.remove('active');
            });
        } catch (error) {
            console.error("[CacaoCore] Refresh request failed:", error);
            // Ensure overlay is hidden even on error
            const overlay = document.querySelector('.refresh-overlay');
            if (overlay) overlay.classList.remove('active');
        }
    };


    // Update syncHashState function to include hash in requests
    async function syncHashState() {
        const page = window.location.hash.slice(1) || '';
        try {
            console.log("[Cacao] Syncing hash state:", page);
            
            // If the hash is empty or just '#', skip the sync
            if (!page) {
                console.log("[Cacao] Empty hash, skipping sync");
                return;
            }
            
            // Show the refresh overlay
            document.querySelector('.refresh-overlay').classList.add('active');
            
            // First update the state
            const stateResponse = await fetch(`/api/action?action=set_state&component_type=current_page&value=${page}&_hash=${page}&t=${Date.now()}`, {
                method: 'GET',
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache', 
                    'Expires': '0'
                }
            });
            
            if (!stateResponse.ok) {
                throw new Error(`Server returned ${stateResponse.status}`);
            }
            
            const stateData = await stateResponse.json();
            console.log("[Cacao] State updated from hash:", stateData);
            
            // Then request a UI refresh with the new state
            await window.CacaoWS.requestServerRefresh();
        } catch (err) {
            console.error('[Cacao] Error syncing hash state:', err);
            document.querySelector('.refresh-overlay').classList.remove('active');
        }
    }

    /**
     * Helper function to check if content contains icon markup
     * @param {string} content - The text content to check
     * @return {boolean} True if the content contains icon markup
     */
    function hasIconMarkup(content) {
        if (!content || typeof content !== 'string') return false;
        return content.includes('<svg') || 
               content.includes('<i class="fa') || 
               content.includes('<span class="cacao-icon"');
    }

    /**
     * Helper function to apply content to elements, handling icon markup properly
     * @param {HTMLElement} el - The element to apply content to
     * @param {string} content - The text content or HTML to apply
     */
    function applyContent(el, content) {
        if (!content) return;
        
        // For <pre> elements, always use textContent to preserve raw text
        if (el.tagName === 'PRE') {
            el.textContent = content;
            return;
        }
        
        // Else, check for icon markup
        if (hasIconMarkup(content)) {
            el.innerHTML = content;
        } else {
            el.textContent = content;
        }
    }

    /**
     * Render array of children onto a parent element.
     */
    function renderChildren(parent, childrenArray) {
        if (Array.isArray(childrenArray)) {
            childrenArray.forEach(child => {
                parent.appendChild(renderComponent(child));
            });
        }
    }

    /**
     * Create a "standard" element (like <div>, <p>, <code>, <ol>, etc.)
     * without needing a specialized function for each one.
     */
    function renderStandardElement(component) {
        const el = document.createElement(component.type);

        // If there's "component.props.content", apply it
        if (component.props && component.props.content) {
            applyContent(el, component.props.content);
        }

        // If there are children in `component.children` or `component.props.children`, render them
        if (component.children) {
            renderChildren(el, component.children);
        } else if (component.props && component.props.children) {
            renderChildren(el, component.props.children);
        }

        return el;
    }

    // Any HTML tags you want to handle automatically (including your missing ones: <code>, <ol>, etc.)
    const STANDARD_TAGS = new Set([
        "div", "span", "section", "main", "nav",
        "header", "footer", "pre", "code",
        "p", "li", "ul", "ol",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "form", "textarea", "input", "button", // Form elements
        "table", "thead", "tbody", "tr", "td", "th", // Table elements
        "img", "a", "label", "select", "option", // Other common elements
        "svg", "path", "circle", "rect", "g", "text", // SVG elements
        "i", "span", "br", "hr", "strong", "em", "u", "s", "sub", "sup", // Text formatting elements
        "details", "summary", // Collapsible elements
        "canvas", "video", "audio", // Media elements
        "style", "link" // For CSS and other links
    ]);

    /**
     * Specialized renderers for components needing custom logic or event handling
     */
    const componentRenderers = {
        descriptions: (component) => {
            console.log("[CacaoCore] Rendering descriptions component:", component);
            const el = document.createElement("div");
            el.className = "descriptions";
            
            // Add bordered class if specified
            if (component.props.bordered) {
                el.classList.add("bordered");
            }

            // Add columns class if specified
            if (component.props.column) {
                el.classList.add(`columns-${component.props.column}`);
            }

            // Add title if provided
            if (component.props.title) {
                const titleDiv = document.createElement("div");
                titleDiv.className = "descriptions-title";
                titleDiv.textContent = component.props.title;
                el.appendChild(titleDiv);
            }

            // Create items wrapper
            const itemsWrapper = document.createElement("div");
            itemsWrapper.className = "descriptions-items";

            // Add items
            if (Array.isArray(component.props.items)) {
                component.props.items.forEach(item => {
                    const itemDiv = document.createElement("div");
                    itemDiv.className = "descriptions-item";

                    const labelDiv = document.createElement("div");
                    labelDiv.className = "descriptions-label";
                    labelDiv.textContent = item.label;
                    itemDiv.appendChild(labelDiv);

                    const contentDiv = document.createElement("div");
                    contentDiv.className = "descriptions-content";
                    if (typeof item.content === 'string') {
                        contentDiv.textContent = item.content;
                    } else {
                        contentDiv.appendChild(renderComponent(item.content));
                    }
                    itemDiv.appendChild(contentDiv);

                    itemsWrapper.appendChild(itemDiv);
                });
            }

            el.appendChild(itemsWrapper);

            // Add styles
            const style = document.createElement('style');
            style.textContent = `
                .descriptions {
                    width: 100%;
                    font-size: 14px;
                }

                .descriptions.bordered {
                    border: 1px solid #e8e8e8;
                    border-radius: 4px;
                }

                .descriptions-title {
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 16px;
                    padding: 16px;
                    border-bottom: 1px solid #e8e8e8;
                }

                .descriptions-items {
                    padding: 16px;
                    display: grid;
                    grid-gap: 16px;
                }

                .descriptions.columns-2 .descriptions-items {
                    grid-template-columns: repeat(2, 1fr);
                }

                .descriptions-item {
                    display: flex;
                    flex-direction: column;
                }

                .descriptions-label {
                    color: #666;
                    margin-bottom: 4px;
                }

                .descriptions-content {
                    color: #333;
                }

                .descriptions.bordered .descriptions-items {
                    border-radius: 0 0 4px 4px;
                }
            `;
            el.appendChild(style);

            return el;
        },

        list: (component) => {
            console.log("[CacaoCore] Rendering list component:", component);
            const el = document.createElement("div");
            el.className = "list";
            if (component.props.bordered) el.classList.add("bordered");
            if (component.props.size) el.classList.add(component.props.size);

            if (Array.isArray(component.props.items)) {
                component.props.items.forEach(item => {
                    const itemEl = document.createElement("div");
                    itemEl.className = "list-item";
                    
                    if (item.title) {
                        const title = document.createElement("div");
                        title.className = "list-item-title";
                        title.textContent = item.title;
                        itemEl.appendChild(title);
                    }

                    if (item.description) {
                        const desc = document.createElement("div");
                        desc.className = "list-item-description";
                        desc.textContent = item.description;
                        itemEl.appendChild(desc);
                    }

                    el.appendChild(itemEl);
                });
            }

            return el;
        },

        enhancedTable: (component) => {
            console.log("[CacaoCore] Rendering enhanced table component:", component);
            const wrapper = document.createElement("div");
            wrapper.className = "enhanced-table-wrapper";

            const table = document.createElement("table");
            table.className = "enhanced-table";

            // Create header
            const thead = document.createElement("thead");
            const headerRow = document.createElement("tr");
            component.props.columns.forEach(column => {
                const th = document.createElement("th");
                th.textContent = column.title;
                if (component.props.sorting) {
                    th.classList.add("sortable");
                    th.onclick = () => {
                        // Sorting logic would go here
                        console.log("[CacaoCore] Sort by:", column.key);
                    };
                }
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Create body
            const tbody = document.createElement("tbody");
            if (Array.isArray(component.props.dataSource)) {
                component.props.dataSource.forEach(row => {
                    const tr = document.createElement("tr");
                    component.props.columns.forEach(column => {
                        const td = document.createElement("td");
                        td.textContent = row[column.dataIndex];
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
            }
            table.appendChild(tbody);

            wrapper.appendChild(table);

            // Add pagination if specified
            if (component.props.pagination) {
                const pagination = document.createElement("div");
                pagination.className = "table-pagination";
                // Pagination UI would go here
                wrapper.appendChild(pagination);
            }

            return wrapper;
        },

        card: (component) => {
            console.log("[CacaoCore] Rendering card component:", component);
            const el = document.createElement("div");
            el.className = "card";
            if (component.props.bordered) el.classList.add("bordered");

            if (component.props.title) {
                const header = document.createElement("div");
                header.className = "card-header";
                const title = document.createElement("div");
                title.className = "card-title";
                title.textContent = component.props.title;
                header.appendChild(title);

                if (component.props.extra) {
                    const extra = document.createElement("div");
                    extra.className = "card-extra";
                    if (typeof component.props.extra === 'string') {
                        extra.textContent = component.props.extra;
                    } else {
                        extra.appendChild(renderComponent(component.props.extra));
                    }
                    header.appendChild(extra);
                }

                el.appendChild(header);
            }

            const content = document.createElement("div");
            content.className = "card-content";
            if (typeof component.props.children === 'string') {
                content.textContent = component.props.children;
            } else if (Array.isArray(component.props.children)) {
                component.props.children.forEach(child => {
                    content.appendChild(renderComponent(child));
                });
            } else if (component.props.children) {
                content.appendChild(renderComponent(component.props.children));
            }
            el.appendChild(content);

            return el;
        },

        badge: (component) => {
            console.log("[CacaoCore] Rendering badge component:", component);
            const wrapper = document.createElement("span");
            wrapper.className = "badge-wrapper";

            // Render the main content if provided
            if (component.props.children) {
                wrapper.appendChild(renderComponent(component.props.children));
            }

            // Create the badge element
            const badge = document.createElement("span");
            badge.className = "badge";

            // Handle dot style badge
            if (component.props.dot) {
                badge.classList.add("dot");
            } else if (component.props.count !== undefined) {
                // Show count if not zero or showZero is true
                if (component.props.count > 0 || component.props.showZero) {
                    badge.textContent = component.props.count;
                }
            }

            wrapper.appendChild(badge);
            return wrapper;
        },

        avatar: (component) => {
            console.log("[CacaoCore] Rendering avatar component:", component);
            const el = document.createElement("span");
            el.className = "avatar";
            
            if (component.props.shape) {
                el.classList.add(component.props.shape);
            }
            if (component.props.size) {
                el.classList.add(component.props.size);
            }

            if (component.props.src) {
                const img = document.createElement("img");
                img.src = component.props.src;
                img.alt = "Avatar";
                el.appendChild(img);
            } else if (component.props.icon) {
                const icon = document.createElement("span");
                icon.className = "avatar-icon";
                applyContent(icon, component.props.icon);
                el.appendChild(icon);
            }

            return el;
        },

        tag: (component) => {
            console.log("[CacaoCore] Rendering tag component:", component);
            const el = document.createElement("span");
            el.className = "tag";
            
            if (component.props.color) {
                el.classList.add(`tag-${component.props.color}`);
                el.style.backgroundColor = component.props.color;
            }

            if (component.props.content) {
                el.textContent = component.props.content;
            }

            if (component.props.closable) {
                const closeBtn = document.createElement("span");
                closeBtn.className = "tag-close";
                closeBtn.innerHTML = "×";
                closeBtn.onclick = (e) => {
                    e.stopPropagation();
                    el.remove();
                };
                el.appendChild(closeBtn);
            }

            return el;
        },

        timeline: (component) => {
            console.log("[CacaoCore] Rendering timeline component:", component);
            const el = document.createElement("div");
            el.className = "timeline";
            
            if (component.props.mode) {
                el.classList.add(`timeline-${component.props.mode}`);
            }
            
            if (component.props.reverse) {
                el.classList.add("timeline-reverse");
            }

            if (Array.isArray(component.props.items)) {
                const items = component.props.reverse ?
                    [...component.props.items].reverse() :
                    component.props.items;
                    
                items.forEach(item => {
                    const itemEl = document.createElement("div");
                    itemEl.className = "timeline-item";

                    // Add dot
                    const dot = document.createElement("div");
                    dot.className = "timeline-dot";
                    itemEl.appendChild(dot);

                    // Add label if provided
                    if (item.label) {
                        const label = document.createElement("div");
                        label.className = "timeline-label";
                        label.textContent = item.label;
                        itemEl.appendChild(label);
                    }

                    // Add content
                    const content = document.createElement("div");
                    content.className = "timeline-content";
                    if (typeof item.content === 'string') {
                        content.textContent = item.content;
                    } else {
                        content.appendChild(renderComponent(item.content));
                    }
                    itemEl.appendChild(content);

                    el.appendChild(itemEl);
                });
            }

            return el;
        },

        text: (component) => {
            const el = document.createElement("p");
            el.className = "text";
            applyContent(el, component.props.content);
            return el;
        },
        
        navbar: (component) => {
            const el = document.createElement("nav");
            el.className = "navbar";
            
            if (component.props?.brand) {
                const brandDiv = document.createElement("div");
                brandDiv.className = "brand";
                applyContent(brandDiv, component.props.brand);
                el.appendChild(brandDiv);
            }
            
            if (component.props?.links) {
                const linksDiv = document.createElement("div");
                component.props.links.forEach(link => {
                    const a = document.createElement("a");
                    a.href = link.url;
                    applyContent(a, link.name);
                    linksDiv.appendChild(a);
                });
                el.appendChild(linksDiv);
            }
            return el;
        },

        sidebar: (component) => {
            const el = document.createElement("div");
            el.className = "sidebar";
            
            // Apply styles from props
            if (component.props?.style) {
                Object.assign(el.style, component.props.style);
            }
            if (component.props?.content) {
                applyContent(el, component.props.content);
            }
            if (component.children) {
                renderChildren(el, component.children);
            } else if (component.props?.children) {
                renderChildren(el, component.props.children);
            }
            return el;
        },

        "nav-item": (component) => {
            const el = document.createElement("div");
            el.className = "nav-item";
            
            // If children array is available, use that
            if (component.props?.children && Array.isArray(component.props.children)) {
                component.props.children.forEach(child => {
                    el.appendChild(renderComponent(child));
                });
            } else {
                // Simple/legacy rendering
                if (component.props?.icon) {
                    const iconSpan = document.createElement("span");
                    applyContent(iconSpan, component.props.icon);
                    iconSpan.style.marginRight = "8px";
                    el.appendChild(iconSpan);
                }
                if (component.props?.label) {
                    const labelSpan = document.createElement("span");
                    applyContent(labelSpan, component.props.label);
                    el.appendChild(labelSpan);
                }
            }
            
            if (component.props?.isActive) {
                el.classList.add("active");
            }
            
            if (component.props?.onClick) {
                el.onclick = async () => {
                    try {
                        const action = component.props.onClick.action;
                        const state = component.props.onClick.state;
                        const value = component.props.onClick.value;
                        const immediate = component.props.onClick.immediate === true;
                        
                        // Check if we're clicking the same page
                        if (state === 'current_page' && window.location.hash === `#${value}`) {
                            console.log("[CacaoCore] Clicked same page, skipping refresh");
                            return;
                        }
                        
                        document.querySelector('.refresh-overlay').classList.add('active');
                        
                        console.log(`[CacaoCore] Handling nav click: ${action} state=${state} value=${value} immediate=${immediate}`);
                        
                        const response = await fetch(`/api/action?action=${action}&component_type=${state}&value=${value}&immediate=${immediate}&t=${Date.now()}`, {
                            method: 'GET',
                            headers: {
                                'Cache-Control': 'no-cache, no-store, must-revalidate',
                                'Pragma': 'no-cache',
                                'Expires': '0'
                            }
                        });
                        
                        if (!response.ok) {
                            throw new Error(`Server returned ${response.status}`);
                        }
                        const data = await response.json();
                        console.log("[CacaoCore] Navigation state updated:", data);
                        
                        if (state === 'current_page') {
                            window.location.hash = value;
                        }
                        
                        if (data.immediate === true) {
                            // fetch UI directly
                            const uiResponse = await fetch(`/api/ui?force=true&_hash=${value}&t=${Date.now()}`, {
                                headers: {
                                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                                    'Pragma': 'no-cache',
                                    'Expires': '0'
                                }
                            });
                            
                            if (!uiResponse.ok) {
                                throw new Error(`UI update failed with status ${uiResponse.status}`);
                            }
                            
                            const uiData = await uiResponse.json();
                            window.CacaoCore.render(uiData);
                        } else {
                            // Force UI refresh
                            window.CacaoWS.requestServerRefresh();
                        }
                    } catch (err) {
                        console.error('[CacaoCore] Error handling nav item click:', err);
                        document.querySelector('.refresh-overlay').classList.remove('active');
                    }
                };
            }
            
            return el;
        },

        button: (component) => {
            const el = document.createElement("button");
            el.className = "button";
            applyContent(el, component.props.label);
            
            if (component.props?.action) {
                el.onclick = async () => {
                    try {
                        console.log("[Cacao] Sending event:", component.props.on_click || component.props.action);
                        document.querySelector('.refresh-overlay').classList.add('active');
                        
                        const parentSection = el.closest('section[data-component-type]');
                        const componentType = parentSection ? parentSection.dataset.componentType : 'unknown';
                        
                        // If WebSocket is open
                        if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                            const eventName = component.props.on_click || component.props.action;
                            console.log("[Cacao] Sending WebSocket event:", eventName);
                            // Include the data property from the component if available
                            const eventData = { component_type: componentType };
                            
                            // Add the data property from the component if it exists
                            if (component.props.data) {
                                console.log("[Cacao] Including custom data in event:", component.props.data);
                                Object.assign(eventData, component.props.data);
                            }
                            
                            window.socket.send(JSON.stringify({
                                type: 'event',
                                event: eventName,
                                data: eventData
                            }));
                        } else {
                            // Fallback to HTTP
                            console.log("[Cacao] WebSocket not available, using HTTP fallback");
                            const action = component.props.on_click || component.props.action;
                            // Build query parameters including custom data
                            let queryParams = `action=${action}&component_type=${componentType}`;
                            
                            // Add the data property from the component if it exists
                            if (component.props.data) {
                                console.log("[Cacao] Including custom data in HTTP fallback:", component.props.data);
                                for (const [key, value] of Object.entries(component.props.data)) {
                                    queryParams += `&${key}=${encodeURIComponent(value)}`;
                                }
                            }
                            
                            const response = await fetch(`/api/action?${queryParams}&t=${Date.now()}`, {
                                method: 'GET',
                                headers: {
                                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                                    'Pragma': 'no-cache',
                                    'Expires': '0'
                                }
                            });
                            
                            if (!response.ok) {
                                const errorText = await response.text();
                                console.error("[Cacao] Server error response:", errorText);
                                throw new Error(`Server returned ${response.status}: ${errorText}`);
                            }
                            
                            const responseData = await response.json();
                            console.log("[CacaoCore] Server response data:", responseData);
                            window.CacaoWS.requestServerRefresh();
                        }
                    } catch (err) {
                        console.error('Error handling action:', err);
                        document.querySelector('.refresh-overlay').classList.remove('active');
                        
                        if (errorCount < MAX_ERROR_ALERTS) {
                            errorCount++;
                            alert(`Error: ${err.message}\nPlease try again or reload the page.`);
                        } else if (errorCount === MAX_ERROR_ALERTS) {
                            errorCount++;
                            console.error("Too many errors. Suppressing further alerts.");
                        }
                    }
                };
            }
            
            return el;
        },

        "task-item": (component) => {
            const el = document.createElement("li");
            el.className = "task-item";
            el.dataset.id = component.props.id;
            
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.checked = component.props.completed;
            
            if (component.props?.onToggle) {
                checkbox.addEventListener("change", async () => {
                    try {
                        document.querySelector('.refresh-overlay').classList.add('active');
                        
                        const action = component.props.onToggle.action;
                        const params = component.props.onToggle.params;
                        const url = `/api/action?action=${action}&component_type=task&id=${params.id}&t=${Date.now()}`;
                        
                        const response = await fetch(url, {
                            method: 'GET',
                            headers: {
                                'Cache-Control': 'no-cache, no-store, must-revalidate'
                            }
                        });
                        
                        if (!response.ok) {
                            throw new Error(`Server returned ${response.status}`);
                        }
                        
                        window.CacaoWS.requestServerRefresh();
                    } catch (err) {
                        console.error('[CacaoCore] Error toggling task:', err);
                        document.querySelector('.refresh-overlay').classList.remove('active');
                    }
                });
            }
            
            const taskLabel = document.createElement("span");
            applyContent(taskLabel, component.props.title);
            if (component.props.completed) {
                taskLabel.style.textDecoration = "line-through";
                taskLabel.style.color = "#888";
            }
            
            el.appendChild(checkbox);
            el.appendChild(taskLabel);
            return el;
        },

        "react-component": (component) => {
            const el = document.createElement("div");
            el.id = component.props.id;
            el.className = "react-component-container";
            
            const loadingDiv = document.createElement("div");
            loadingDiv.className = "react-loading";
            loadingDiv.textContent = `Loading ${component.props.package}...`;
            el.appendChild(loadingDiv);
            
            setTimeout(() => {
                if (window.ReactBridge && typeof window.ReactBridge.renderComponent === "function") {
                    window.ReactBridge.renderComponent(component.props).then(success => {
                        if (success) {
                            loadingDiv.remove();
                        }
                    });
                } else {
                    console.error("[CacaoCore] ReactBridge not available");
                    loadingDiv.textContent = "Error: React bridge not available";
                }
            }, 0);
            
            return el;
        },
        
        datepicker: (component) => {
            console.log("[CacaoCore] Rendering datepicker component:", component);
            const el = document.createElement("input");
            el.type = "date";
            
            // Set common attributes
            if (component.props.value !== undefined) el.value = component.props.value;
            if (component.props.disabled) el.disabled = true;
            
            // Apply styles
            if (component.props.style) {
                Object.assign(el.style, component.props.style);
            }
            
            // Add event listener for changes
            if (component.props.onChange) {
                el.addEventListener("change", async (e) => {
                    console.log("[CacaoCore] Date changed:", e.target.value);
                    
                    const action = component.props.onChange.action || "date_change";
                    const params = {
                        ...(component.props.onChange.params || {}),
                        value: e.target.value
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending date event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Date event successful");
                            window.CacaoWS.requestServerRefresh();
                        } else {
                            console.error("[CacaoCore] Date event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending date event:", err);
                    }
                });
            }
            
            return el;
        },
        
        timepicker: (component) => {
            console.log("[CacaoCore] Rendering timepicker component:", component);
            const el = document.createElement("input");
            el.type = "time";
            
            // Set common attributes
            if (component.props.value !== undefined) el.value = component.props.value;
            if (component.props.disabled) el.disabled = true;
            
            // Apply styles
            if (component.props.style) {
                Object.assign(el.style, component.props.style);
            }
            
            // Add event listener for changes
            if (component.props.onChange) {
                el.addEventListener("change", async (e) => {
                    console.log("[CacaoCore] Time changed:", e.target.value);
                    
                    const action = component.props.onChange.action || "time_change";
                    const params = {
                        ...(component.props.onChange.params || {}),
                        value: e.target.value
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending time event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Time event successful");
                            window.CacaoWS.requestServerRefresh();
                        } else {
                            console.error("[CacaoCore] Time event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending time event:", err);
                    }
                });
            }
            
            return el;
        },
        
        upload: (component) => {
            console.log("[CacaoCore] Rendering upload component:", component);
            
            // Create wrapper div
            const wrapper = document.createElement("div");
            wrapper.className = "upload-wrapper";
            
            // Create file input
            const input = document.createElement("input");
            input.type = "file";
            if (component.props.multiple) input.multiple = true;
            if (component.props.disabled) input.disabled = true;
            
            // Apply styles
            if (component.props.style) {
                Object.assign(wrapper.style, component.props.style);
            }
            
            // Add label or placeholder
            const label = document.createElement("div");
            label.textContent = component.props.label || "Click or drag files here to upload";
            wrapper.appendChild(label);
            
            // Add file input
            wrapper.appendChild(input);
            
            // Add event listener for changes
            if (component.props.onUpload) {
                input.addEventListener("change", async (e) => {
                    console.log("[CacaoCore] Files selected:", e.target.files);
                    
                    // In a real implementation, you would upload the files here
                    // For now, just trigger the event
                    const action = component.props.onUpload.action || "file_upload";
                    const params = {
                        ...(component.props.onUpload.params || {}),
                        fileCount: e.target.files.length
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending upload event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Upload event successful");
                            window.CacaoWS.requestServerRefresh();
                        } else {
                            console.error("[CacaoCore] Upload event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending upload event:", err);
                    }
                });
            }
            
            return wrapper;
        },
        
        search: (component) => {
            console.log("[CacaoCore] Rendering search component:", component);
            
            // Create wrapper div
            const wrapper = document.createElement("div");
            wrapper.className = "search-input-wrapper";
            
            // Create search input
            const input = document.createElement("input");
            input.type = "search";
            if (component.props.value !== undefined) input.value = component.props.value;
            if (component.props.placeholder) input.placeholder = component.props.placeholder;
            if (component.props.disabled) input.disabled = true;
            
            // Apply styles
            if (component.props.style) {
                Object.assign(input.style, component.props.style);
            }
            
            // Create search button
            const button = document.createElement("button");
            button.textContent = "Search";
            button.className = "search-button";
            
            // Append elements
            wrapper.appendChild(input);
            wrapper.appendChild(button);
            
            // Add event listener for search
            if (component.props.onSearch) {
                const performSearch = async () => {
                    console.log("[CacaoCore] Search:", input.value);
                    
                    const action = component.props.onSearch.action || "search";
                    const params = {
                        ...(component.props.onSearch.params || {}),
                        query: input.value
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending search event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Search event successful");
                            window.CacaoWS.requestServerRefresh();
                        } else {
                            console.error("[CacaoCore] Search event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending search event:", err);
                    }
                };
                
                // Search on button click
                button.addEventListener("click", performSearch);
                
                // Search on Enter key
                input.addEventListener("keydown", (e) => {
                    if (e.key === "Enter") {
                        e.preventDefault();
                        performSearch();
                    }
                });
            }
            
            return wrapper;
        },

        input: (component) => {
            console.log("[CacaoCore] Rendering input component:", component);
            const el = document.createElement("input");
            
            // Set input type (text, password, email, etc.)
            el.type = component.props.inputType || "text";
            
            // Set common attributes
            if (component.props.value !== undefined) el.value = component.props.value;
            if (component.props.placeholder) el.placeholder = component.props.placeholder;
            if (component.props.disabled) el.disabled = true;
            
            // Apply styles
            if (component.props.style) {
                Object.assign(el.style, component.props.style);
            }
            
            // Add event listener for changes
            if (component.props.onChange) {
                el.addEventListener("input", async (e) => {
                    console.log("[CacaoCore] Input changed:", e.target.value);
                    
                    const action = component.props.onChange.action || "input_change";
                    const params = {
                        ...(component.props.onChange.params || {}),
                        value: e.target.value
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending input event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Input event successful");
                        } else {
                            console.error("[CacaoCore] Input event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending input event:", err);
                    }
                });
            }
            
            return el;
        },
        
        textarea: (component) => {
            console.log("[CacaoCore] Rendering textarea component:", component);
            const el = document.createElement("textarea");
            
            // Set common attributes
            if (component.props.value !== undefined) el.value = component.props.value;
            if (component.props.placeholder) el.placeholder = component.props.placeholder;
            if (component.props.disabled) el.disabled = true;
            if (component.props.rows) el.rows = component.props.rows;
            
            // Apply styles
            if (component.props.style) {
                Object.assign(el.style, component.props.style);
            }
            
            // Add event listener for changes
            if (component.props.onChange) {
                el.addEventListener("input", async (e) => {
                    console.log("[CacaoCore] Textarea changed:", e.target.value);
                    
                    const action = component.props.onChange.action || "textarea_change";
                    const params = {
                        ...(component.props.onChange.params || {}),
                        value: e.target.value
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending textarea event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Textarea event successful");
                        } else {
                            console.error("[CacaoCore] Textarea event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending textarea event:", err);
                    }
                });
            }
            
            return el;
        },
        
        select: (component) => {
            console.log("[CacaoCore] Rendering select component:", component);
            const el = document.createElement("select");
            
            // Set common attributes
            if (component.props.value !== undefined) el.value = component.props.value;
            if (component.props.disabled) el.disabled = true;
            
            // Apply styles
            if (component.props.style) {
                Object.assign(el.style, component.props.style);
            }
            
            // Add placeholder if provided
            if (component.props.placeholder) {
                const placeholderOption = document.createElement("option");
                placeholderOption.value = "";
                placeholderOption.textContent = component.props.placeholder;
                placeholderOption.disabled = true;
                placeholderOption.selected = !component.props.value;
                el.appendChild(placeholderOption);
            }
            
            // Add options
            if (Array.isArray(component.props.options)) {
                component.props.options.forEach(option => {
                    const optionEl = document.createElement("option");
                    optionEl.value = option.value;
                    optionEl.textContent = option.label;
                    if (component.props.value === option.value) {
                        optionEl.selected = true;
                    }
                    el.appendChild(optionEl);
                });
            }
            
            // Add event listener for changes
            if (component.props.onChange) {
                el.addEventListener("change", async (e) => {
                    console.log("[CacaoCore] Select changed:", e.target.value);
                    
                    const action = component.props.onChange.action || "select_change";
                    const params = {
                        ...(component.props.onChange.params || {}),
                        value: e.target.value
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending select event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Select event successful");
                            window.CacaoWS.requestServerRefresh();
                        } else {
                            console.error("[CacaoCore] Select event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending select event:", err);
                    }
                });
            }
            
            return el;
        },
        
        checkbox: (component) => {
            console.log("[CacaoCore] Rendering checkbox component:", component);
            
            // Create wrapper div
            const wrapper = document.createElement("div");
            wrapper.className = "checkbox-wrapper";
            
            // Create checkbox input
            const input = document.createElement("input");
            input.type = "checkbox";
            input.checked = !!component.props.checked;
            if (component.props.disabled) input.disabled = true;
            
            // Create label
            const label = document.createElement("span");
            label.textContent = component.props.label || "";
            
            // Append elements
            wrapper.appendChild(input);
            wrapper.appendChild(label);
            
            // Add event listener for changes
            if (component.props.onChange) {
                input.addEventListener("change", async (e) => {
                    console.log("[CacaoCore] Checkbox changed:", e.target.checked);
                    
                    const action = component.props.onChange.action || "checkbox_change";
                    const params = {
                        ...(component.props.onChange.params || {}),
                        checked: e.target.checked
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending checkbox event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Checkbox event successful");
                            window.CacaoWS.requestServerRefresh();
                        } else {
                            console.error("[CacaoCore] Checkbox event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending checkbox event:", err);
                    }
                });
            }
            
            return wrapper;
        },
        
        radio: (component) => {
            console.log("[CacaoCore] Rendering radio component:", component);
            
            // Create wrapper div
            const wrapper = document.createElement("div");
            wrapper.className = "radio-group";
            
            // Add options
            if (Array.isArray(component.props.options)) {
                component.props.options.forEach(option => {
                    const radioWrapper = document.createElement("div");
                    radioWrapper.className = "radio-wrapper";
                    
                    const input = document.createElement("input");
                    input.type = "radio";
                    input.name = `radio-${Math.random().toString(36).substring(2, 9)}`;
                    input.value = option.value;
                    input.checked = component.props.value === option.value;
                    if (component.props.disabled) input.disabled = true;
                    
                    const label = document.createElement("span");
                    label.textContent = option.label || option.value;
                    
                    radioWrapper.appendChild(input);
                    radioWrapper.appendChild(label);
                    wrapper.appendChild(radioWrapper);
                    
                    // Add event listener for changes
                    if (component.props.onChange) {
                        input.addEventListener("change", async (e) => {
                            if (e.target.checked) {
                                console.log("[CacaoCore] Radio changed:", e.target.value);
                                
                                const action = component.props.onChange.action || "radio_change";
                                const params = {
                                    ...(component.props.onChange.params || {}),
                                    value: e.target.value
                                };
                                
                                // HTTP fallback
                                const queryParams = Object.entries(params)
                                    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                                    .join("&");
                                    
                                const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                                try {
                                    console.log("[CacaoCore] Sending radio event:", url);
                                    const response = await fetch(url, {
                                        method: "GET",
                                        headers: {
                                            "Cache-Control": "no-cache, no-store, must-revalidate"
                                        }
                                    });
                                    
                                    if (response.ok) {
                                        console.log("[CacaoCore] Radio event successful");
                                        window.CacaoWS.requestServerRefresh();
                                    } else {
                                        console.error("[CacaoCore] Radio event failed:", response.status);
                                    }
                                } catch (err) {
                                    console.error("[CacaoCore] Error sending radio event:", err);
                                }
                            }
                        });
                    }
                });
            }
            
            return wrapper;
        },
        
        switch: (component) => {
            console.log("[CacaoCore] Rendering switch component:", component);
            
            // Create wrapper div
            const wrapper = document.createElement("div");
            wrapper.className = "switch-wrapper";
            
            // Create checkbox input
            const input = document.createElement("input");
            input.type = "checkbox";
            input.checked = !!component.props.checked;
            if (component.props.disabled) input.disabled = true;
            
            // Create slider
            const slider = document.createElement("span");
            slider.className = "switch-slider";
            
            // Append elements
            wrapper.appendChild(input);
            wrapper.appendChild(slider);
            
            // Add event listener for changes
            if (component.props.onChange) {
                input.addEventListener("change", async (e) => {
                    console.log("[CacaoCore] Switch changed:", e.target.checked);
                    
                    const action = component.props.onChange.action || "switch_change";
                    const params = {
                        ...(component.props.onChange.params || {}),
                        checked: e.target.checked
                    };
                    
                    // HTTP fallback
                    const queryParams = Object.entries(params)
                        .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                        .join("&");
                        
                    const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                    try {
                        console.log("[CacaoCore] Sending switch event:", url);
                        const response = await fetch(url, {
                            method: "GET",
                            headers: {
                                "Cache-Control": "no-cache, no-store, must-revalidate"
                            }
                        });
                        
                        if (response.ok) {
                            console.log("[CacaoCore] Switch event successful");
                            window.CacaoWS.requestServerRefresh();
                        } else {
                            console.error("[CacaoCore] Switch event failed:", response.status);
                        }
                    } catch (err) {
                        console.error("[CacaoCore] Error sending switch event:", err);
                    }
                });
            }
            
            return wrapper;
        },

        rate: (component) => {
            console.log("[CacaoCore] Rendering rate component:", component);
            const max = component.props.max || 5;
            const value = typeof component.props.value === "number" ? component.props.value : 0;
            const disabled = !!component.props.disabled;
            
            // Create wrapper with class matching the CSS in default_theme.py
            const el = document.createElement("div");
            el.className = "rate-wrapper";
            
            // Helper to render stars
            function renderStars(currentValue) {
                console.log("[CacaoCore] Rendering stars with value:", currentValue);
                el.innerHTML = "";
                for (let i = 1; i <= max; i++) {
                    const star = document.createElement("span");
                    // Use classes that match the CSS in default_theme.py
                    star.className = "rate-star";
                    if (i <= currentValue) {
                        star.className += " filled";
                    }
                    if (disabled) {
                        star.className += " disabled";
                    }
                    
                    // Use Unicode stars
                    star.textContent = "★";
                    
                    // Make focusable for accessibility
                    star.setAttribute("tabindex", disabled ? "-1" : "0");
                    star.setAttribute("role", "button");
                    star.setAttribute("aria-label", `Rate ${i} of ${max}`);
                    
                    if (!disabled) {
                        // Add hover effects
                        star.addEventListener("mouseenter", () => {
                            console.log("[CacaoCore] Star hover:", i);
                            renderStars(i);
                        });
                        
                        star.addEventListener("mouseleave", () => {
                            renderStars(currentValue);
                        });
                        
                        // Add click handler
                        star.addEventListener("click", async (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log("[CacaoCore] Star clicked:", i);
                            
                            // Update UI immediately for better UX
                            renderStars(i);
                            
                            if (component.props.onChange) {
                                // Send event to backend
                                const action = component.props.onChange.action || "rate_change";
                                const params = {
                                    ...(component.props.onChange.params || {}),
                                    value: i
                                };
                                
                                // HTTP fallback
                                const queryParams = Object.entries(params)
                                    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                                    .join("&");
                                    
                                const url = `/api/event?event=${action}&${queryParams}&t=${Date.now()}`;
                                try {
                                    console.log("[CacaoCore] Sending rate event:", url);
                                    const response = await fetch(url, {
                                        method: "GET",
                                        headers: {
                                            "Cache-Control": "no-cache, no-store, must-revalidate"
                                        }
                                    });
                                    
                                    if (response.ok) {
                                        console.log("[CacaoCore] Rate event successful");
                                        window.CacaoWS.requestServerRefresh();
                                    } else {
                                        console.error("[CacaoCore] Rate event failed:", response.status);
                                    }
                                } catch (err) {
                                    console.error("[CacaoCore] Error sending rate event:", err);
                                }
                            }
                        });
                        
                        // Add keyboard support
                        star.addEventListener("keydown", (e) => {
                            if (e.key === "Enter" || e.key === " ") {
                                e.preventDefault();
                                star.click();
                            }
                        });
                    }
                    
                    el.appendChild(star);
                }
            }

            // Initial render
            renderStars(value);

            // Optionally add a label
            if (component.props.label) {
                const label = document.createElement("span");
                label.textContent = component.props.label;
                label.style.marginLeft = "8px";
                el.appendChild(label);
            }

            return el;
        },

        "range-slider": (component) => {
            const slider = document.createElement("input");
            slider.type = "range";
            slider.className = component.props.className || "range-slider";
            slider.min = component.props.min;
            slider.max = component.props.max;
            slider.step = component.props.step;
            slider.value = component.props.value;

            let updateTimeout;
            const updateValue = async () => {
                if (component.props.onChange) {
                    // Clear any existing timeout to debounce
                    clearTimeout(updateTimeout);
                    
                    // Re-introduce setTimeout with a longer delay (150ms)
                    updateTimeout = setTimeout(async () => {
                        try {
                            // Consider adding a subtle visual cue instead of the full overlay for frequent events
                            // document.querySelector('.refresh-overlay').classList.add('active');
                            
                            const action = component.props.onChange.action;
                            const params = {
                                ...component.props.onChange.params,
                                value: slider.value // Use the current slider value at the time of execution
                            };
                            
                            const queryParams = Object.entries(params)
                                .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
                                .join('&');
                                
                            // console.log(`[CacaoCore] Sending event (debounced): ${action} with params: ${queryParams}`); // Optional: uncomment for debugging
                            
                            // Send event via HTTP GET
                            const response = await fetch(`/api/event?event=${action}&${queryParams}&t=${Date.now()}`, {
                                method: 'GET',
                                headers: {
                                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                                }
                            });
                            
                            if (!response.ok) {
                                throw new Error(`Server returned ${response.status}`);
                            }
                            
                            const data = await response.json();
                            // console.log("[CacaoCore] Event response (debounced):", data); // Optional: uncomment for debugging
                            
                            // Update slider value based on response *if* backend sends it back
                            // This helps keep frontend consistent if backend modifies the value
                            if (data.value !== undefined) {
                                // Check if the slider element still exists before updating
                                if (document.body.contains(slider)) {
                                   slider.value = data.value;
                                }
                            }
                            
                            // Trigger a UI refresh to show the updated value in other components
                            window.CacaoWS.requestServerRefresh();
                            
                        } catch (err) {
                            console.error('[CacaoCore] Error updating slider (debounced):', err);
                            // Remove overlay if it was added
                            // document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    }, 450); // Increased debounce to 450ms for smoother interaction
                }
            };

            // Use the 'input' event for continuous updates while dragging
            slider.addEventListener('input', updateValue);
            
            // Add mouseup event to ensure we always get a final update when the user releases the slider
            // This ensures the final value is captured even after quick drags
            const finalUpdate = async () => {
                // Clear any pending timeouts
                clearTimeout(updateTimeout);
                
                // Immediately send the final value
                try {
                    const action = component.props.onChange.action;
                    const params = {
                        ...component.props.onChange.params,
                        value: slider.value
                    };
                    
                    const queryParams = Object.entries(params)
                        .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
                        .join('&');
                    
                    console.log(`[CacaoCore] Sending final slider value: ${slider.value}`);
                    
                    const response = await fetch(`/api/event?event=${action}&${queryParams}&t=${Date.now()}`, {
                        method: 'GET',
                        headers: {
                            'Cache-Control': 'no-cache, no-store, must-revalidate'
                        }
                    });
                    
                    if (!response.ok) {
                        throw new Error(`Server returned ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    // Update slider value if needed
                    if (data.value !== undefined && document.body.contains(slider)) {
                        slider.value = data.value;
                    }
                    
                    // Always refresh UI on final update
                    window.CacaoWS.requestServerRefresh();
                    
                } catch (err) {
                    console.error('[CacaoCore] Error sending final slider value:', err);
                }
            };
            
            slider.addEventListener('mouseup', finalUpdate);
            slider.addEventListener('touchend', finalUpdate);
            
            return slider; // Return the created slider element
        },

        // --- INPUT COMPONENTS ---
        "input": (component) => {
            const el = document.createElement("input");
            el.type = component.props.inputType || "text";
            el.value = component.props.value || "";
            if (component.props.placeholder) el.placeholder = component.props.placeholder;
            if (component.props.disabled) el.disabled = true;
            if (component.props.style) Object.assign(el.style, component.props.style);
            if (component.props.className) el.className = component.props.className;
            // No onChange binding by default (add if needed)
            return el;
        },

        "search": (component) => {
            // Render as input[type=search] + button (or just input)
            const wrapper = document.createElement("div");
            wrapper.className = "search-input-wrapper";
            const input = document.createElement("input");
            input.type = "search";
            input.value = component.props.value || "";
            if (component.props.placeholder) input.placeholder = component.props.placeholder;
            if (component.props.disabled) input.disabled = true;
            if (component.props.style) Object.assign(input.style, component.props.style);
            if (component.props.className) input.className = component.props.className;
            wrapper.appendChild(input);
            // Optionally add a search button
            // const button = document.createElement("button");
            // button.textContent = "Search";
            // wrapper.appendChild(button);
            return wrapper;
        },

        "select": (component) => {
            const el = document.createElement("select");
            if (component.props.disabled) el.disabled = true;
            if (component.props.style) Object.assign(el.style, component.props.style);
            if (component.props.className) el.className = component.props.className;
            if (component.props.placeholder) {
                const placeholderOption = document.createElement("option");
                placeholderOption.value = "";
                placeholderOption.disabled = true;
                placeholderOption.selected = !component.props.value;
                placeholderOption.hidden = true;
                placeholderOption.textContent = component.props.placeholder;
                el.appendChild(placeholderOption);
            }
            if (Array.isArray(component.props.options)) {
                component.props.options.forEach(opt => {
                    const option = document.createElement("option");
                    option.value = opt.value;
                    option.textContent = opt.label;
                    if (component.props.value === opt.value) option.selected = true;
                    el.appendChild(option);
                });
            }
            return el;
        },

        "checkbox": (component) => {
            const wrapper = document.createElement("label");
            wrapper.className = "checkbox-wrapper";
            const input = document.createElement("input");
            input.type = "checkbox";
            input.checked = !!component.props.checked;
            if (component.props.disabled) input.disabled = true;
            if (component.props.style) Object.assign(input.style, component.props.style);
            if (component.props.className) input.className = component.props.className;
            wrapper.appendChild(input);
            if (component.props.label) {
                const span = document.createElement("span");
                span.textContent = component.props.label;
                wrapper.appendChild(span);
            }
            return wrapper;
        },

        "radio": (component) => {
            const wrapper = document.createElement("div");
            wrapper.className = "radio-group";
            if (Array.isArray(component.props.options)) {
                component.props.options.forEach(opt => {
                    const label = document.createElement("label");
                    label.className = "radio-wrapper";
                    const input = document.createElement("input");
                    input.type = "radio";
                    input.name = "radio-group-" + Math.random().toString(36).substr(2, 6);
                    input.value = opt.value;
                    if (component.props.value === opt.value) input.checked = true;
                    if (component.props.disabled) input.disabled = true;
                    label.appendChild(input);
                    const span = document.createElement("span");
                    span.textContent = opt.label;
                    label.appendChild(span);
                    wrapper.appendChild(label);
                });
            }
            return wrapper;
        },

        "switch": (component) => {
            // Styled checkbox
            const wrapper = document.createElement("label");
            wrapper.className = "switch-wrapper";
            const input = document.createElement("input");
            input.type = "checkbox";
            input.checked = !!component.props.checked;
            if (component.props.disabled) input.disabled = true;
            if (component.props.className) input.className = component.props.className;
            wrapper.appendChild(input);
            const slider = document.createElement("span");
            slider.className = "switch-slider";
            wrapper.appendChild(slider);
            return wrapper;
        },


        "datepicker": (component) => {
            const el = document.createElement("input");
            el.type = "date";
            if (component.props.value) el.value = component.props.value;
            if (component.props.disabled) el.disabled = true;
            if (component.props.style) Object.assign(el.style, component.props.style);
            if (component.props.className) el.className = component.props.className;
            return el;
        },

        "timepicker": (component) => {
            const el = document.createElement("input");
            el.type = "time";
            if (component.props.value) el.value = component.props.value;
            if (component.props.disabled) el.disabled = true;
            if (component.props.style) Object.assign(el.style, component.props.style);
            if (component.props.className) el.className = component.props.className;
            return el;
        },

        "upload": (component) => {
            const wrapper = document.createElement("div");
            wrapper.className = "upload-wrapper";
            const input = document.createElement("input");
            input.type = "file";
            if (component.props.multiple) input.multiple = true;
            if (component.props.disabled) input.disabled = true;
            if (component.props.style) Object.assign(input.style, component.props.style);
            if (component.props.className) input.className = component.props.className;
            wrapper.appendChild(input);
            return wrapper;
        },
        
        textarea: (component) => {
            const el = document.createElement("textarea");
            el.className = component.props.className || "textarea";
            
            // Apply content
            if (component.props.content) {
                el.value = component.props.content;
            }
            
            // Apply styles
            if (component.props.style) {
                Object.assign(el.style, component.props.style);
            }
            
            // Handle content changes
            if (component.props.action) {
                let updateTimeout;
                
                el.addEventListener("input", () => {
                    // Clear any existing timeout to debounce
                    clearTimeout(updateTimeout);
                    
                    // Set a timeout to avoid sending too many events
                    updateTimeout = setTimeout(async () => {
                        try {
                            const action = component.props.action;
                            const componentType = component.component_type || "textarea";
                            
                            // Build event data including the textarea content
                            const eventData = {
                                component_type: componentType,
                                content: el.value
                            };
                            
                            // Add the data property from the component if it exists
                            if (component.props.data) {
                                console.log("[Cacao] Including custom data in textarea event:", component.props.data);
                                Object.assign(eventData, component.props.data);
                            }
                            
                            console.log("[Cacao] Sending textarea content update:", action, eventData);
                            
                            // If WebSocket is open
                            if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                                window.socket.send(JSON.stringify({
                                    type: 'event',
                                    event: action,
                                    data: eventData
                                }));
                            } else {
                                // Fallback to HTTP
                                console.log("[Cacao] WebSocket not available, using HTTP fallback for textarea");
                                
                                // Build query parameters
                                let queryParams = `action=${action}&component_type=${componentType}`;
                                
                                // Add the data property from the component if it exists
                                if (component.props.data) {
                                    for (const [key, value] of Object.entries(component.props.data)) {
                                        queryParams += `&${key}=${encodeURIComponent(value)}`;
                                    }
                                }
                                
                                // Add content parameter
                                queryParams += `&content=${encodeURIComponent(el.value)}`;
                                
                                const response = await fetch(`/api/action?${queryParams}&t=${Date.now()}`, {
                                    method: 'GET',
                                    headers: {
                                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                                        'Pragma': 'no-cache',
                                        'Expires': '0'
                                    }
                                });
                                
                                if (!response.ok) {
                                    const errorText = await response.text();
                                    console.error("[Cacao] Server error response:", errorText);
                                    throw new Error(`Server returned ${response.status}: ${errorText}`);
                                }
                                
                                const responseData = await response.json();
                                console.log("[CacaoCore] Server response data:", responseData);
                            }
                        } catch (err) {
                            console.error('[CacaoCore] Error handling textarea input:', err);
                        }
                    }, 1000); // 1 second debounce
                });
            }
            
            return el;
        },
        // SLIDER (for type: "slider"),
        "slider": (component) => {
            const slider = document.createElement("input");
            slider.type = "range";
            return slider;
        },

        menu: (component) => {
            console.log("[CacaoCore] Rendering menu component:", component);
            const el = document.createElement("nav");
            el.className = "menu";

            // Add mode class (horizontal/vertical)
            if (component.props.mode === "horizontal") {
                el.classList.add("menu-horizontal");
            }

            // Apply custom styles
            if (component.props.style) {
                Object.assign(el.style, component.props.style);
            }

            // Create menu items
            if (Array.isArray(component.props.items)) {
                component.props.items.forEach(item => {
                    const menuItem = document.createElement("div");
                    menuItem.className = "menu-item";
                    
                    // Check if item is selected
                    if (component.props.selectedKeys &&
                        component.props.selectedKeys.includes(item.key)) {
                        menuItem.classList.add("selected");
                    }

                    // Add label content
                    applyContent(menuItem, item.label);

                    // Handle click events
                    menuItem.addEventListener("click", async (e) => {
                        e.preventDefault();
                        try {
                            console.log("[CacaoCore] Menu item clicked:", item.key);
                            
                            // Send menu selection event
                            const params = {
                                component_type: "menu",
                                key: item.key
                            };

                            const queryParams = Object.entries(params)
                                .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
                                .join("&");

                            const url = `/api/event?event=menu_select&${queryParams}&t=${Date.now()}`;
                            const response = await fetch(url, {
                                method: "GET",
                                headers: {
                                    "Cache-Control": "no-cache, no-store, must-revalidate"
                                }
                            });

                            if (response.ok) {
                                // Update visual selection immediately
                                el.querySelectorAll(".menu-item").forEach(mi => {
                                    mi.classList.remove("selected");
                                });
                                menuItem.classList.add("selected");

                                window.CacaoWS.requestServerRefresh();
                            } else {
                                console.error("[CacaoCore] Menu select failed:", response.status);
                            }
                        } catch (err) {
                            console.error("[CacaoCore] Error handling menu selection:", err);
                        }
                    });

                    el.appendChild(menuItem);
                });
            }

            // Add menu styles
            const style = document.createElement("style");
            style.textContent = `
                .menu {
                    font-size: 14px;
                    line-height: 1.5;
                    margin: 0;
                    padding: 0;
                    background: #fff;
                    border-bottom: 1px solid #f0f0f0;
                }

                .menu-horizontal {
                    display: flex;
                    flex-direction: row;
                }

                .menu-item {
                    padding: 12px 20px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    position: relative;
                    color: #595959;
                }

                .menu-item:hover {
                    color: #8B4513;
                }

                .menu-item.selected {
                    color: #8B4513;
                    font-weight: 500;
                }

                .menu-item.selected::after {
                    content: '';
                    position: absolute;
                    left: 20px;
                    right: 20px;
                    bottom: 0;
                    height: 2px;
                    background: #8B4513;
                }

                @media (max-width: 768px) {
                    .menu-horizontal {
                        overflow-x: auto;
                        -webkit-overflow-scrolling: touch;
                    }

                    .menu-item {
                        padding: 12px 16px;
                        white-space: nowrap;
                    }
                }
            `;
            el.appendChild(style);

            return el;
        },

        // SLIDER (for type: "slider"),
        "slider": (component) => {
            const slider = document.createElement("input");
            slider.type = "range";
            slider.className = component.props.className || "range-slider";
            slider.min = component.props.min;
            slider.max = component.props.max;
            slider.step = component.props.step;
            slider.value = component.props.value;

            let updateTimeout;
            const updateValue = async () => {
                if (component.props.onChange) {
                    clearTimeout(updateTimeout);
                    updateTimeout = setTimeout(async () => {
                        try {
                            // Optionally show overlay
                            // document.querySelector('.refresh-overlay').classList.add('active');
                            const action = component.props.onChange.action;
                            const params = {
                                ...component.props.onChange.params,
                                value: slider.value
                            };
                            const queryParams = Object.entries(params)
                                .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
                                .join('&');
                            const response = await fetch(`/api/event?event=${action}&${queryParams}&t=${Date.now()}`, {
                                method: 'GET',
                                headers: {
                                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                                }
                            });
                            if (!response.ok) {
                                throw new Error(`Server returned ${response.status}`);
                            }
                            const data = await response.json();
                            if (data.value !== undefined) {
                                slider.value = data.value;
                            }
                            window.CacaoWS.requestServerRefresh();
                        } catch (err) {
                            console.error('[CacaoCore] Error updating slider:', err);
                            // document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    }, 200);
                }
            };
            slider.addEventListener('input', updateValue);
            return slider;
        },

        // INTERACTIVE RATE (stars, supports half-stars)
        "rate": (component) => {
            const wrapper = document.createElement("div");
            wrapper.className = "rate-wrapper";
            const max = component.props.max || 5;
            let value = component.props.value || 0;
            let hoverValue = null;

            function renderStars() {
                wrapper.innerHTML = "";
                for (let i = 1; i <= max; i++) {
                    const star = document.createElement("span");
                    star.className = "rate-star";
                    // Half-star logic
                    let fill = false;
                    if (hoverValue !== null) {
                        fill = i <= Math.floor(hoverValue);
                        if (i === Math.ceil(hoverValue) && hoverValue % 1 >= 0.5) {
                            star.classList.add("half");
                        }
                    } else {
                        fill = i <= Math.floor(value);
                        if (i === Math.ceil(value) && value % 1 >= 0.5) {
                            star.classList.add("half");
                        }
                    }
                    if (fill) star.classList.add("filled");
                    star.textContent = "★";
                    // Mouse events for half-star
                    star.addEventListener("mousemove", (e) => {
                        const rect = star.getBoundingClientRect();
                        const x = e.clientX - rect.left;
                        hoverValue = x < rect.width / 2 ? i - 0.5 : i;
                        renderStars();
                    });
                    star.addEventListener("mouseleave", () => {
                        hoverValue = null;
                        renderStars();
                    });
                    star.addEventListener("click", (e) => {
                        const rect = star.getBoundingClientRect();
                        const x = e.clientX - rect.left;
                        value = x < rect.width / 2 ? i - 0.5 : i;
                        // Optionally: send event to backend here
                        // If you want to send to backend:
                        if (component.props.onChange) {
                            const action = component.props.onChange.action;
                            const params = {
                                ...component.props.onChange.params,
                                value: value
                            };
                            const queryParams = Object.entries(params)
                                .map(([key, val]) => `${key}=${encodeURIComponent(val)}`)
                                .join('&');
                            fetch(`/api/event?event=${action}&${queryParams}&t=${Date.now()}`, {
                                method: 'GET',
                                headers: {
                                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                                }
                            }).then(r => r.json()).then(data => {
                                if (data.value !== undefined) value = data.value;
                                window.CacaoWS.requestServerRefresh();
                            });
                        }
                        renderStars();
                    });
                    wrapper.appendChild(star);
                }
            }
            renderStars();
            return wrapper;
        },

        "range-sliders": (component) => {
            const container = document.createElement("div");
            container.className = "range-sliders-container";
            
            // Create sliders container
            const slidersContainer = document.createElement("div");
            slidersContainer.className = "sliders-wrapper";
            
            // Create lower slider
            const lowerSlider = document.createElement("input");
            lowerSlider.type = "range";
            lowerSlider.className = "range-slider lower";
            lowerSlider.min = component.props.min;
            lowerSlider.max = component.props.max;
            lowerSlider.step = component.props.step;
            lowerSlider.value = component.props.lowerValue;

            // Create upper slider
            const upperSlider = document.createElement("input");
            upperSlider.type = "range";
            upperSlider.className = "range-slider upper";
            upperSlider.min = component.props.min;
            upperSlider.max = component.props.max;
            upperSlider.step = component.props.step;
            upperSlider.value = component.props.upperValue;

            // Add value displays
            const lowerDisplay = document.createElement("div");
            lowerDisplay.className = "range-value lower";
            lowerDisplay.textContent = `$${component.props.lowerValue}`;

            const upperDisplay = document.createElement("div");
            upperDisplay.className = "range-value upper";
            upperDisplay.textContent = `$${component.props.upperValue}`;

            const rangeDisplay = document.createElement("div");
            rangeDisplay.className = "range-display";
            rangeDisplay.appendChild(lowerDisplay);
            rangeDisplay.appendChild(document.createTextNode(" - "));
            rangeDisplay.appendChild(upperDisplay);

           let updateTimeout;
           const updateValues = async () => {
               const lower = parseFloat(lowerSlider.value);
               const upper = parseFloat(upperSlider.value);
               
               // Ensure lower value doesn't exceed upper value and vice versa
               if (lower > upper) {
                   if (lowerSlider === document.activeElement) {
                       upperSlider.value = lower;
                   } else {
                       lowerSlider.value = upper;
                   }
               }
                
               // Update displays immediately
               lowerDisplay.textContent = `$${lowerSlider.value}`;
               upperDisplay.textContent = `$${upperSlider.value}`;

                if (component.props.onChange) {
                    clearTimeout(updateTimeout);
                    updateTimeout = setTimeout(async () => {
                        try {
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
                            const action = component.props.onChange.action;
                            const params = {
                                ...component.props.onChange.params,
                                lower_value: lowerSlider.value,
                                upper_value: upperSlider.value
                            };
                            
                            const queryParams = Object.entries(params)
                                .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
                                .join('&');
                                
                            const response = await fetch(`/api/event?event=${action}&${queryParams}&t=${Date.now()}`, {
                                method: 'GET',
                                headers: {
                                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                                }
                            });
                            
                            if (!response.ok) {
                                throw new Error(`Server returned ${response.status}`);
                            }
                            
                            const data = await response.json();
                            if (data.lower_value !== undefined) {
                                lowerSlider.value = data.lower_value;
                            }
                            if (data.upper_value !== undefined) {
                                upperSlider.value = data.upper_value;
                            }
                            window.CacaoWS.requestServerRefresh();
                        } catch (err) {
                            console.error('[CacaoCore] Error updating range:', err);
                            document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    }, 100); // Debounce updates
                }
            };

            // Add styles
            const styleEl = document.createElement('style');
            styleEl.textContent = `
                .range-sliders-container {
                    width: 100%;
                    padding: 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .sliders-wrapper {
                    width: 100%;
                    position: relative;
                    padding: 10px 0;
                }
                .range-slider {
                    width: 100%;
                    margin: 10px 0;
                    -webkit-appearance: none;
                    background: transparent;
                }
                .range-slider::-webkit-slider-thumb {
                    -webkit-appearance: none;
                    height: 24px;
                    width: 24px;
                    border-radius: 50%;
                    background: #ffffff;
                    cursor: pointer;
                    margin-top: -10px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                    border: 2px solid #D2691E;
                    transition: all 0.2s ease;
                }
                .range-slider::-webkit-slider-thumb:hover {
                    transform: scale(1.1);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                }
                .range-slider::-webkit-slider-runnable-track {
                    width: 100%;
                    height: 4px;
                    background: rgba(255,255,255,0.3);
                    border-radius: 2px;
                }
                .range-display {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 20px;
                    font-size: 20px;
                    color: #ffffff;
                    font-weight: bold;
                    text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
                }
                .range-value {
                    min-width: 60px;
                    text-align: center;
                    padding: 5px 10px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 15px;
                    margin: 0 10px;
                }
            `;
            
            container.appendChild(styleEl);
            slidersContainer.appendChild(lowerSlider);
            slidersContainer.appendChild(upperSlider);
            container.appendChild(slidersContainer);
            container.appendChild(rangeDisplay);

            lowerSlider.addEventListener('input', updateValues);
            upperSlider.addEventListener('input', updateValues);
            
            return container;
        }
    };

    /**
     * Main function that decides how to render a component.
     */
    function renderComponent(component) {
        // Basic validation
        if (!component || !component.type) {
            console.error("[CacaoCore] Invalid component:", component);
            const errorEl = document.createElement("div");
            errorEl.textContent = "Error: Invalid component";
            errorEl.style.color = "red";
            return errorEl;
        }

        let el;
        // 1. Special case for textarea - use our custom renderer
        if (component.type === "textarea") {
            console.log("[CacaoCore] Using custom textarea renderer");
            el = componentRenderers.textarea(component);
        }
        // 2. If there's a specialized renderer in componentRenderers, use it
        else if (componentRenderers[component.type]) {
            el = componentRenderers[component.type](component);
        }
        // 3. Else if it's a known standard HTML tag, use the fallback
        else if (STANDARD_TAGS.has(component.type)) {
            el = renderStandardElement(component);
        }
        // 3. Otherwise, fallback to raw JSON
        else {
            el = document.createElement("pre");
            el.textContent = JSON.stringify(component, null, 2);
        }

        // After we have the element, apply any custom classes/styles
        if (component.props?.className) {
            // If the renderer added a className already, append a space
            if (el.className) {
                el.className += ` ${component.props.className}`;
            } else {
                el.className = component.props.className;
            }
        }
        if (component.props?.style) {
            Object.assign(el.style, component.props.style);
        }

        // Store component type as a data-attribute if available
        if (component.component_type) {
            el.dataset.componentType = component.component_type;
        }

        return el;
    }

    /**
     * Renders the entire UI definition into #app.
     */
    function render(uiDefinition) {
        console.log("[CacaoCore] Rendering UI definition:", uiDefinition);
        
        // Skip if version unchanged and not forced
        if (uiDefinition._v === lastVersion && !uiDefinition._force && !uiDefinition.force) {
            console.log("[CacaoCore] Skipping render - same version");
            return;
        }
        lastVersion = uiDefinition._v;
        
        const app = document.getElementById("app");
        if (!app) {
            console.error("[CacaoCore] Could not find app container");
            return;
        }
        
        // Clear existing content
        while (app.firstChild) {
            app.removeChild(app.firstChild);
        }

        // If there's a layout with children or a div with children
        if ((uiDefinition.layout === 'column' || uiDefinition.type === 'div') && uiDefinition.children) {
            uiDefinition.children.forEach(child => {
                app.appendChild(renderComponent(child));
            });
        } else {
            // single component
            app.appendChild(renderComponent(uiDefinition));
        }
        
        console.log("[CacaoCore] UI rendered successfully");
        
        // Hide refresh overlay
        document.querySelector('.refresh-overlay').classList.remove('active');
    }

    // Handle browser back/forward buttons and initial hash
    window.addEventListener('hashchange', syncHashState);
    if (window.location.hash) {
        syncHashState();
    }

    // Expose CacaoCore globally
    window.CacaoCore = {
        render,
        clearCache: () => { 
            lastVersion = null; 
            errorCount = 0;  // Reset error count when cache is cleared
        }
    };
})();
