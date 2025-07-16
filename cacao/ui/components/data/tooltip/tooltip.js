(component) => {
    console.log("[CacaoCore] Rendering tooltip component:", component);
    
    // Create main wrapper element
    const wrapper = document.createElement("div");
    wrapper.className = "tooltip-wrapper";
    wrapper.style.position = "relative";
    wrapper.style.display = "inline-block";
    
    // Render the main content (trigger element)
    if (component.props.children) {
        if (typeof component.props.children === 'string') {
            wrapper.textContent = component.props.children;
        } else {
            wrapper.appendChild(window.CacaoCore.renderComponent(component.props.children));
        }
    }
    
    // Create tooltip element
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    tooltip.style.position = "absolute";
    tooltip.style.backgroundColor = "#333";
    tooltip.style.color = "white";
    tooltip.style.padding = "8px 12px";
    tooltip.style.borderRadius = "4px";
    tooltip.style.fontSize = "12px";
    tooltip.style.whiteSpace = "nowrap";
    tooltip.style.zIndex = "1000";
    tooltip.style.opacity = "0";
    tooltip.style.visibility = "hidden";
    tooltip.style.transition = "opacity 0.3s, visibility 0.3s";
    tooltip.style.pointerEvents = "none";
    
    // Set tooltip content
    tooltip.textContent = component.props.title || component.props.content || "Tooltip";
    
    // Position tooltip based on placement
    const placement = component.props.placement || "top";
    switch (placement) {
        case "top":
            tooltip.style.bottom = "100%";
            tooltip.style.left = "50%";
            tooltip.style.transform = "translateX(-50%)";
            tooltip.style.marginBottom = "8px";
            break;
        case "bottom":
            tooltip.style.top = "100%";
            tooltip.style.left = "50%";
            tooltip.style.transform = "translateX(-50%)";
            tooltip.style.marginTop = "8px";
            break;
        case "left":
            tooltip.style.right = "100%";
            tooltip.style.top = "50%";
            tooltip.style.transform = "translateY(-50%)";
            tooltip.style.marginRight = "8px";
            break;
        case "right":
            tooltip.style.left = "100%";
            tooltip.style.top = "50%";
            tooltip.style.transform = "translateY(-50%)";
            tooltip.style.marginLeft = "8px";
            break;
    }
    
    // Add event listeners for hover
    wrapper.addEventListener("mouseenter", () => {
        tooltip.style.opacity = "1";
        tooltip.style.visibility = "visible";
    });
    
    wrapper.addEventListener("mouseleave", () => {
        tooltip.style.opacity = "0";
        tooltip.style.visibility = "hidden";
    });
    
    wrapper.appendChild(tooltip);
    
    return wrapper;
}