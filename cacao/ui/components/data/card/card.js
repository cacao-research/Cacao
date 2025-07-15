(component) => {
    console.log("[CacaoCore] Rendering card component:", component);
    const el = document.createElement("div");
    el.className = "card";
    if (component.props.bordered) el.classList.add("bordered");

    if (component.props.title) {
        const header = document.createElement("div");
        header.className = "card-header";
        const title = document.createElement("div");
        title.className = "card-title";
        title.textContent = component.props.title;
        header.appendChild(title);

        if (component.props.extra) {
            const extra = document.createElement("div");
            extra.className = "card-extra";
            if (typeof component.props.extra === 'string') {
                extra.textContent = component.props.extra;
            } else {
                extra.appendChild(window.CacaoCore.renderComponent(component.props.extra));
            }
            header.appendChild(extra);
        }

        el.appendChild(header);
    }

    const content = document.createElement("div");
    content.className = "card-content";
    if (typeof component.props.children === 'string') {
        content.textContent = component.props.children;
    } else if (Array.isArray(component.props.children)) {
        component.props.children.forEach(child => {
            content.appendChild(window.CacaoCore.renderComponent(child));
        });
    } else if (component.props.children) {
        content.appendChild(window.CacaoCore.renderComponent(component.props.children));
    }
    el.appendChild(content);

    return el;
}