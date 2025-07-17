// Select Component Renderer
(component) => {
    const el = document.createElement("select");
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    if (component.props.placeholder) {
        const placeholderOption = document.createElement("option");
        placeholderOption.value = "";
        placeholderOption.disabled = true;
        placeholderOption.selected = !component.props.value;
        placeholderOption.hidden = true;
        placeholderOption.textContent = component.props.placeholder;
        el.appendChild(placeholderOption);
    }
    if (Array.isArray(component.props.options)) {
        component.props.options.forEach(opt => {
            const option = document.createElement("option");
            option.value = opt.value;
            option.textContent = opt.label;
            if (component.props.value === opt.value) option.selected = true;
            el.appendChild(option);
        });
    }
    return el;
}