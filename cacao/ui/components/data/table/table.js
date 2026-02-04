// Merged Table Component JavaScript Renderer for Cacao Framework
// Supports both simple native rendering and advanced DataTables.js functionality

// === Global Filter Panel Functions ===
// These functions must be globally available for onclick handlers

window.closeFilterPanel = function(tableId) {
    const panel = document.getElementById(`filter-panel-${tableId}`);
    const overlay = document.getElementById(`filter-overlay-${tableId}`);
    if (panel && overlay) {
        closeFilterPanel(panel, overlay);
    }
};

// Global filter state storage
window.cacaoTableFilters = window.cacaoTableFilters || {};

window.applyAdvancedFilters = function(tableId) {
    console.log('[DEBUG] ==> applyAdvancedFilters called for tableId:', tableId);
    
    const table = document.getElementById(tableId);
    const wrapper = table ? table.closest('.datatable-wrapper') : null;
    
    console.log('[DEBUG] DOM elements found:', {
        table: !!table,
        wrapper: !!wrapper,
        dataTable: wrapper ? !!wrapper._dataTable : false
    });
    
    if (!table || !wrapper || !wrapper._dataTable) {
        console.error('[DEBUG] EARLY EXIT: DataTable not found for advanced filters');
        console.log('[DEBUG] Available table IDs:', Array.from(document.querySelectorAll('table')).map(t => t.id));
        return;
    }
    
    const dataTable = window.jQuery(`#${tableId}`).DataTable();
    const panel = document.getElementById(`filter-panel-${tableId}`);
    const toggleBtn = wrapper._filterToggle;
    
    console.log('[DEBUG] DataTable instance obtained:', !!dataTable);
    console.log('[DEBUG] Filter panel found:', !!panel);
    
    if (!panel) {
        console.error('[DEBUG] EARLY EXIT: Filter panel not found! Expected ID:', `filter-panel-${tableId}`);
        console.log('[DEBUG] Available filter panels:', Array.from(document.querySelectorAll('[id*="filter-panel"]')).map(p => p.id));
        return;
    }
    
    // Collect filter values with enhanced debugging
    const filters = {};
    const filterInputs = panel.querySelectorAll('[id^="filter-"]');
    let hasActiveFilters = false;
    
    console.log('[DEBUG] Found filter inputs:', filterInputs.length);
    console.log('[DEBUG] Filter input IDs:', Array.from(filterInputs).map(input => ({id: input.id, value: input.value, type: input.type})));
    
    filterInputs.forEach(input => {
        console.log('[DEBUG] Processing filter input:', input.id, 'value:', input.value);
        const idParts = input.id.split('-');
        console.log('[DEBUG] ID parts:', idParts);
        
        if (idParts.length >= 4) {
            // Fixed column name extraction - handle split tableId
            // Expected format: filter-table-{randomId}-{columnName}-{fieldType}
            // idParts: ['filter', 'table', 'randomId', 'columnName', 'fieldType']
            
            if (idParts[0] !== 'filter' || idParts[1] !== 'table') {
                console.warn('[DEBUG] Unexpected ID format:', input.id);
                return;
            }
            
            // Extract parts after 'table-randomId'
            const columnParts = idParts.slice(3, -1); // Skip 'filter', 'table', 'randomId' and fieldType
            const columnName = columnParts.join('-');
            const fieldType = idParts[idParts.length - 1];
            
            console.log('[DEBUG] Extracted:', {columnName, fieldType, idParts});
            
            if (fieldType === 'type') {
                // Skip type selectors
                return;
            }
            
            if (fieldType === 'min' || fieldType === 'max') {
                // Range filter
                console.log('[DEBUG] Range filter processing:', {columnName, fieldType, value: input.value});
                
                if (input.value && input.value.trim() !== '') {
                    if (!filters[columnName]) {
                        filters[columnName] = { type: 'range' };
                    }
                    filters[columnName][fieldType] = input.value.trim();
                    hasActiveFilters = true;
                    console.log('[DEBUG] ✅ Added range filter:', columnName, filters[columnName]);
                } else {
                    console.log('[DEBUG] ❌ Skipping empty range filter:', columnName, fieldType);
                }
            } else if (fieldType === 'value') {
                // Regular filter
                const typeSelect = document.getElementById(`filter-${tableId}-${columnName}-type`);
                const filterType = typeSelect ? typeSelect.value : 'contains';
                
                console.log('[DEBUG] Regular filter processing:');
                console.log('[DEBUG] - Column:', columnName);
                console.log('[DEBUG] - Input value:', input.value);
                console.log('[DEBUG] - Filter type:', filterType);
                console.log('[DEBUG] - Type select found:', !!typeSelect);
                
                if (input.value && input.value.trim() !== '') {
                    filters[columnName] = {
                        type: filterType,
                        value: input.value.trim()
                    };
                    hasActiveFilters = true;
                    console.log('[DEBUG] ✅ Added filter for column:', columnName, filters[columnName]);
                } else {
                    console.log('[DEBUG] ❌ Skipping empty filter for column:', columnName);
                }
            }
        }
    });
    
    // Store filters globally for use by DataTable AJAX function
    window.cacaoTableFilters[tableId] = filters;
    
    // Update toggle button state
    if (toggleBtn) {
        if (hasActiveFilters) {
            toggleBtn.classList.add('has-filters');
        } else {
            toggleBtn.classList.remove('has-filters');
        }
    }
    
    console.log('[DEBUG] Applying advanced filters:', filters);
    console.log('[DEBUG] Stored filters globally for table:', tableId);
    console.log('[DEBUG] Has active filters:', hasActiveFilters);
    
    // Trigger DataTable refresh - the AJAX data function will pick up the stored filters
    console.log('[DEBUG] Calling dataTable.draw()');
    dataTable.draw();
    
    // Close filter panel
    window.closeFilterPanel(tableId);
    
    console.log('Applied advanced filters:', filters);
};

window.clearAdvancedFilters = function(tableId) {
    const panel = document.getElementById(`filter-panel-${tableId}`);
    const table = document.getElementById(tableId);
    const wrapper = table ? table.closest('.datatable-wrapper') : null;
    const toggleBtn = wrapper ? wrapper._filterToggle : null;
    
    // Clear all filter inputs
    const filterInputs = panel.querySelectorAll('input, select');
    filterInputs.forEach(input => {
        if (input.type === 'select-one') {
            input.selectedIndex = 0;
        } else {
            input.value = '';
        }
    });
    
    // Update toggle button state
    if (toggleBtn) {
        toggleBtn.classList.remove('has-filters');
    }
    
    // Clear stored filters
    if (window.cacaoTableFilters) {
        window.cacaoTableFilters[tableId] = {};
    }
    
    // Refresh DataTable - the AJAX data function will pick up the cleared filters
    if (table && wrapper && wrapper._dataTable) {
        const dataTable = window.jQuery(`#${tableId}`).DataTable();
        console.log('[DEBUG] Clearing filters and refreshing DataTable');
        dataTable.draw();
    }
    
    console.log('Cleared all advanced filters');
};

// === Helper Functions for Filter Panel ===

function closeFilterPanel(panel, overlay) {
    panel.classList.add("animating-out");
    panel.classList.remove("open");
    overlay.classList.remove("visible");
    
    setTimeout(() => {
        panel.classList.remove("animating-out");
    }, 300);
}

function openFilterPanel(panel, overlay) {
    panel.classList.add("animating-in");
    panel.classList.add("open");
    overlay.classList.add("visible");
    
    setTimeout(() => {
        panel.classList.remove("animating-in");
    }, 300);
}

function createFilterPanel(tableId, props) {
    // Create overlay
    const overlay = document.createElement("div");
    overlay.id = `filter-overlay-${tableId}`;
    overlay.className = "table-filter-panel-overlay";
    overlay.onclick = () => {
        const panel = document.getElementById(`filter-panel-${tableId}`);
        closeFilterPanel(panel, overlay);
    };
    document.body.appendChild(overlay);
    
    // Create filter panel
    const panel = document.createElement("div");
    panel.id = `filter-panel-${tableId}`;
    panel.className = "table-filter-panel";
    
    // Create header
    const header = document.createElement("div");
    header.className = "filter-panel-header";
    header.innerHTML = `
        <h3 class="filter-panel-title">Advanced Filters</h3>
        <button class="filter-panel-close" onclick="window.closeFilterPanel('${tableId}')">&times;</button>
    `;
    
    // Create body
    const body = document.createElement("div");
    body.className = "filter-panel-body";
    
    // Generate filter fields based on columns
    if (props.columns && props.columns.length > 0) {
        props.columns.forEach((column, index) => {
            const fieldGroup = createFilterField(column, index, tableId);
            body.appendChild(fieldGroup);
        });
    }
    
    // Create actions
    const actions = document.createElement("div");
    actions.className = "filter-panel-actions";
    actions.innerHTML = `
        <button class="filter-btn filter-btn-primary" onclick="window.applyAdvancedFilters('${tableId}')">Apply Filters</button>
        <button class="filter-btn filter-btn-clear" onclick="window.clearAdvancedFilters('${tableId}')">Clear All</button>
    `;
    
    panel.appendChild(header);
    panel.appendChild(body);
    panel.appendChild(actions);
    
    return panel;
}

function createFilterField(column, index, tableId) {
    const fieldGroup = document.createElement("div");
    fieldGroup.className = "filter-group";
    
    const label = document.createElement("label");
    label.className = "filter-group-label";
    label.textContent = column.title || column.label || `Column ${index + 1}`;
    
    const fieldContainer = document.createElement("div");
    fieldContainer.className = "filter-field";
    
    // Determine field type based on column data type
    const dataIndex = column.dataIndex || column.key || `col_${index}`;
    const fieldType = getColumnFilterType(column);
    
    if (fieldType === 'range') {
        // Numeric range filter
        const rangeContainer = document.createElement("div");
        rangeContainer.className = "filter-range";
        
        const minInput = document.createElement("input");
        minInput.type = "number";
        minInput.placeholder = "Min value";
        minInput.id = `filter-${tableId}-${dataIndex}-min`;
        
        const separator = document.createElement("span");
        separator.className = "filter-range-separator";
        separator.textContent = "to";
        
        const maxInput = document.createElement("input");
        maxInput.type = "number";
        maxInput.placeholder = "Max value";
        maxInput.id = `filter-${tableId}-${dataIndex}-max`;
        
        rangeContainer.appendChild(minInput);
        rangeContainer.appendChild(separator);
        rangeContainer.appendChild(maxInput);
        fieldContainer.appendChild(rangeContainer);
    } else {
        // Text filter with type selection
        const typeSelect = document.createElement("select");
        typeSelect.id = `filter-${tableId}-${dataIndex}-type`;
        typeSelect.innerHTML = `
            <option value="contains">Contains</option>
            <option value="equals">Equals</option>
            <option value="starts_with">Starts with</option>
            <option value="ends_with">Ends with</option>
            ${fieldType === 'numeric' ? `
                <option value="greater_than">Greater than</option>
                <option value="less_than">Less than</option>
            ` : ''}
        `;
        
        const valueInput = document.createElement("input");
        valueInput.type = fieldType === 'numeric' ? 'number' : 'text';
        valueInput.placeholder = `Filter ${column.title || 'column'}...`;
        valueInput.id = `filter-${tableId}-${dataIndex}-value`;
        valueInput.style.marginTop = "8px";
        
        fieldContainer.appendChild(typeSelect);
        fieldContainer.appendChild(valueInput);
    }
    
    fieldGroup.appendChild(label);
    fieldGroup.appendChild(fieldContainer);
    
    return fieldGroup;
}

function getColumnFilterType(column) {
    // Determine appropriate filter type based on column properties
    if (column.type === 'number' || column.dataType === 'numeric') {
        return 'range';
    }
    if (column.type === 'date' || column.dataType === 'date') {
        return 'date';
    }
    return 'text';
}

window.toggleAdvancedFilters = function(tableId, props) {
    let panel = document.getElementById(`filter-panel-${tableId}`);
    
    if (!panel) {
        panel = createFilterPanel(tableId, props);
        document.body.appendChild(panel);
    }
    
    const overlay = document.getElementById(`filter-overlay-${tableId}`);
    const isOpen = panel.classList.contains("open");
    
    if (isOpen) {
        closeFilterPanel(panel, overlay);
    } else {
        openFilterPanel(panel, overlay);
    }
};

(component) => {
    // === Component Renderer ===
    console.log("[CacaoCore] Rendering merged table component:", component);
    
    const props = component.props;
    const isAdvanced = props.advanced === true;
    const tableId = `table-${Math.random().toString(36).substr(2, 9)}`;
    
    // === DataTables.js Asset Loading Functions ===
    
    function loadDataTablesAssets(props) {
        return new Promise(async (resolve) => {
            // Check if DataTables is already loaded
            if (window.jQuery && window.jQuery.fn.DataTable) {
                resolve();
                return;
            }
            
            try {
                // Step 1: Load jQuery first and ensure it's available
                if (!window.jQuery) {
                    await loadScript('https://code.jquery.com/jquery-3.7.0.min.js');
                    // Wait for jQuery to be globally available
                    await waitForjQuery();
                }
                
                // Step 2: Load DataTables CSS (can be parallel with core JS)
                const cssPromises = [];
                if (!document.querySelector('link[href*="datatables"]')) {
                    cssPromises.push(loadCSS(getDataTablesCSS(props.theme)));
                }
                
                // Step 3: Load DataTables core library after jQuery is confirmed available
                await loadScript('https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js');
                
                // Step 4: Load theme-specific assets (depends on core DataTables)
                if (props.theme === 'bootstrap5') {
                    await loadScript('https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js');
                } else if (props.theme === 'bootstrap4') {
                    await loadScript('https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap4.min.js');
                }
                
                // Step 5: Load additional plugins sequentially (each depends on core DataTables)
                if (props.datatables_config && props.datatables_config.responsive) {
                    await loadScript('https://cdn.datatables.net/responsive/2.5.0/js/dataTables.responsive.min.js');
                    cssPromises.push(loadCSS('https://cdn.datatables.net/responsive/2.5.0/css/responsive.dataTables.min.css'));
                }
                
                if (props.datatables_config && props.datatables_config.fixedHeader) {
                    await loadScript('https://cdn.datatables.net/fixedheader/3.4.0/js/dataTables.fixedHeader.min.js');
                    cssPromises.push(loadCSS('https://cdn.datatables.net/fixedheader/3.4.0/css/fixedHeader.dataTables.min.css'));
                }
                
                if (props.datatables_config && props.datatables_config.select) {
                    await loadScript('https://cdn.datatables.net/select/1.7.0/js/dataTables.select.min.js');
                    cssPromises.push(loadCSS('https://cdn.datatables.net/select/1.7.0/css/select.dataTables.min.css'));
                }
                
                if (props.datatables_config && props.datatables_config.buttons) {
                    // Load buttons plugin dependencies sequentially
                    await loadScript('https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js');
                    
                    // Load button feature dependencies (can be parallel as they don't depend on each other)
                    await Promise.all([
                        loadScript('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js'),
                        loadScript('https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js'),
                        loadScript('https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js')
                    ]);
                    
                    // Load button feature plugins (depend on core buttons + their dependencies)
                    await Promise.all([
                        loadScript('https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js'),
                        loadScript('https://cdn.datatables.net/buttons/2.4.2/js/buttons.print.min.js')
                    ]);
                    
                    cssPromises.push(loadCSS('https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css'));
                }
                
                // Wait for all CSS to load
                await Promise.all(cssPromises);
                
                // Final verification that jQuery and DataTables are available
                await waitForDataTables();
                
                resolve();
            } catch (error) {
                console.error('Error loading DataTables assets:', error);
                resolve(); // Continue execution even if some assets fail to load
            }
        });
    }
    
    // Helper function to wait for jQuery to be globally available
    function waitForjQuery() {
        return new Promise((resolve) => {
            const checkjQuery = () => {
                if (window.jQuery && typeof window.jQuery === 'function') {
                    resolve();
                } else {
                    setTimeout(checkjQuery, 50);
                }
            };
            checkjQuery();
        });
    }
    
    // Helper function to wait for DataTables to be available
    function waitForDataTables() {
        return new Promise((resolve) => {
            const checkDataTables = () => {
                if (window.jQuery && window.jQuery.fn && window.jQuery.fn.DataTable) {
                    resolve();
                } else {
                    setTimeout(checkDataTables, 50);
                }
            };
            checkDataTables();
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
            
            // Enhance AJAX configuration to support advanced filters
            if (config.ajax && props.pandas_server && props.pandas_server.enabled) {
                const originalAjax = config.ajax;
                const originalDataFunction = typeof originalAjax === 'object' ? originalAjax.data : null;
                const ajaxUrl = typeof originalAjax === 'string' ? originalAjax : originalAjax.url;
                
                config.ajax = {
                    url: ajaxUrl,
                    data: function(d) {
                        console.log('[DEBUG] DataTable AJAX data function called for table:', tableId);
                        console.log('[DEBUG] Original DataTables data:', d);
                        
                        // Call original data function if it exists
                        if (originalDataFunction && typeof originalDataFunction === 'function') {
                            d = originalDataFunction(d) || d;
                            console.log('[DEBUG] After original data function:', d);
                        }
                        
                        // Add advanced filters from global storage
                        const storedFilters = window.cacaoTableFilters && window.cacaoTableFilters[tableId] ?
                            window.cacaoTableFilters[tableId] : {};
                        
                        const filtersJson = JSON.stringify(storedFilters);
                        d.advanced_filters = filtersJson;
                        
                        console.log('[DEBUG] Adding advanced_filters:', filtersJson);
                        console.log('[DEBUG] Final data being sent:', d);
                        
                        return d;
                    }
                };
                
                // Copy other AJAX properties if they exist
                if (typeof originalAjax === 'object') {
                    Object.keys(originalAjax).forEach(key => {
                        if (key !== 'data' && key !== 'url') {
                            config.ajax[key] = originalAjax[key];
                        }
                    });
                }
                
                console.log('[DEBUG] Enhanced AJAX configuration with advanced filters support');
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
    
    function addFilterToggleButton(wrapper, tableId, props) {
        // Create filter toggle button
        const filterToggle = document.createElement("div");
        filterToggle.className = "table-filter-toggle";
        
        const toggleBtn = document.createElement("button");
        toggleBtn.className = "filter-toggle-btn";
        toggleBtn.innerHTML = `
            <span class="filter-toggle-icon">🔍</span>
            <span>Advanced Filters</span>
            <span class="filter-active-indicator"></span>
        `;
        
        toggleBtn.onclick = () => window.toggleAdvancedFilters(tableId, props);
        
        filterToggle.appendChild(toggleBtn);
        
        // Insert before the table
        wrapper.insertBefore(filterToggle, wrapper.firstChild);
        
        // Store reference for later use
        wrapper._filterToggle = toggleBtn;
    }
    
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
        // Add filter toggle button if pandas server is enabled
        if (props.pandas_server && props.pandas_server.enabled) {
            addFilterToggleButton(wrapper, tableId, props);
        }
        
        loadDataTablesAssets(props).then(() => {
            initializeDataTable(tableId, props, wrapper);
        });
    }
    
    return wrapper;
};