// Datepicker Component Renderer
(component) => {
    const el = document.createElement("input");
    el.type = "date";
    if (component.props.value) el.value = component.props.value;
    if (component.props.disabled) el.disabled = true;
    if (component.props.style) Object.assign(el.style, component.props.style);
    if (component.props.className) el.className = component.props.className;
    return el;
}