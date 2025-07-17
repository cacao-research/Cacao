// Textarea Component Renderer
(component) => {
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
}