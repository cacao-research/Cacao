(component) => {
    console.log("[CacaoCore] Rendering descriptions component:", component);
    const el = document.createElement("div");
    el.className = "descriptions";
    
    // Add bordered class if specified
    if (component.props.bordered) {
        el.classList.add("bordered");
    }

    // Add columns class if specified
    if (component.props.column) {
        el.classList.add(`columns-${component.props.column}`);
    }

    // Add title if provided
    if (component.props.title) {
        const titleDiv = document.createElement("div");
        titleDiv.className = "descriptions-title";
        titleDiv.textContent = component.props.title;
        el.appendChild(titleDiv);
    }

    // Create items wrapper
    const itemsWrapper = document.createElement("div");
    itemsWrapper.className = "descriptions-items";

    // Add items
    if (Array.isArray(component.props.items)) {
        component.props.items.forEach(item => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "descriptions-item";

            const labelDiv = document.createElement("div");
            labelDiv.className = "descriptions-label";
            labelDiv.textContent = item.label;
            itemDiv.appendChild(labelDiv);

            const contentDiv = document.createElement("div");
            contentDiv.className = "descriptions-content";
            if (typeof item.content === 'string') {
                contentDiv.textContent = item.content;
            } else {
                contentDiv.appendChild(window.CacaoCore.renderComponent(item.content));
            }
            itemDiv.appendChild(contentDiv);

            itemsWrapper.appendChild(itemDiv);
        });
    }

    el.appendChild(itemsWrapper);

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .descriptions {
            width: 100%;
            font-size: 14px;
        }

        .descriptions.bordered {
            border: 1px solid #e8e8e8;
            border-radius: 4px;
        }

        .descriptions-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            padding: 16px;
            border-bottom: 1px solid #e8e8e8;
        }

        .descriptions-items {
            padding: 16px;
            display: grid;
            grid-gap: 16px;
        }

        .descriptions.columns-2 .descriptions-items {
            grid-template-columns: repeat(2, 1fr);
        }

        .descriptions-item {
            display: flex;
            flex-direction: column;
        }

        .descriptions-label {
            color: #666;
            margin-bottom: 4px;
        }

        .descriptions-content {
            color: #333;
        }

        .descriptions.bordered .descriptions-items {
            border-radius: 0 0 4px 4px;
        }
    `;
    el.appendChild(style);

    return el;
}