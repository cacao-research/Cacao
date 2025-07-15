(component) => {
    console.log("[CacaoCore] Rendering badge component:", component);
    const wrapper = document.createElement("span");
    wrapper.className = "badge-wrapper";

    // Render the main content if provided
    if (component.props.children) {
        wrapper.appendChild(window.CacaoCore.renderComponent(component.props.children));
    }

    // Create the badge element
    const badge = document.createElement("span");
    badge.className = "badge";

    // Handle dot style badge
    if (component.props.dot) {
        badge.classList.add("dot");
    } else if (component.props.count !== undefined) {
        // Show count if not zero or showZero is true
        if (component.props.count > 0 || component.props.showZero) {
            badge.textContent = component.props.count;
        }
    }

    wrapper.appendChild(badge);
    return wrapper;
}