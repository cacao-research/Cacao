// Upload Component Renderer
(component) => {
    const wrapper = document.createElement("div");
    wrapper.className = "upload-wrapper";
    const input = document.createElement("input");
    input.type = "file";
    if (component.props.multiple) input.multiple = true;
    if (component.props.disabled) input.disabled = true;
    if (component.props.style) Object.assign(input.style, component.props.style);
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    return wrapper;
}