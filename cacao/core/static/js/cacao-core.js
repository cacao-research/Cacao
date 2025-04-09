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
                            window.socket.send(JSON.stringify({
                                type: 'event',
                                event: eventName,
                                data: { component_type: componentType }
                            }));
                        } else {
                            // Fallback to HTTP
                            console.log("[Cacao] WebSocket not available, using HTTP fallback");
                            const action = component.props.on_click || component.props.action;
                            const response = await fetch(`/api/action?action=${action}&component_type=${componentType}&t=${Date.now()}`, {
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

        "slider": (component) => {
            const slider = document.createElement("input");
            slider.type = "range";
            slider.className = "range-slider";
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
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
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
                            document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    }, 100); // Debounce updates
                }
            };

            slider.addEventListener('input', updateValue);
            return slider;
        },

        "slider": (component) => {
            const slider = document.createElement("input");
            slider.type = "range";
            slider.className = "range-slider";
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
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
                            const action = component.props.onChange.action;
                            const params = {
                                ...component.props.onChange.params,
                                value: slider.value
                            };

                            // If WebSocket is open
                            if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                                console.log("[Cacao] Sending WebSocket event:", action);
                                window.socket.send(JSON.stringify({
                                    type: 'event',
                                    event: action,
                                    data: params
                                }));
                            } else {
                                // Fallback to HTTP
                                console.log("[Cacao] WebSocket not available, using HTTP fallback");
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
                            }
                        } catch (err) {
                            console.error('[CacaoCore] Error updating slider:', err);
                            document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    }, 100); // Debounce updates
                }
            };

            slider.addEventListener('input', updateValue);
            return slider;
        },

        "slider": (component) => {
            const slider = document.createElement("input");
            slider.type = "range";
            slider.className = "range-slider";
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
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
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
                            document.querySelector('.refresh-overlay').classList.remove('active');
                        }
                    }, 100); // Debounce updates
                }
            };

            slider.addEventListener('input', updateValue);
            return slider;
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
        // 1. If there's a specialized renderer in componentRenderers, use it
        if (componentRenderers[component.type]) {
            el = componentRenderers[component.type](component);
        }
        // 2. Else if it's a known standard HTML tag, use the fallback
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
