// Button Component Renderer
(component) => {
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
}