/*
  cacao-core.js
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
        
        // For pre elements, always use textContent to preserve raw text
        if (el.tagName === 'PRE') {
            el.textContent = content;
            return;
        }
        
        // For all other elements, check for icon markup
        if (hasIconMarkup(content)) {
            el.innerHTML = content;
        } else {
            el.textContent = content;
        }
    }

    // Simple renderer that maps JSON UI definitions to HTML
    function renderComponent(component) {
        if (!component || !component.type) {
            console.error("[CacaoCore] Invalid component:", component);
            const errorEl = document.createElement("div");
            errorEl.textContent = "Error: Invalid component";
            errorEl.style.color = "red";
            return errorEl;
        }
        
        console.log("[CacaoCore] Rendering component:", component.type);
        let el;
        
        switch(component.type) {
            case "navbar":
                el = document.createElement("nav");
                el.className = "navbar";
                
                if (component.props.brand) {
                    const brandDiv = document.createElement("div");
                    brandDiv.className = "brand";
                    applyContent(brandDiv, component.props.brand);
                    el.appendChild(brandDiv);
                }
                
                if(component.props.links) {
                    const linksDiv = document.createElement("div");
                    component.props.links.forEach(link => {
                        const a = document.createElement("a");
                        a.href = link.url;
                        applyContent(a, link.name);
                        linksDiv.appendChild(a);
                    });
                    el.appendChild(linksDiv);
                }
                break;
            case "hero":
                el = document.createElement("section");
                el.className = "hero";
                if (component.props.backgroundImage) {
                    el.style.backgroundImage = `url(${component.props.backgroundImage})`;
                }
                
                const heroTitle = document.createElement("h1");
                applyContent(heroTitle, component.props.title);
                el.appendChild(heroTitle);
                
                const heroSubtitle = document.createElement("p");
                applyContent(heroSubtitle, component.props.subtitle);
                el.appendChild(heroSubtitle);
                break;
            case "section":
            case "div":
            case "main":
                el = document.createElement(
                    component.type === 'section' ? 'section' : 
                    component.type === 'main' ? 'main' : 
                    'div'
                );
                el.className = component.type === 'section' ? "section" : 
                               component.type === 'main' ? "content-area" : "";
                
                // Store component type as a data attribute if available
                if (component.component_type) {
                    el.dataset.componentType = component.component_type;
                }
                
                // Check for direct content
                if (component.props.content) {
                    applyContent(el, component.props.content);
                }
                
                // Add children
                if(component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "text":
                el = document.createElement("p");
                el.className = "text";
                applyContent(el, component.props.content);
                break;
            case "sidebar":
                el = document.createElement("div");
                el.className = "sidebar";
                
                // Apply styles from props
                if (component.props && component.props.style) {
                    Object.assign(el.style, component.props.style);
                }
                
                // Check for direct content
                if (component.props && component.props.content) {
                    applyContent(el, component.props.content);
                }
                
                // Add children if available
                if(component.props && component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "nav-item":
                el = document.createElement("div");
                el.className = "nav-item";
                
                // Process children if available
                if (component.props && component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                } else {
                    // Legacy rendering for backward compatibility
                    // Add icon if available
                    if (component.props && component.props.icon) {
                        const iconSpan = document.createElement("span");
                        applyContent(iconSpan, component.props.icon); // Apply icon content with icon handling
                        iconSpan.style.marginRight = "8px";
                        el.appendChild(iconSpan);
                    }
                    
                    // Add label
                    if (component.props && component.props.label) {
                        const labelSpan = document.createElement("span");
                        applyContent(labelSpan, component.props.label);
                        el.appendChild(labelSpan);
                    }
                }
                
                // Apply active styles if active
                if (component.props && component.props.isActive) {
                    el.classList.add("active");
                }
                
                // Add click handler for navigation
                if (component.props && component.props.onClick) {
                    el.onclick = async () => {
                        try {
                            // Show refresh overlay
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
                            const action = component.props.onClick.action;
                            const state = component.props.onClick.state;
                            const value = component.props.onClick.value;
                            const immediate = component.props.onClick.immediate === true;
                            
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
                            
                            // Update URL if this is a page navigation
                            if (state === 'current_page') {
                                const newPage = value;
                                window.location.hash = newPage;
                            }
                            
                            // Check if this is an immediate action that requires UI refresh
                            if (data.immediate === true) {
                                console.log("[CacaoCore] Immediate action detected, fetching UI directly");
                                
                                // Fetch UI directly instead of using requestServerRefresh
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
                                console.log("[CacaoCore] Immediate UI update:", uiData);
                                window.CacaoCore.render(uiData);
                            } else {
                                // Force UI refresh after action (standard behavior)
                                window.CacaoWS.requestServerRefresh();
                            }
                        } catch (err) {
                            console.error('[CacaoCore] Error handling nav item click:', err);
                            // Hide refresh overlay on error
                            document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    };
                }
                break;
            case "h1":
            case "h2":
            case "h3":
            case "h4":
            case "h5":
            case "h6":
                el = document.createElement(component.type);
                applyContent(el, component.props.content);
                break;
            case "p":
                el = document.createElement("p");
                applyContent(el, component.props.content);
                break;
            case "li":
                el = document.createElement("li");
                applyContent(el, component.props.content);
                
                // Handle list item children if present
                if (component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "pre":
                el = document.createElement("pre");
                // Always use textContent for pre elements to preserve raw text
                if (component.props.content) {
                    el.textContent = component.props.content;
                }
                
                // Apply styles if provided
                if (component.props.style) {
                    Object.assign(el.style, component.props.style);
                }
                break;
            case "header":
                el = document.createElement("header");
                el.className = "header";
                if (component.props.title) {
                    const headerTitle = document.createElement("h1");
                    applyContent(headerTitle, component.props.title);
                    el.appendChild(headerTitle);
                }
                if (component.props.subtitle) {
                    const headerSubtitle = document.createElement("p");
                    applyContent(headerSubtitle, component.props.subtitle);
                    el.appendChild(headerSubtitle);
                }
                break;
            case "container":
                el = document.createElement("div");
                el.className = "container";
                if (component.props.maxWidth) {
                    el.style.maxWidth = component.props.maxWidth;
                }
                if (component.props.padding) {
                    el.style.padding = component.props.padding;
                }
                
                // Check for direct content
                if (component.props.content) {
                    applyContent(el, component.props.content);
                }
                
                if (component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "card":
                el = document.createElement("div");
                el.className = "card";
                if (component.props.title) {
                    const cardTitle = document.createElement("h2");
                    cardTitle.className = "card-title";
                    applyContent(cardTitle, component.props.title);
                    el.appendChild(cardTitle);
                }
                if (component.props.children && Array.isArray(component.props.children)) {
                    const cardContent = document.createElement("div");
                    cardContent.className = "card-content";
                    component.props.children.forEach(child => {
                        cardContent.appendChild(renderComponent(child));
                    });
                    el.appendChild(cardContent);
                }
                break;
            case "ul":
            case "list":
                el = document.createElement("ul");
                el.className = component.type === "list" ? "list" : "";
                
                // Handle direct content if present (rare, but supported)
                if (component.props.content) {
                    applyContent(el, component.props.content);
                }
                
                if (component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "task-item":
                el = document.createElement("li");
                el.className = "task-item";
                el.dataset.id = component.props.id;
                
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.checked = component.props.completed;
                if (component.props.onToggle) {
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
                break;
            case "button":
                el = document.createElement("button");
                el.className = "button";
                applyContent(el, component.props.label);
                
                if(component.props.action) {
                    // Add click handler that sends action to server via GET
                    el.onclick = async () => {
                        try {
                            console.log("[Cacao] Sending event:", component.props.on_click || component.props.action);
                            
                            // Show refresh overlay
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
                            // Find the parent component type
                            const parentSection = el.closest('section[data-component-type]');
                            const componentType = parentSection ? parentSection.dataset.componentType : 'unknown';
                            
                            // Check if WebSocket is available
                            if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                                // Use WebSocket for real-time event
                                const eventName = component.props.on_click || component.props.action;
                                console.log("[Cacao] Sending WebSocket event:", eventName);
                                
                                // Send event via WebSocket
                                window.socket.send(JSON.stringify({
                                    type: 'event',
                                    event: eventName,
                                    data: {
                                        component_type: componentType
                                    }
                                }));
                            } else {
                                // Fallback to HTTP request
                                console.log("[Cacao] WebSocket not available, using HTTP fallback");
                                const action = component.props.on_click || component.props.action;
                                
                                // Use GET request with query parameters
                                const response = await fetch(`/api/action?action=${action}&component_type=${componentType}&t=${Date.now()}`, {
                                    method: 'GET',
                                    headers: {
                                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                                        'Pragma': 'no-cache',
                                        'Expires': '0'
                                    }
                                });
                                
                                console.log("[Cacao] Server response status:", response.status);
                                
                                if (!response.ok) {
                                    const errorText = await response.text();
                                    console.error("[Cacao] Server error response:", errorText);
                                    throw new Error(`Server returned ${response.status}: ${errorText}`);
                                }
                                
                                const responseData = await response.json();
                                console.log("[CacaoCore] Server response data:", responseData);
                                
                                // Force UI refresh after action
                                window.CacaoWS.requestServerRefresh();
                            }
                        } catch (err) {
                            console.error('Error handling action:', err);
                            
                            // Hide refresh overlay
                            document.querySelector('.refresh-overlay').classList.remove('active');
                            
                            // Limit error alerts
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
                break;
            case "footer":
                el = document.createElement("footer");
                el.className = "footer";
                applyContent(el, component.props.text);
                break;
            case "column":
                el = document.createElement("div");
                el.className = "column";
                
                // Check for direct content
                if (component.props.content) {
                    applyContent(el, component.props.content);
                }
                
                if(component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "grid":
                el = document.createElement("div");
                el.className = "grid";
                
                // Check for direct content
                if (component.props.content) {
                    applyContent(el, component.props.content);
                }
                
                if(component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "form":
                el = document.createElement("form");
                el.className = "form";
                // Prevent default form submission
                el.onsubmit = (e) => e.preventDefault();
                
                // Check for direct content
                if (component.props.content) {
                    applyContent(el, component.props.content);
                }
                
                if(component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "input":
                el = document.createElement("input");
                el.className = "input";
                
                if (component.props.value !== undefined) {
                    el.value = component.props.value;
                }
                
                if (component.props.placeholder) {
                    el.placeholder = component.props.placeholder;
                }
                
                if (component.props.onChange) {
                    el.addEventListener("input", async (e) => {
                        try {
                            const value = e.target.value;
                            
                            // Show refresh overlay for consistent UX
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
                            const response = await fetch(`/api/action?action=${component.props.onChange}&component_type=input&value=${encodeURIComponent(value)}&t=${Date.now()}`, {
                                method: 'GET',
                                headers: {
                                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                                }
                            });
                            
                            if (!response.ok) {
                                throw new Error(`Server returned ${response.status}`);
                            }
                            
                            // Request UI refresh
                            window.CacaoWS.requestServerRefresh();
                        } catch (err) {
                            console.error('[CacaoCore] Error handling input change:', err);
                            document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    });
                }
                break;
            default:
                // Fallback: display raw JSON
                el = document.createElement("pre");
                el.textContent = JSON.stringify(component, null, 2);
        }
        
        // Add any custom classes
        if (component.props && component.props.className) {
            el.className += ` ${component.props.className}`;
        }
        
        // Add any custom styles
        if (component.props && component.props.style) {
            Object.assign(el.style, component.props.style);
        }
        
        return el;
    }

    function render(uiDefinition) {
        console.log("[CacaoCore] Rendering UI definition:", uiDefinition);
        
        // Check if this is a new version
        // For hot reloads, we should always render even if the version is the same
        // The force flag can be set to true to force rendering
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
