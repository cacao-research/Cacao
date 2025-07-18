"""
Merged Table Component for Cacao Framework
Combines simple table and advanced DataTables.js functionality
"""

from typing import Dict, Any, List, Optional, Union
import warnings
from ...base import Component

class Table(Component):
    """
    Unified Table component with progressive enhancement.
    
    By default, renders as a lightweight native table.
    With advanced=True, uses DataTables.js for advanced features.
    
    API Support:
    - Modern: columns, dataSource, data
    - Legacy: headers, rows (with deprecation warnings)
    """
    
    def __init__(
        self,
        # Modern API (preferred)
        columns: Optional[List[Dict[str, Any]]] = None,
        dataSource: Optional[List[Dict[str, Any]]] = None,
        data: Optional[List[Dict[str, Any]]] = None,
        
        # Legacy API (deprecated)
        headers: Optional[List[str]] = None,
        rows: Optional[List[List[Any]]] = None,
        
        # Feature flag for progressive enhancement
        advanced: bool = False,
        
        # Basic table features (both modes)
        pagination: Union[bool, Dict[str, Any]] = None,
        sorting: bool = None,
        filters: Optional[Dict[str, Any]] = None,
        
        # Advanced features (advanced mode only)
        page_length: int = 10,
        length_menu: List[int] = None,
        searching: bool = True,
        ordering: bool = True,
        info: bool = True,
        responsive: bool = True,
        scroll_x: bool = False,
        scroll_y: Optional[str] = None,
        fixed_header: bool = False,
        
        # Server-side processing
        server_side: bool = False,
        ajax_url: Optional[str] = None,
        
        # Styling
        theme: str = "default",
        striped: bool = True,
        hover: bool = True,
        compact: bool = False,
        
        # Selection
        select: bool = False,
        select_style: str = "single",
        
        # Export buttons
        buttons: List[str] = None,
        
        # Custom options
        custom_options: Dict[str, Any] = None,
        
        **kwargs
    ) -> None:
        super().__init__()
        
        # Handle legacy API with deprecation warnings
        if headers is not None or rows is not None:
            warnings.warn(
                "The 'headers' and 'rows' parameters are deprecated. "
                "Use 'columns' and 'dataSource' instead.",
                DeprecationWarning,
                stacklevel=2
            )
            
            # Convert legacy format to modern format
            if headers and not columns:
                columns = [{"title": header, "dataIndex": f"col_{i}"} for i, header in enumerate(headers)]
            
            if rows and not dataSource and not data:
                dataSource = []
                for row in rows:
                    row_dict = {}
                    for i, value in enumerate(row):
                        row_dict[f"col_{i}"] = value
                    dataSource.append(row_dict)
        
        # Handle data vs dataSource (both are valid)
        if data is not None and dataSource is None:
            dataSource = data
        
        # Store core props
        self.columns = columns or []
        self.dataSource = dataSource or []
        self.advanced = advanced
        
        # Basic features
        self.pagination = pagination if pagination is not None else ({"page_size": 10, "current": 1} if not advanced else True)
        self.sorting = sorting if sorting is not None else (False if not advanced else True)
        self.filters = filters
        
        # Advanced features (only relevant when advanced=True)
        if advanced:
            self.page_length = page_length
            self.length_menu = length_menu or [10, 25, 50, 100]
            self.searching = searching
            self.ordering = ordering
            self.info = info
            self.responsive = responsive
            self.scroll_x = scroll_x
            self.scroll_y = scroll_y
            self.fixed_header = fixed_header
            self.server_side = server_side
            self.ajax_url = ajax_url
            self.theme = theme
            self.striped = striped
            self.hover = hover
            self.compact = compact
            self.select = select
            self.select_style = select_style
            self.buttons = buttons or []
            self.custom_options = custom_options or {}
        
        # Store additional props
        self.extra_props = kwargs
    
    def _build_datatables_config(self) -> Dict[str, Any]:
        """Build DataTables configuration object (advanced mode only)"""
        if not self.advanced:
            return {}
        
        config = {
            # Core features
            "paging": self.pagination if isinstance(self.pagination, bool) else True,
            "pageLength": self.page_length,
            "lengthMenu": self.length_menu,
            "searching": self.searching,
            "ordering": self.ordering,
            "info": self.info,
            
            # Data
            "data": self.dataSource if not self.server_side else None,
            "columns": self._process_columns_for_datatables(),
            
            # Server-side processing
            "serverSide": self.server_side,
            "ajax": self.ajax_url if self.server_side else None,
            
            # Advanced features
            "responsive": self.responsive,
            "scrollX": self.scroll_x,
            "scrollY": self.scroll_y,
            "fixedHeader": self.fixed_header,
            
            # Selection
            "select": {
                "style": self.select_style
            } if self.select else False,
            
            # Language customization
            "language": {
                "search": "Search:",
                "lengthMenu": "Show _MENU_ entries per page",
                "info": "Showing _START_ to _END_ of _TOTAL_ entries",
                "infoEmpty": "No entries to show",
                "infoFiltered": "(filtered from _MAX_ total entries)",
                "zeroRecords": "No matching records found",
                "emptyTable": "No data available in table",
                "paginate": {
                    "first": "First",
                    "last": "Last",
                    "next": "Next",
                    "previous": "Previous"
                }
            },
            
            # Buttons configuration
            "buttons": self.buttons if self.buttons else None,
            "dom": self._build_dom_string()
        }
        
        # Merge custom options
        config.update(self.custom_options)
        
        # Remove None values
        return {k: v for k, v in config.items() if v is not None}
    
    def _process_columns_for_datatables(self) -> List[Dict[str, Any]]:
        """Process column definitions for DataTables (advanced mode only)"""
        processed_columns = []
        
        for col in self.columns:
            dt_col = {
                "data": col.get("dataIndex", col.get("key")),
                "title": col.get("title", col.get("label", "")),
                "orderable": col.get("sortable", True),
                "searchable": col.get("searchable", True),
                "visible": col.get("visible", True),
                "width": col.get("width"),
                "className": col.get("className", ""),
            }
            
            # Handle custom render functions
            if col.get("render"):
                dt_col["render"] = col["render"]
            
            # Handle column type
            if col.get("type"):
                dt_col["type"] = col["type"]
            
            processed_columns.append({k: v for k, v in dt_col.items() if v is not None})
        
        return processed_columns
    
    def _build_dom_string(self) -> str:
        """Build DataTables DOM string based on features (advanced mode only)"""
        if not self.advanced:
            return ""
        
        dom_parts = []
        
        # Buttons
        if self.buttons:
            dom_parts.append("B")
        
        # Length menu and search
        dom_parts.extend(["l", "f"])
        
        # Table
        dom_parts.append("t")
        
        # Info and pagination
        if self.info:
            dom_parts.append("i")
        if self.pagination:
            dom_parts.append("p")
        
        return "".join(dom_parts)
    
    def _get_css_classes(self) -> str:
        """Get CSS classes for table styling"""
        if not self.advanced:
            return "table"
        
        classes = ["display", "table"]
        
        if self.striped:
            classes.append("table-striped")
        if self.hover:
            classes.append("table-hover")
        if self.compact:
            classes.append("table-sm")
        
        # Theme-specific classes
        if self.theme == "bootstrap4" or self.theme == "bootstrap5":
            classes.extend(["table-bordered"])
        
        return " ".join(classes)
    
    def render(self) -> Dict[str, Any]:
        """Render the Table component"""
        if self.advanced:
            # Advanced mode: use DataTables.js
            return {
                "type": "table",
                "props": {
                    # Table structure
                    "columns": self.columns,
                    "dataSource": self.dataSource,
                    "data": self.dataSource,  # alias for compatibility
                    
                    # Mode flag
                    "advanced": True,
                    
                    # DataTables configuration
                    "datatables_config": self._build_datatables_config(),
                    
                    # Styling
                    "theme": self.theme,
                    "css_classes": self._get_css_classes(),
                    
                    # Component metadata
                    "server_side": self.server_side,
                    "ajax_url": self.ajax_url,
                    
                    **self.extra_props
                }
            }
        else:
            # Simple mode: use native rendering
            return {
                "type": "table",
                "props": {
                    "columns": self.columns,
                    "dataSource": self.dataSource,
                    "pagination": self.pagination,
                    "sorting": self.sorting,
                    "filters": self.filters,
                    
                    # Mode flag
                    "advanced": False,
                    
                    **self.extra_props
                }
            }

# Keep backward compatibility with original factory functions
def create_simple_table(columns: List[Dict[str, Any]], dataSource: List[Dict[str, Any]], **kwargs) -> Table:
    """Create a simple table with native rendering"""
    return Table(columns=columns, dataSource=dataSource, advanced=False, **kwargs)

def create_advanced_table(columns: List[Dict[str, Any]], dataSource: List[Dict[str, Any]], **kwargs) -> Table:
    """Create an advanced table with DataTables.js"""
    return Table(columns=columns, dataSource=dataSource, advanced=True, **kwargs)

# Legacy aliases for backward compatibility
DataTable = Table  # Alias for the unified component

def create_simple_datatable(columns: List[Dict[str, Any]], data: List[Dict[str, Any]], **kwargs) -> Table:
    """Create a simple DataTable with basic features (legacy compatibility)"""
    return Table(columns=columns, dataSource=data, advanced=True, **kwargs)

def create_server_side_datatable(columns: List[Dict[str, Any]], ajax_url: str, **kwargs) -> Table:
    """Create a server-side processing DataTable (legacy compatibility)"""
    return Table(
        columns=columns,
        server_side=True,
        ajax_url=ajax_url,
        advanced=True,
        **kwargs
    )

def create_export_datatable(columns: List[Dict[str, Any]], data: List[Dict[str, Any]], **kwargs) -> Table:
    """Create a DataTable with export buttons (legacy compatibility)"""
    return Table(
        columns=columns,
        dataSource=data,
        buttons=["copy", "csv", "excel", "pdf", "print"],
        advanced=True,
        **kwargs
    )
