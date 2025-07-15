(component) => {
    console.log("[CacaoCore] Rendering enhanced table component:", component);
    const wrapper = document.createElement("div");
    wrapper.className = "table-wrapper";

    const table = document.createElement("table");
    table.className = "table";

    // Create header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    component.props.columns.forEach(column => {
        const th = document.createElement("th");
        th.textContent = column.title;
        if (component.props.sorting) {
            th.classList.add("sortable");
            th.onclick = () => {
                // Sorting logic would go here
                console.log("[CacaoCore] Sort by:", column.key);
            };
        }
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create body
    const tbody = document.createElement("tbody");
    if (Array.isArray(component.props.dataSource)) {
        component.props.dataSource.forEach(row => {
            const tr = document.createElement("tr");
            component.props.columns.forEach(column => {
                const td = document.createElement("td");
                td.textContent = row[column.dataIndex];
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
    table.appendChild(tbody);

    wrapper.appendChild(table);

    // Add pagination if specified
    if (component.props.pagination) {
        const pagination = document.createElement("div");
        pagination.className = "table-pagination";
        // Pagination UI would go here
        wrapper.appendChild(pagination);
    }

    return wrapper;
}