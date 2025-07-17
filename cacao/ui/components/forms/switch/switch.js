// Switch component renderer
(component) => {
    // Styled checkbox
    const wrapper = document.createElement("label");
    wrapper.className = "switch-wrapper";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = !!component.props.checked;
    if (component.props.disabled) input.disabled = true;
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    const slider = document.createElement("span");
    slider.className = "switch-slider";
    wrapper.appendChild(slider);
    return wrapper;
}