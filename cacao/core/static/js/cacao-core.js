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

    // Simple renderer that maps JSON UI definitions to HTML
    function renderComponent(component) {
        let el;
        switch(component.type) {
            case "navbar":
                el = document.createElement("nav");
                el.className = "navbar";
                el.innerHTML = `<div class="brand">${component.props.brand}</div>`;
                if(component.props.links) {
                    const linksDiv = document.createElement("div");
                    component.props.links.forEach(link => {
                        const a = document.createElement("a");
                        a.href = link.url;
                        a.textContent = link.name;
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
                el.innerHTML = `<h1>${component.props.title}</h1><p>${component.props.subtitle}</p>`;
                break;
            case "section":
                el = document.createElement("section");
                el.className = "section";
                
                // Store component type as a data attribute if available
                if (component.component_type) {
                    el.dataset.componentType = component.component_type;
                }
                
                if(component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "text":
                el = document.createElement("p");
                el.className = "text";
                el.textContent = component.props.content;
                break;
            case "button":
                el = document.createElement("button");
                el.className = "button";
                el.textContent = component.props.label;
                if(component.props.action) {
                    // Add click handler that sends action to server via GET
                    el.onclick = async () => {
                        try {
                            console.log("[Cacao] Sending action:", component.props.action);
                            
                            // Show refresh overlay
                            document.querySelector('.refresh-overlay').classList.add('active');
                            
                            // Find the parent component type
                            const parentSection = el.closest('section[data-component-type]');
                            const componentType = parentSection ? parentSection.dataset.componentType : 'unknown';
                            
                            // Use GET request with query parameters
                            const response = await fetch(`/api/action?action=${component.props.action}&component_type=${componentType}&t=${Date.now()}`, {
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
                            console.log("[Cacao] Server response data:", responseData);
                            
                            // Force UI refresh after action
                            window.CacaoWS.forceRefresh();
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
                el.textContent = component.props.text;
                break;
            case "column":
                el = document.createElement("div");
                el.className = "column";
                if(component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
                    });
                }
                break;
            case "grid":
                el = document.createElement("div");
                el.className = "grid";
                if(component.props.children && Array.isArray(component.props.children)) {
                    component.props.children.forEach(child => {
                        el.appendChild(renderComponent(child));
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
        if (uiDefinition._v === lastVersion && !uiDefinition._force) {
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

        // If there's a layout with children
        if (uiDefinition.layout === 'column' && uiDefinition.children) {
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

    // Expose CacaoCore globally
    window.CacaoCore = {
        render,
        clearCache: () => { 
            lastVersion = null; 
            errorCount = 0;  // Reset error count when cache is cleared
        }
    };
})();
