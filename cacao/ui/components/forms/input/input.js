// Input Component Renderer
(component) => {
    const el = document.createElement("input");
    el.type = component.props.inputType || "text";
    el.value = component.props.value || "";
    if (component.props.placeholder) el.placeholder = component.props.placeholder;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    // No onChange binding by default (add if needed)
    return el;
}