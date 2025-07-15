(component) => {
    console.log("[CacaoCore] Rendering timeline component:", component);
    const el = document.createElement("div");
    el.className = "timeline";
    
    if (component.props.mode) {
        el.classList.add(`timeline-${component.props.mode}`);
    }
    
    if (component.props.reverse) {
        el.classList.add("timeline-reverse");
    }

    if (Array.isArray(component.props.items)) {
        const items = component.props.reverse ?
            [...component.props.items].reverse() :
            component.props.items;
            
        items.forEach(item => {
            const itemEl = document.createElement("div");
            itemEl.className = "timeline-item";

            // Add dot
            const dot = document.createElement("div");
            dot.className = "timeline-dot";
            itemEl.appendChild(dot);

            // Add label if provided
            if (item.label) {
                const label = document.createElement("div");
                label.className = "timeline-label";
                label.textContent = item.label;
                itemEl.appendChild(label);
            }

            // Add content
            const content = document.createElement("div");
            content.className = "timeline-content";
            if (typeof item.content === 'string') {
                content.textContent = item.content;
            } else {
                content.appendChild(window.CacaoCore.renderComponent(item.content));
            }
            itemEl.appendChild(content);

            el.appendChild(itemEl);
        });
    }

    return el;
}