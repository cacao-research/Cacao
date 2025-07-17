(component) => {
    console.log("[CacaoCore] Rendering tree_viewer component:", component);
    const tree = document.createElement('div');
    tree.className = 'tree_viewer';
    
    // Extract props
    const expandAll = component.props.expand_all || false;
    const onNodeClick = component.props.on_node_click;
    const data = component.props.data;
    const theme = component.props.theme || 'light';
    
    // Apply theme class
    tree.classList.add(`theme-${theme}`);
    
    // Set ID if provided
    if (component.props.id) {
        tree.id = component.props.id;
    }

    function renderNode(key, value, parent) {
        const node = document.createElement('div');
        node.className = 'tree-node';
        const isObject = value !== null && typeof value === 'object';

        // toggle handle
        const toggle = document.createElement('span');
        toggle.className = 'tree-expand-toggle';
        toggle.textContent = isObject ? (expandAll ? '▼' : '▶') : '';
        node.appendChild(toggle);

        // key
        const keySpan = document.createElement('span');
        keySpan.className = 'tree-key';
        keySpan.textContent = key;
        node.appendChild(keySpan);

        node.appendChild(document.createTextNode(':'));

        // primitive value
        if (!isObject) {
            const val = document.createElement('span');
            val.className = 'tree-value';
            val.textContent = JSON.stringify(value);
            node.appendChild(val);
        }

        // children
        if (isObject) {
            const childrenWrapper = document.createElement('div');
            childrenWrapper.className = 'tree-children';
            if (!expandAll) {
                childrenWrapper.style.display = 'none';
                node.classList.add('collapsed');
            }
            Object.entries(value).forEach(([k, v]) =>
                renderNode(k, v, childrenWrapper)
            );
            node.appendChild(childrenWrapper);

            toggle.addEventListener('click', () => {
                const collapsed = node.classList.toggle('collapsed');
                childrenWrapper.style.display = collapsed ? 'none' : 'block';
                toggle.textContent = collapsed ? '▶' : '▼';
            });
        }

        // optional click event
        if (onNodeClick) {
            keySpan.style.cursor = 'pointer';
            keySpan.addEventListener('click', () => {
                const evt = new CustomEvent(onNodeClick, { detail: { key } });
                tree.dispatchEvent(evt);
            });
        }

        parent.appendChild(node);
    }

    if (typeof data === 'object' && data !== null) {
        Object.entries(data).forEach(([k, v]) => renderNode(k, v, tree));
    }
    
    return tree;
}
