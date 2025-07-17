// Checkbox component renderer
(component) => {
    const wrapper = document.createElement("label");
    wrapper.className = "checkbox-wrapper";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = !!component.props.checked;
    if (component.props.disabled) input.disabled = true;
    if (component.props.style) Object.assign(input.style, component.props.style);
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    if (component.props.label) {
        const span = document.createElement("span");
        span.textContent = component.props.label;
        wrapper.appendChild(span);
    }
    return wrapper;
}