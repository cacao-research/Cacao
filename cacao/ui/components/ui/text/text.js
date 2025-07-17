// Text component renderer
(component) => {
    const el = document.createElement("p");
    el.className = "text";
    applyContent(el, component.props.content);
    return el;
}