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
    
    // Debug mode configuration
    let debugMode = false;
    const DEBUG_PREFIX = "[CacaoCore Debug]";
    
    // Function availability tracking
    const REQUIRED_FUNCTIONS = ['renderChildren', 'applyContent', 'renderComponent'];
    
    /**
     * Debug logging function that only logs when debug mode is enabled
     * @param {string} message - The debug message
     * @param {any} data - Optional data to log
     */
    function debugLog(message, data = null) {
        if (debugMode) {
            if (data !== null) {
                console.log(DEBUG_PREFIX, message, data);
            } else {
                console.log(DEBUG_PREFIX, message);
            }
        }
    }
    
    /**
     * Enhanced error logging with context and suggestions
     * @param {string} context - Where the error occurred
     * @param {Error|string} error - The error that occurred
     * @param {Object} component - The component that caused the error (optional)
     * @param {Object} suggestions - Suggested fixes (optional)
     */
    function logDetailedError(context, error, component = null, suggestions = null) {
        const errorMessage = error instanceof Error ? error.message : error;
        console.error(`[CacaoCore Error] ${context}:`, errorMessage);
        
        if (component) {
            console.error("Component that failed:", component);
        }
        
        // Check for common scope-related issues
        if (errorMessage.includes('not defined') || errorMessage.includes('undefined')) {
            const missingFunction = errorMessage.match(/(\w+) is not defined/);
            if (missingFunction && REQUIRED_FUNCTIONS.includes(missingFunction[1])) {
                console.error("SCOPE ISSUE DETECTED:");
                console.error(`- Function '${missingFunction[1]}' is not accessible`);
                console.error("- This is likely a scope-related issue in auto-generated components");
                console.error("- Ensure window.CacaoCore exists and contains the required functions");
                console.error("- Try accessing functions via window.CacaoCore instead of direct references");
            }
        }
        
        if (suggestions) {
            console.error("Suggested fixes:", suggestions);
        }
        
        // Log current CacaoCore state for debugging
        if (window.CacaoCore) {
            console.error("Available CacaoCore functions:", Object.keys(window.CacaoCore));
        } else {
            console.error("CRITICAL: window.CacaoCore is not available!");
        }
    }
    
    /**
     * Validate that required functions are available in the global scope
     * @returns {Object} Validation result with missing functions
     */
    function validateFunctionAvailability() {
        const missing = [];
        const available = [];
        
        REQUIRED_FUNCTIONS.forEach(func => {
            if (window.CacaoCore && typeof window.CacaoCore[func] === 'function') {
                available.push(func);
            } else {
                missing.push(func);
            }
        });
        
        debugLog("Function availability check:", { available, missing });
        
        return {
            isValid: missing.length === 0,
            missing,
            available
        };
    }
    
    /**
     * Create a defensive wrapper for component rendering that validates scope
     * @param {Object} component - The component to render
     * @param {string} rendererType - Type of renderer being used
     * @returns {HTMLElement} The rendered element or error element
     */
    function safeComponentRender(component, rendererType) {
        try {
            // Validate function availability before rendering
            const validation = validateFunctionAvailability();
            if (!validation.isValid) {
                throw new Error(`Missing required functions: ${validation.missing.join(', ')}`);
            }
            
            debugLog(`Rendering component with ${rendererType} renderer:`, component);
            
            let el;
            if (rendererType === 'custom' && componentRenderers[component.type]) {
                el = componentRenderers[component.type](component);
            } else if (rendererType === 'standard' && STANDARD_TAGS.has(component.type)) {
                el = renderStandardElement(component);
            } else {
                throw new Error(`Unknown renderer type: ${rendererType}`);
            }
            
            debugLog(`Successfully rendered ${component.type} component`);
            return el;
            
        } catch (error) {
            logDetailedError(
                `Component rendering (${rendererType})`,
                error,
                component,
                {
                    "Check window.CacaoCore": "Ensure window.CacaoCore object exists and is properly initialized",
                    "Validate component structure": "Ensure component has required 'type' property",
                    "Check component renderer": `Verify ${component.type} renderer is properly defined`,
                    "Enable debug mode": "Set window.CacaoCore.setDebugMode(true) for more details"
                }
            );
            
            // Return a detailed error element
            const errorEl = document.createElement("div");
            errorEl.className = "cacao-error";
            errorEl.style.cssText = `
                color: #dc3545;
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                padding: 10px;
                margin: 5px 0;
                border-radius: 4px;
                font-family: monospace;
                font-size: 12px;
            `;
            errorEl.innerHTML = `
                <strong>Cacao Render Error:</strong><br>
                <strong>Component:</strong> ${component.type || 'unknown'}<br>
                <strong>Error:</strong> ${error.message}<br>
                <strong>Renderer:</strong> ${rendererType}<br>
                <small>Check console for detailed debugging information</small>
            `;
            return errorEl;
        }
    }

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
        if (!parent) {
            logDetailedError("renderChildren", "Parent element is null or undefined", null, {
                "Check parent element": "Ensure parent element exists before calling renderChildren"
            });
            return;
        }
        
        if (Array.isArray(childrenArray)) {
            debugLog(`Rendering ${childrenArray.length} children`);
            childrenArray.forEach((child, index) => {
                try {
                    const childElement = renderComponent(child);
                    if (childElement) {
                        parent.appendChild(childElement);
                        debugLog(`Child ${index} rendered successfully`);
                    } else {
                        logDetailedError("renderChildren", `Child ${index} rendered as null/undefined`, child);
                    }
                } catch (error) {
                    logDetailedError("renderChildren", `Failed to render child ${index}`, child, {
                        "Check child component": "Ensure child component has valid structure",
                        "Validate child type": "Ensure child.type is a recognized component type"
                    });
                    
                    // Create error placeholder for failed child
                    const errorEl = document.createElement("div");
                    errorEl.className = "cacao-child-error";
                    errorEl.style.cssText = "color: red; font-size: 12px; padding: 2px; border: 1px dashed red;";
                    errorEl.textContent = `Error rendering child ${index}: ${error.message}`;
                    parent.appendChild(errorEl);
                }
            });
        } else if (childrenArray !== undefined && childrenArray !== null) {
            logDetailedError("renderChildren", "childrenArray is not an array", childrenArray, {
                "Check children property": "Ensure children is an array or null/undefined"
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
        "thead", "tbody", "tr", "td", "th", // Table elements
        "img", "a", "label", "option", // Other common elements
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
        
    };

    /**
     * Main function that decides how to render a component.
     */
    function renderComponent(component) {
        // Enhanced validation with detailed error reporting
        if (!component) {
            logDetailedError("renderComponent", "Component is null or undefined", null, {
                "Check component input": "Ensure a valid component object is passed to renderComponent"
            });
            return createErrorElement("Invalid component: null or undefined");
        }
        
        if (!component.type) {
            logDetailedError("renderComponent", "Component missing required 'type' property", component, {
                "Add type property": "Ensure component object has a 'type' property",
                "Check component structure": "Verify component follows expected format: { type: 'componentName', props: {...} }"
            });
            return createErrorElement(`Invalid component: missing 'type' property`);
        }

        // Validate window.CacaoCore exists and has required functions
        if (!window.CacaoCore) {
            logDetailedError("renderComponent", "window.CacaoCore is not available", component, {
                "Initialize CacaoCore": "Ensure cacao-core.js has loaded and window.CacaoCore is initialized",
                "Check script loading": "Verify cacao-core.js is included before component rendering"
            });
            return createErrorElement("CacaoCore not initialized");
        }

        debugLog("Starting component render:", { type: component.type, hasProps: !!component.props });

        let el;
        try {
            // 1. Special case for textarea - use our custom renderer
            if (component.type === "textarea") {
                debugLog("Using custom textarea renderer");
                if (!componentRenderers.textarea) {
                    throw new Error("textarea renderer not found in componentRenderers");
                }
                el = safeComponentRender(component, 'custom');
            }
            // 2. If there's a specialized renderer in componentRenderers, use it
            else if (componentRenderers[component.type]) {
                debugLog(`Using custom renderer for ${component.type}`);
                el = safeComponentRender(component, 'custom');
            }
            // 3. Else if it's a known standard HTML tag, use the fallback
            else if (STANDARD_TAGS.has(component.type)) {
                debugLog(`Using standard renderer for ${component.type}`);
                el = safeComponentRender(component, 'standard');
            }
            // 4. Otherwise, fallback to raw JSON with warning
            else {
                logDetailedError("renderComponent", `Unknown component type: ${component.type}`, component, {
                    "Add component renderer": `Add a renderer for '${component.type}' in componentRenderers object`,
                    "Check component type": `Verify '${component.type}' is a valid component type`,
                    "Use standard HTML tag": "If this should be a standard HTML element, add it to STANDARD_TAGS"
                });
                
                el = document.createElement("pre");
                el.className = "cacao-unknown-component";
                el.style.cssText = "background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 5px; font-family: monospace; font-size: 12px;";
                el.textContent = `Unknown component type: ${component.type}\n\n${JSON.stringify(component, null, 2)}`;
            }

            // After we have the element, apply any custom classes/styles
            if (el && component.props?.className) {
                // If the renderer added a className already, append a space
                if (el.className) {
                    el.className += ` ${component.props.className}`;
                } else {
                    el.className = component.props.className;
                }
                debugLog("Applied custom className:", component.props.className);
            }
            
            if (el && component.props?.style) {
                Object.assign(el.style, component.props.style);
                debugLog("Applied custom styles:", component.props.style);
            }

            // Store component type as a data-attribute if available
            if (el && component.component_type) {
                el.dataset.componentType = component.component_type;
            }

            debugLog(`Successfully rendered component: ${component.type}`);
            return el;
            
        } catch (error) {
            logDetailedError("renderComponent", `Failed to render component ${component.type}`, component, {
                "Check component renderer": `Verify ${component.type} renderer is properly implemented`,
                "Validate component props": "Ensure component props are valid and complete",
                "Enable debug mode": "Set window.CacaoCore.setDebugMode(true) for detailed logging"
            });
            
            return createErrorElement(`Failed to render ${component.type}: ${error.message}`);
        }
    }
    
    /**
     * Helper function to create consistent error elements
     * @param {string} message - Error message to display
     * @returns {HTMLElement} Error element
     */
    function createErrorElement(message) {
        const errorEl = document.createElement("div");
        errorEl.className = "cacao-error";
        errorEl.style.cssText = `
            color: #dc3545;
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 8px 12px;
            margin: 4px 0;
            border-radius: 4px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 14px;
            line-height: 1.4;
        `;
        errorEl.innerHTML = `<strong>Cacao Error:</strong> ${message}`;
        return errorEl;
    }

    /**
     * Renders the entire UI definition into #app.
     */
    function render(uiDefinition) {
        debugLog("Starting UI render with definition:", uiDefinition);
        
        try {
            // Enhanced validation
            if (!uiDefinition) {
                logDetailedError("render", "UI definition is null or undefined", null, {
                    "Check server response": "Ensure server returns valid UI definition",
                    "Verify data flow": "Check that UI data is properly passed to render function"
                });
                return;
            }
            
            // Skip if version unchanged and not forced
            if (uiDefinition._v === lastVersion && !uiDefinition._force && !uiDefinition.force) {
                debugLog("Skipping render - same version:", lastVersion);
                return;
            }
            lastVersion = uiDefinition._v;
            
            const app = document.getElementById("app");
            if (!app) {
                logDetailedError("render", "Could not find app container element", null, {
                    "Check HTML structure": "Ensure an element with id='app' exists in the DOM",
                    "Verify DOM ready": "Make sure DOM is fully loaded before calling render"
                });
                return;
            }
            
            debugLog("Clearing existing app content");
            
            // Clear existing content safely
            try {
                while (app.firstChild) {
                    app.removeChild(app.firstChild);
                }
            } catch (clearError) {
                logDetailedError("render", "Error clearing app content", clearError);
                // Try alternative clearing method
                app.innerHTML = '';
            }

            // Render content with error handling
            try {
                if ((uiDefinition.layout === 'column' || uiDefinition.type === 'div') && uiDefinition.children) {
                    debugLog(`Rendering ${uiDefinition.children.length} child components`);
                    uiDefinition.children.forEach((child, index) => {
                        try {
                            const childElement = renderComponent(child);
                            if (childElement) {
                                app.appendChild(childElement);
                                debugLog(`Successfully rendered child ${index}`);
                            } else {
                                logDetailedError("render", `Child ${index} rendered as null`, child);
                            }
                        } catch (childError) {
                            logDetailedError("render", `Failed to render child ${index}`, child, {
                                "Check child structure": "Ensure child component has valid structure",
                                "Skip broken children": "Consider adding error boundaries for individual components"
                            });
                            
                            // Add error placeholder for failed child
                            const errorEl = createErrorElement(`Failed to render child component ${index}`);
                            app.appendChild(errorEl);
                        }
                    });
                } else {
                    // single component
                    debugLog("Rendering single component:", uiDefinition.type);
                    const element = renderComponent(uiDefinition);
                    if (element) {
                        app.appendChild(element);
                    } else {
                        logDetailedError("render", "Single component rendered as null", uiDefinition);
                    }
                }
                
                debugLog("UI rendered successfully");
                console.log("[CacaoCore] UI rendered successfully");
                
            } catch (renderError) {
                logDetailedError("render", "Error during component rendering", renderError, {
                    "Check component definitions": "Verify all components are properly defined",
                    "Enable debug mode": "Set window.CacaoCore.setDebugMode(true) for detailed logging",
                    "Check browser console": "Review console for additional error details"
                });
                
                // Show error message in app
                const errorEl = createErrorElement("Failed to render UI components. Check console for details.");
                app.appendChild(errorEl);
            }
            
        } catch (generalError) {
            logDetailedError("render", "General rendering error", generalError, {
                "Check error details": "Review the specific error message for guidance",
                "Reload page": "Try refreshing the page if the error persists",
                "Check server status": "Verify the application server is running properly"
            });
            
            // Last resort error display
            const app = document.getElementById("app");
            if (app) {
                app.innerHTML = `
                    <div style="color: red; padding: 20px; text-align: center; font-family: sans-serif;">
                        <h3>Cacao Rendering Error</h3>
                        <p>Failed to render the application. Please check the browser console for details.</p>
                        <button onclick="window.location.reload()" style="padding: 10px 20px; margin-top: 10px;">
                            Reload Page
                        </button>
                    </div>
                `;
            }
        } finally {
            // Always try to hide refresh overlay
            try {
                const overlay = document.querySelector('.refresh-overlay');
                if (overlay) {
                    overlay.classList.remove('active');
                }
            } catch (overlayError) {
                // Ignore overlay errors
                debugLog("Error hiding refresh overlay:", overlayError);
            }
        }
    }

    // Handle browser back/forward buttons and initial hash
    window.addEventListener('hashchange', syncHashState);
    if (window.location.hash) {
        syncHashState();
    }

    // Expose CacaoCore globally
    window.CacaoCore = {
        render,
        componentRenderers,
        renderComponent,
        renderChildren,
        applyContent,
        clearCache: () => {
            lastVersion = null;
            errorCount = 0;  // Reset error count when cache is cleared
            debugLog("Cache cleared and error count reset");
        },
        
        // Debug and error handling functions
        setDebugMode: (enabled) => {
            debugMode = enabled;
            console.log(`[CacaoCore] Debug mode ${enabled ? 'enabled' : 'disabled'}`);
        },
        
        getDebugMode: () => debugMode,
        
        validateFunctionAvailability,
        
        // Utility functions for external debugging
        debugLog,
        logDetailedError,
        createErrorElement,
        
        // Version and status information
        getVersion: () => "1.0.0-enhanced",
        getStatus: () => ({
            lastVersion,
            errorCount,
            debugMode,
            functionsAvailable: validateFunctionAvailability()
        }),
        
        // Manual error reporting for external components
        reportError: (context, error, component = null, suggestions = null) => {
            logDetailedError(context, error, component, suggestions);
        }
    };
    
    // Initialize with improved error boundary
    try {
        // Validate that all required functions are properly exposed
        const validation = validateFunctionAvailability();
        if (!validation.isValid) {
            console.warn("[CacaoCore] Some functions may not be properly exposed:", validation.missing);
        } else {
            debugLog("CacaoCore initialized successfully with all required functions");
        }
        
        // Add global error handler for uncaught component errors
        window.addEventListener('error', function(event) {
            if (event.error && event.error.stack && event.error.stack.includes('renderComponent')) {
                logDetailedError(
                    "Uncaught component error",
                    event.error,
                    null,
                    {
                        "Check component structure": "Verify all component objects have valid structure",
                        "Enable debug mode": "Call window.CacaoCore.setDebugMode(true) for detailed logging",
                        "Check console": "Review browser console for additional error details"
                    }
                );
            }
        });
        
    } catch (initError) {
        console.error("[CacaoCore] Initialization error:", initError);
    }
    
})();
