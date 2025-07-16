(component) => {
    console.log("[CacaoCore] Rendering tag component:", component);
    const el = document.createElement("span");
    el.className = "tag";
    
    if (component.props.color) {
        el.classList.add(`tag-${component.props.color}`);
        el.style.backgroundColor = component.props.color;
    }

    if (component.props.content) {
        el.textContent = component.props.content;
    }

    if (component.props.closable) {
        const closeBtn = document.createElement("span");
        closeBtn.className = "tag-close";
        closeBtn.innerHTML = "×";
        closeBtn.onclick = (e) => {
            e.stopPropagation();
            el.remove();
        };
        el.appendChild(closeBtn);
    }

    return el;
}