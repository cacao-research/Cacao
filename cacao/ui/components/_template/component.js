// Template for creating new Cacao components
// Copy this file to your component directory and modify as needed

// Component renderer function
(component) => {
    // Create the main element
    const el = document.createElement("div");
    el.className = "your-component-name";
    
    // Handle component props
    if (component.props?.className) {
        el.className += " " + component.props.className;
    }
    
    if (component.props?.style) {
        Object.assign(el.style, component.props.style);
    }
    
    // Handle component content
    if (component.props?.content) {
        // This will be auto-transformed to window.CacaoCore.applyContent()
        applyContent(el, component.props.content);
    }
    
    // Handle component children
    if (component.children) {
        // This will be auto-transformed to window.CacaoCore.renderChildren()
        renderChildren(el, component.children);
    } else if (component.props?.children) {
        // This will be auto-transformed to window.CacaoCore.renderChildren()
        renderChildren(el, component.props.children);
    }
    
    // Handle nested components
    if (component.props?.nestedComponent) {
        // This will be auto-transformed to window.CacaoCore.renderComponent()
        const nestedEl = renderComponent(component.props.nestedComponent);
        el.appendChild(nestedEl);
    }
    
    // Add event listeners if needed
    if (component.props?.onClick) {
        el.addEventListener('click', component.props.onClick);
    }
    
    // Return the completed element
    return el;
}