(component) => {
    console.log("[CacaoCore] Rendering avatar component:", component);
    const el = document.createElement("span");
    el.className = "avatar";
    
    if (component.props.shape) {
        el.classList.add(component.props.shape);
    }
    if (component.props.size) {
        el.classList.add(component.props.size);
    }

    if (component.props.src) {
        const img = document.createElement("img");
        img.src = component.props.src;
        img.alt = "Avatar";
        el.appendChild(img);
    } else if (component.props.icon) {
        const icon = document.createElement("span");
        icon.className = "avatar-icon";
        applyContent(icon, component.props.icon);
        el.appendChild(icon);
    }

    return el;
}