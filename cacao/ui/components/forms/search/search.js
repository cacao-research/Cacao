// Search Component Renderer
(component) => {
    // Render as input[type=search] + button (or just input)
    const wrapper = document.createElement("div");
    wrapper.className = "search-input-wrapper";
    const input = document.createElement("input");
    input.type = "search";
    input.value = component.props.value || "";
    if (component.props.placeholder) input.placeholder = component.props.placeholder;
    if (component.props.disabled) input.disabled = true;
    if (component.props.style) Object.assign(input.style, component.props.style);
    if (component.props.className) input.className = component.props.className;
    wrapper.appendChild(input);
    // Optionally add a search button
    // const button = document.createElement("button");
    // button.textContent = "Search";
    // wrapper.appendChild(button);
    return wrapper;
}