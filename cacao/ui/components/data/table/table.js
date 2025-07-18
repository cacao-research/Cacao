// Merged Table Component JavaScript Renderer for Cacao Framework
// Supports both simple native rendering and advanced DataTables.js functionality
(component) => {
    console.log("[CacaoCore] Rendering merged table component:", component);
    
    const props = component.props;
    const isAdvanced = props.advanced === true;
    const tableId = `table-${Math.random().toString(36).substr(2, 9)}`;
    
    // Create wrapper div
    const wrapper = document.createElement("div");
    wrapper.className = isAdvanced ? "datatable-wrapper" : "table-wrapper";
    
    // Create table element
    const table = document.createElement("table");
    table.id = tableId;
    table.className = isAdvanced ? 
        (props.css_classes || "display table table-striped table-hover") : 
        "table";
    
    if (isAdvanced) {
        table.style.width = "100%";
    }
    
    // Create table header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    
    props.columns.forEach(column => {
        const th = document.createElement("th");
        th.textContent = column.title || column.label || "";
        
        if (column.width) {
            th.style.width = column.width;
        }
        
        // Add sorting capability for simple mode
        if (!isAdvanced && props.sorting) {
            th.classList.add("sortable");
            th.onclick = () => {
                console.log("[CacaoCore] Sort by:", column.dataIndex || column.key);
                // Simple sorting logic could be implemented here
            };
        }
        
        headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create table body
    const tbody = document.createElement("tbody");
    
    // For simple mode, populate table body immediately
    if (!isAdvanced && Array.isArray(props.dataSource)) {
        props.dataSource.forEach(row => {
            const tr = document.createElement("tr");
            props.columns.forEach(column => {
                const td = document.createElement("td");
                const dataIndex = column.dataIndex || column.key;
                td.textContent = row[dataIndex] || '';
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }
    
    table.appendChild(tbody);
    
    // Create table footer if needed for advanced mode
    if (isAdvanced && props.show_footer) {
        const tfoot = document.createElement("tfoot");
        const footerRow = document.createElement("tr");
        
        props.columns.forEach(column => {
            const th = document.createElement("th");
            th.textContent = column.title || column.label || "";
            footerRow.appendChild(th);
        });
        
        tfoot.appendChild(footerRow);
        table.appendChild(tfoot);
    }
    
    wrapper.appendChild(table);
    
    // Add simple pagination for simple mode
    if (!isAdvanced && props.pagination) {
        const pagination = document.createElement("div");
        pagination.className = "table-pagination";
        
        // Create simple pagination UI
        const paginationInfo = document.createElement("span");
        paginationInfo.className = "pagination-info";
        paginationInfo.textContent = `Page ${props.pagination.current || 1} of ${Math.ceil(props.dataSource.length / (props.pagination.page_size || 10))}`;
        
        const paginationControls = document.createElement("div");
        paginationControls.className = "pagination-controls";
        
        const prevBtn = document.createElement("button");
        prevBtn.textContent = "Previous";
        prevBtn.onclick = () => console.log("[CacaoCore] Previous page");
        
        const nextBtn = document.createElement("button");
        nextBtn.textContent = "Next";
        nextBtn.onclick = () => console.log("[CacaoCore] Next page");
        
        paginationControls.appendChild(prevBtn);
        paginationControls.appendChild(nextBtn);
        
        pagination.appendChild(paginationInfo);
        pagination.appendChild(paginationControls);
        wrapper.appendChild(pagination);
    }
    
    // Advanced mode: Load DataTables.js assets and initialize
    if (isAdvanced) {
        loadDataTablesAssets(props).then(() => {
            initializeDataTable(tableId, props, wrapper);
        });
    }
    
    return wrapper;
    
    // === DataTables.js Asset Loading Functions ===
    
    function loadDataTablesAssets(props) {
        return new Promise((resolve) => {
            // Check if DataTables is already loaded
            if (window.jQuery && window.jQuery.fn.DataTable) {
                resolve();
                return;
            }
            
            const assetsToLoad = [];
            
            // Load jQuery if not present
            if (!window.jQuery) {
                assetsToLoad.push(loadScript('https://code.jquery.com/jquery-3.7.0.min.js'));
            }
            
            // Load DataTables CSS
            if (!document.querySelector('link[href*="datatables"]')) {
                assetsToLoad.push(loadCSS(getDataTablesCSS(props.theme)));
            }
            
            // Load DataTables JS
            assetsToLoad.push(loadScript('https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js'));
            
            // Load theme-specific assets
            if (props.theme === 'bootstrap5') {
                assetsToLoad.push(loadScript('https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js'));
            } else if (props.theme === 'bootstrap4') {
                assetsToLoad.push(loadScript('https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap4.min.js'));
            }
            
            // Load additional features based on configuration
            if (props.datatables_config && props.datatables_config.responsive) {
                assetsToLoad.push(loadScript('https://cdn.datatables.net/responsive/2.5.0/js/dataTables.responsive.min.js'));
                assetsToLoad.push(loadCSS('https://cdn.datatables.net/responsive/2.5.0/css/responsive.dataTables.min.css'));
            }
            
            if (props.datatables_config && props.datatables_config.fixedHeader) {
                assetsToLoad.push(loadScript('https://cdn.datatables.net/fixedheader/3.4.0/js/dataTables.fixedHeader.min.js'));
                assetsToLoad.push(loadCSS('https://cdn.datatables.net/fixedheader/3.4.0/css/fixedHeader.dataTables.min.css'));
            }
            
            if (props.datatables_config && props.datatables_config.select) {
                assetsToLoad.push(loadScript('https://cdn.datatables.net/select/1.7.0/js/dataTables.select.min.js'));
                assetsToLoad.push(loadCSS('https://cdn.datatables.net/select/1.7.0/css/select.dataTables.min.css'));
            }
            
            if (props.datatables_config && props.datatables_config.buttons) {
                assetsToLoad.push(loadScript('https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js'));
                assetsToLoad.push(loadScript('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'));
                assetsToLoad.push(loadScript('https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js'));
                assetsToLoad.push(loadScript('https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js'));
                assetsToLoad.push(loadScript('https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js'));
                assetsToLoad.push(loadScript('https://cdn.datatables.net/buttons/2.4.2/js/buttons.print.min.js'));
                assetsToLoad.push(loadCSS('https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css'));
            }
            
            Promise.all(assetsToLoad).then(() => {
                // Wait a bit for all scripts to be parsed
                setTimeout(resolve, 100);
            });
        });
    }
    
    function initializeDataTable(tableId, props, wrapper) {
        try {
            const $ = window.jQuery;
            const config = { ...props.datatables_config };
            
            // Add event handlers
            if (props.on_row_click) {
                config.rowCallback = function(row, data, index) {
                    $(row).on('click', function() {
                        // Send event to server
                        if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
                            window.socket.send(JSON.stringify({
                                type: 'event',
                                event: props.on_row_click,
                                data: { row_data: data, row_index: index }
                            }));
                        }
                    });
                };
            }
            
            // Initialize DataTable
            const dataTable = $(`#${tableId}`).DataTable(config);
            
            // Store reference for potential future access
            wrapper._dataTable = dataTable;
            
            // Handle server-side events
            if (props.server_side && props.ajax_url) {
                dataTable.on('xhr', function() {
                    console.log('[DataTable] Data loaded from server');
                });
            }
            
            console.log('[CacaoCore] DataTable initialized successfully');
            
        } catch (error) {
            console.error('[CacaoCore] Error initializing DataTable:', error);
            
            // Fallback: create a basic HTML table
            if (!props.server_side && props.dataSource) {
                const tbody = wrapper.querySelector('tbody');
                tbody.innerHTML = '';
                props.dataSource.forEach(row => {
                    const tr = document.createElement('tr');
                    props.columns.forEach(column => {
                        const td = document.createElement('td');
                        const dataIndex = column.dataIndex || column.key;
                        td.textContent = row[dataIndex] || '';
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
            }
        }
    }
    
    function getDataTablesCSS(theme) {
        const baseUrl = 'https://cdn.datatables.net/1.13.7/css/';
        switch (theme) {
            case 'bootstrap5':
                return baseUrl + 'dataTables.bootstrap5.min.css';
            case 'bootstrap4':
                return baseUrl + 'dataTables.bootstrap4.min.css';
            case 'material':
                return baseUrl + 'dataTables.material.min.css';
            default:
                return baseUrl + 'jquery.dataTables.min.css';
        }
    }
    
    function loadScript(src) {
        return new Promise((resolve, reject) => {
            // Check if script already exists
            if (document.querySelector(`script[src="${src}"]`)) {
                resolve();
                return;
            }
            
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    function loadCSS(href) {
        return new Promise((resolve) => {
            // Check if CSS already exists
            if (document.querySelector(`link[href="${href}"]`)) {
                resolve();
                return;
            }
            
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.onload = resolve;
            document.head.appendChild(link);
        });
    }
};