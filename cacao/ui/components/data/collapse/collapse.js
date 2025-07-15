(component) => {
    console.log("[CacaoCore] Rendering collapse component:", component);
    
    // Create main element
    const el = document.createElement("div");
    el.className = "collapse";
    el.style.border = "1px solid #ddd";
    el.style.borderRadius = "4px";
    el.style.marginBottom = "8px";
    
    // Track collapse state
    let isCollapsed = component.props.defaultCollapsed !== false;
    
    // Create header (trigger)
    const header = document.createElement("div");
    header.className = "collapse-header";
    header.style.padding = "12px 16px";
    header.style.backgroundColor = "#f8f9fa";
    header.style.borderBottom = "1px solid #ddd";
    header.style.cursor = "pointer";
    header.style.display = "flex";
    header.style.alignItems = "center";
    header.style.justifyContent = "space-between";
    header.style.userSelect = "none";
    
    // Add header title
    const headerTitle = document.createElement("div");
    headerTitle.className = "collapse-title";
    headerTitle.style.fontWeight = "500";
    headerTitle.textContent = component.props.title || "Collapse";
    header.appendChild(headerTitle);
    
    // Add collapse indicator
    const indicator = document.createElement("div");
    indicator.className = "collapse-indicator";
    indicator.style.fontSize = "12px";
    indicator.style.transition = "transform 0.2s ease";
    indicator.innerHTML = "▼";
    header.appendChild(indicator);
    
    // Create content area
    const content = document.createElement("div");
    content.className = "collapse-content";
    content.style.overflow = "hidden";
    content.style.transition = "max-height 0.3s ease, opacity 0.3s ease";
    
    // Create content wrapper
    const contentWrapper = document.createElement("div");
    contentWrapper.className = "collapse-content-wrapper";
    contentWrapper.style.padding = "16px";
    
    // Add content
    if (component.props.children) {
        if (typeof component.props.children === 'string') {
            contentWrapper.textContent = component.props.children;
        } else if (Array.isArray(component.props.children)) {
            component.props.children.forEach(child => {
                contentWrapper.appendChild(window.CacaoCore.renderComponent(child));
            });
        } else {
            contentWrapper.appendChild(window.CacaoCore.renderComponent(component.props.children));
        }
    } else {
        contentWrapper.innerHTML = `
            <div style="color: #666; font-style: italic;">
                Collapse content goes here...
            </div>
        `;
    }
    
    content.appendChild(contentWrapper);
    
    // Function to update collapse state
    const updateCollapse = () => {
        if (isCollapsed) {
            content.style.maxHeight = "0";
            content.style.opacity = "0";
            content.style.borderTop = "none";
            indicator.style.transform = "rotate(-90deg)";
        } else {
            content.style.maxHeight = contentWrapper.scrollHeight + "px";
            content.style.opacity = "1";
            content.style.borderTop = "1px solid #ddd";
            indicator.style.transform = "rotate(0deg)";
        }
    };
    
    // Add click handler to header
    header.addEventListener("click", () => {
        isCollapsed = !isCollapsed;
        updateCollapse();
    });
    
    // Add keyboard support
    header.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            isCollapsed = !isCollapsed;
            updateCollapse();
        }
    });
    
    // Make header focusable
    header.setAttribute("tabindex", "0");
    header.setAttribute("role", "button");
    header.setAttribute("aria-expanded", !isCollapsed);
    
    // Add hover effect
    header.addEventListener("mouseenter", () => {
        header.style.backgroundColor = "#e9ecef";
    });
    
    header.addEventListener("mouseleave", () => {
        header.style.backgroundColor = "#f8f9fa";
    });
    
    // Assemble component
    el.appendChild(header);
    el.appendChild(content);
    
    // Set initial state
    updateCollapse();
    
    return el;
}