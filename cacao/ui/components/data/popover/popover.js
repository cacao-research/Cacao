(component) => {
    console.log("[CacaoCore] Rendering popover component:", component);
    
    // Create main wrapper element
    const wrapper = document.createElement("div");
    wrapper.className = "popover-wrapper";
    wrapper.style.position = "relative";
    wrapper.style.display = "inline-block";
    
    // Render the trigger element
    const trigger = document.createElement("span");
    trigger.className = "popover-trigger";
    trigger.style.cursor = "pointer";
    
    if (component.props.children) {
        if (typeof component.props.children === 'string') {
            trigger.textContent = component.props.children;
        } else {
            trigger.appendChild(window.CacaoCore.renderComponent(component.props.children));
        }
    } else {
        trigger.textContent = "Click me";
    }
    
    // Create popover element
    const popover = document.createElement("div");
    popover.className = "popover";
    popover.style.position = "absolute";
    popover.style.backgroundColor = "white";
    popover.style.border = "1px solid #ccc";
    popover.style.borderRadius = "4px";
    popover.style.boxShadow = "0 2px 8px rgba(0,0,0,0.15)";
    popover.style.padding = "12px";
    popover.style.minWidth = "200px";
    popover.style.maxWidth = "300px";
    popover.style.zIndex = "1000";
    popover.style.display = "none";
    
    // Add popover content
    const content = document.createElement("div");
    content.className = "popover-content";
    
    if (component.props.title) {
        const title = document.createElement("div");
        title.className = "popover-title";
        title.style.fontWeight = "bold";
        title.style.marginBottom = "8px";
        title.textContent = component.props.title;
        content.appendChild(title);
    }
    
    if (component.props.content) {
        const body = document.createElement("div");
        body.className = "popover-body";
        if (typeof component.props.content === 'string') {
            body.textContent = component.props.content;
        } else {
            body.appendChild(window.CacaoCore.renderComponent(component.props.content));
        }
        content.appendChild(body);
    }
    
    popover.appendChild(content);
    
    // Position popover based on placement
    const placement = component.props.placement || "bottom";
    switch (placement) {
        case "top":
            popover.style.bottom = "100%";
            popover.style.left = "50%";
            popover.style.transform = "translateX(-50%)";
            popover.style.marginBottom = "8px";
            break;
        case "bottom":
            popover.style.top = "100%";
            popover.style.left = "50%";
            popover.style.transform = "translateX(-50%)";
            popover.style.marginTop = "8px";
            break;
        case "left":
            popover.style.right = "100%";
            popover.style.top = "50%";
            popover.style.transform = "translateY(-50%)";
            popover.style.marginRight = "8px";
            break;
        case "right":
            popover.style.left = "100%";
            popover.style.top = "50%";
            popover.style.transform = "translateY(-50%)";
            popover.style.marginLeft = "8px";
            break;
    }
    
    // Add click handler to toggle popover
    let isVisible = false;
    trigger.addEventListener("click", (e) => {
        e.stopPropagation();
        isVisible = !isVisible;
        popover.style.display = isVisible ? "block" : "none";
    });
    
    // Hide popover when clicking outside
    document.addEventListener("click", (e) => {
        if (!wrapper.contains(e.target) && isVisible) {
            isVisible = false;
            popover.style.display = "none";
        }
    });
    
    wrapper.appendChild(trigger);
    wrapper.appendChild(popover);
    
    return wrapper;
}