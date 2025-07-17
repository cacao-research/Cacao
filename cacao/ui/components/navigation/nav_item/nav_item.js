// Sidebar component renderer
(component) => {
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
}