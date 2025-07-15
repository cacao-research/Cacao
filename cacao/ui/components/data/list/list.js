(component) => {
    console.log("[CacaoCore] Rendering list component:", component);
    const el = document.createElement("div");
    el.className = "list";
    if (component.props.bordered) el.classList.add("bordered");
    if (component.props.size) el.classList.add(component.props.size);

    if (Array.isArray(component.props.items)) {
        component.props.items.forEach(item => {
            const itemEl = document.createElement("div");
            itemEl.className = "list-item";
            
            if (item.title) {
                const title = document.createElement("div");
                title.className = "list-item-title";
                title.textContent = item.title;
                itemEl.appendChild(title);
            }

            if (item.description) {
                const desc = document.createElement("div");
                desc.className = "list-item-description";
                desc.textContent = item.description;
                itemEl.appendChild(desc);
            }

            el.appendChild(itemEl);
        });
    }

    return el;
}