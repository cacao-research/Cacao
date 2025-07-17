// Radio component renderer
(component) => {
    const wrapper = document.createElement("div");
    wrapper.className = "radio-group";
    if (Array.isArray(component.props.options)) {
        component.props.options.forEach(opt => {
            const label = document.createElement("label");
            label.className = "radio-wrapper";
            const input = document.createElement("input");
            input.type = "radio";
            input.name = "radio-group-" + Math.random().toString(36).substr(2, 6);
            input.value = opt.value;
            if (component.props.value === opt.value) input.checked = true;
            if (component.props.disabled) input.disabled = true;
            label.appendChild(input);
            const span = document.createElement("span");
            span.textContent = opt.label;
            label.appendChild(span);
            wrapper.appendChild(label);
        });
    }
    return wrapper;
}