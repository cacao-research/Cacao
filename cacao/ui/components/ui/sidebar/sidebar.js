// Sidebar component renderer
(component) => {
    const el = document.createElement("div");
    el.className = "sidebar";
    
    // Apply styles from props
    if (component.props?.style) {
        Object.assign(el.style, component.props.style);
    }
    if (component.props?.content) {
        applyContent(el, component.props.content);
    }
    if (component.children) {
        renderChildren(el, component.children);
    } else if (component.props?.children) {
        renderChildren(el, component.props.children);
    }
    return el;
}