"""
Table Data Server for Cacao Framework
Implements DataTables server-side processing protocol for pandas DataFrames
"""

import json
import uuid
import pandas as pd
import threading
from typing import Dict, Any, List, Optional, Union
from urllib.parse import parse_qs, urlparse
from cacao.core.server import CacaoServer
from cacao.core.mixins.logging import LoggingMixin


class TableDataServer(LoggingMixin):
    """
    Server-side data processing for DataTables with pandas DataFrame support.
    
    Handles DataTables AJAX protocol:
    - draw: Request counter for security
    - start: Pagination start index
    - length: Number of records per page
    - search[value]: Global search term
    - order[0][column]: Column index to sort by
    - order[0][dir]: Sort direction (asc/desc)
    
    Response format:
    - draw: Echo back the draw counter
    - recordsTotal: Total records before filtering
    - recordsFiltered: Total records after filtering
    - data: Array of row data for current page
    """
    
    # Class variable to store registered servers
    _servers: Dict[str, 'TableDataServer'] = {}
    _lock = threading.Lock()
    
    def __init__(self, dataframe: pd.DataFrame, table_id: str, columns: List[Dict[str, Any]] = None) -> None:
        """
        Initialize TableDataServer with pandas DataFrame.
        
        Args:
            dataframe: pandas DataFrame containing the data
            table_id: Unique identifier for this table
            columns: Column definitions from Table component
        """
        self.dataframe = dataframe.copy()  # Make a copy to avoid modifying original
        self.table_id = table_id
        self.columns = columns or []
        self.endpoint = f"/api/table-data/{table_id}"
        
        # Store original DataFrame for total record count
        self.original_dataframe = dataframe.copy()
        
        # Thread safety
        self._data_lock = threading.Lock()
        
        # Register this server instance
        with TableDataServer._lock:
            TableDataServer._servers[table_id] = self
            
        self.log(f"TableDataServer initialized for table {table_id}", "info", "📊")
    
    @classmethod
    def get_server(cls, table_id: str) -> Optional['TableDataServer']:
        """Get registered server instance by table ID."""
        with cls._lock:
            return cls._servers.get(table_id)
    
    @classmethod
    def remove_server(cls, table_id: str) -> None:
        """Remove registered server instance."""
        with cls._lock:
            cls._servers.pop(table_id, None)
    
    def register_endpoint(self, server: CacaoServer) -> None:
        """Register this table's endpoint with the CacaoServer."""
        from cacao.core.decorators import register_route, ROUTES
        
        self.log(f"DEBUG: Starting route registration for {self.endpoint}", "info", "🔍")
        self.log(f"DEBUG: Current ROUTES before registration: {list(ROUTES.keys())}", "info", "📋")
        
        # Create a closure to capture this instance
        instance = self
        
        def handle_table_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
            instance.log(f"DEBUG: Table request handler called with data: {request_data}", "info", "📨")
            return instance.handle_request(request_data)
        
        # Register the route manually
        register_route(self.endpoint, handle_table_request)
        
        self.log(f"DEBUG: ROUTES after registration: {list(ROUTES.keys())}", "info", "📋")
        self.log(f"DEBUG: Route handler for {self.endpoint}: {ROUTES.get(self.endpoint)}", "info", "🎯")
        self.log(f"Registered endpoint: {self.endpoint}", "info", "🔗")
    
    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle DataTables AJAX request.
        
        Args:
            request_data: Request parameters from DataTables
            
        Returns:
            DataTables-compatible JSON response
        """
        try:
            self.log(f"[DEBUG] Server received request data keys: {list(request_data.keys())}", "info", "🔍")
            self.log(f"[DEBUG] Full request data: {request_data}", "info", "📨")
            
            # Parse DataTables parameters
            draw = int(request_data.get('draw', [1])[0]) if isinstance(request_data.get('draw'), list) else int(request_data.get('draw', 1))
            start = int(request_data.get('start', [0])[0]) if isinstance(request_data.get('start'), list) else int(request_data.get('start', 0))
            length = int(request_data.get('length', [10])[0]) if isinstance(request_data.get('length'), list) else int(request_data.get('length', 10))
            search_value = request_data.get('search[value]', [''])[0] if isinstance(request_data.get('search[value]'), list) else request_data.get('search[value]', '')
            
            # Parse column-specific filter parameters
            column_filters = {}
            i = 0
            while f'columns[{i}][search][value]' in request_data:
                column_search = request_data.get(f'columns[{i}][search][value]', [''])[0] if isinstance(request_data.get(f'columns[{i}][search][value]'), list) else request_data.get(f'columns[{i}][search][value]', '')
                if column_search.strip():
                    column_filters[i] = column_search.strip()
                i += 1
            
            # Parse custom advanced filters (for filter panel)
            advanced_filters = request_data.get('advanced_filters', {})
            self.log(f"[DEBUG] Raw advanced_filters from request: {advanced_filters} (type: {type(advanced_filters)})", "info", "🎯")
            
            if isinstance(advanced_filters, list) and len(advanced_filters) > 0:
                advanced_filters = advanced_filters[0]
                self.log(f"[DEBUG] Extracted from list: {advanced_filters}", "info", "📋")
            if isinstance(advanced_filters, str):
                try:
                    import json
                    advanced_filters = json.loads(advanced_filters)
                    self.log(f"[DEBUG] Parsed JSON advanced_filters: {advanced_filters}", "info", "✅")
                except Exception as e:
                    self.log(f"[DEBUG] Failed to parse JSON advanced_filters: {e}", "warning", "⚠️")
                    advanced_filters = {}
            
            self.log(f"[DEBUG] Final advanced_filters: {advanced_filters}", "info", "🎯")
            
            # Parse ordering parameters
            order_params = []
            i = 0
            while f'order[{i}][column]' in request_data:
                column_idx = request_data.get(f'order[{i}][column]', ['0'])[0] if isinstance(request_data.get(f'order[{i}][column]'), list) else request_data.get(f'order[{i}][column]', '0')
                direction = request_data.get(f'order[{i}][dir]', ['asc'])[0] if isinstance(request_data.get(f'order[{i}][dir]'), list) else request_data.get(f'order[{i}][dir]', 'asc')
                order_params.append({
                    'column': int(column_idx),
                    'dir': direction
                })
                i += 1
            
            # Thread-safe data processing
            with self._data_lock:
                # Start with original data
                filtered_df = self.dataframe.copy()
                
                # Apply global search if provided
                if search_value.strip():
                    filtered_df = self._apply_search(filtered_df, search_value.strip())
                
                # Apply column-specific filters
                if column_filters:
                    filtered_df = self._apply_column_filters(filtered_df, column_filters)
                
                # Apply advanced filters from filter panel
                if advanced_filters:
                    filtered_df = self._apply_advanced_filters(filtered_df, advanced_filters)
                
                # Apply sorting
                if order_params:
                    filtered_df = self._apply_sorting(filtered_df, order_params)
                
                # Get total counts
                records_total = len(self.original_dataframe)
                records_filtered = len(filtered_df)
                
                # Apply pagination
                paginated_df = self._apply_pagination(filtered_df, start, length)
                
                # Convert to list of dictionaries for JSON response
                data = paginated_df.to_dict('records')
                
                # Format data according to column definitions
                formatted_data = self._format_data(data)
                
            # Build DataTables response
            response = {
                'draw': draw,
                'recordsTotal': records_total,
                'recordsFiltered': records_filtered,
                'data': formatted_data
            }
            
            self.log(f"Table {self.table_id} served {len(formatted_data)} records (filtered: {records_filtered}/{records_total})", "info", "📊")
            return response
            
        except Exception as e:
            self.log(f"Error handling table request: {str(e)}", "error", "❌")
            return {
                'draw': draw if 'draw' in locals() else 1,
                'recordsTotal': 0,
                'recordsFiltered': 0,
                'data': [],
                'error': str(e)
            }
    
    def _apply_search(self, df: pd.DataFrame, search_value: str) -> pd.DataFrame:
        """
        Apply global search across all string columns.
        
        Args:
            df: DataFrame to search
            search_value: Search term
            
        Returns:
            Filtered DataFrame
        """
        if not search_value or df.empty:
            return df
        
        try:
            # Create a boolean mask for matching rows
            search_mask = pd.Series([False] * len(df), index=df.index)
            
            # Search in all object/string columns
            for column in df.columns:
                if df[column].dtype == 'object' or pd.api.types.is_string_dtype(df[column]):
                    # Convert to string and search (case-insensitive)
                    column_mask = df[column].astype(str).str.contains(
                        search_value, 
                        case=False, 
                        na=False, 
                        regex=False
                    )
                    search_mask = search_mask | column_mask
                elif pd.api.types.is_numeric_dtype(df[column]):
                    # For numeric columns, convert search value to numeric and match
                    try:
                        numeric_search = pd.to_numeric(search_value, errors='ignore')
                        if pd.api.types.is_numeric_dtype(type(numeric_search)):
                            column_mask = df[column] == numeric_search
                            search_mask = search_mask | column_mask
                    except (ValueError, TypeError):
                        pass  # Skip numeric search if conversion fails
            
            return df[search_mask]
            
        except Exception as e:
            self.log(f"Error in search filtering: {str(e)}", "warning", "⚠️")
            return df  # Return original df if search fails
    
    def _apply_column_filters(self, df: pd.DataFrame, column_filters: Dict[int, str]) -> pd.DataFrame:
        """
        Apply column-specific filters.
        
        Args:
            df: DataFrame to filter
            column_filters: Dictionary mapping column index to filter value
            
        Returns:
            Filtered DataFrame
        """
        if not column_filters or df.empty:
            return df
        
        try:
            # Create a boolean mask for matching rows
            filter_mask = pd.Series([True] * len(df), index=df.index)
            
            for column_idx, filter_value in column_filters.items():
                if 0 <= column_idx < len(df.columns):
                    column_name = df.columns[column_idx]
                    column = df[column_name]
                    
                    if pd.api.types.is_string_dtype(column) or column.dtype == 'object':
                        # String filtering (case-insensitive contains)
                        column_mask = column.astype(str).str.contains(
                            filter_value,
                            case=False,
                            na=False,
                            regex=False
                        )
                    elif pd.api.types.is_numeric_dtype(column):
                        # Numeric filtering (exact match or range)
                        try:
                            if '-' in filter_value and len(filter_value.split('-')) == 2:
                                # Range filtering (e.g., "10-20")
                                min_val, max_val = filter_value.split('-')
                                min_val = pd.to_numeric(min_val.strip(), errors='coerce')
                                max_val = pd.to_numeric(max_val.strip(), errors='coerce')
                                if not pd.isna(min_val) and not pd.isna(max_val):
                                    column_mask = (column >= min_val) & (column <= max_val)
                                else:
                                    column_mask = pd.Series([False] * len(df), index=df.index)
                            else:
                                # Exact numeric match
                                numeric_filter = pd.to_numeric(filter_value, errors='coerce')
                                if not pd.isna(numeric_filter):
                                    column_mask = column == numeric_filter
                                else:
                                    column_mask = pd.Series([False] * len(df), index=df.index)
                        except:
                            column_mask = pd.Series([False] * len(df), index=df.index)
                    else:
                        # Default string-based filtering for other types
                        column_mask = column.astype(str).str.contains(
                            filter_value,
                            case=False,
                            na=False,
                            regex=False
                        )
                    
                    filter_mask = filter_mask & column_mask
            
            return df[filter_mask]
            
        except Exception as e:
            self.log(f"Error in column filtering: {str(e)}", "warning", "⚠️")
            return df
    
    def _apply_advanced_filters(self, df: pd.DataFrame, advanced_filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply advanced filters from the filter panel.
        
        Args:
            df: DataFrame to filter
            advanced_filters: Dictionary of advanced filter conditions
            
        Returns:
            Filtered DataFrame
        """
        if not advanced_filters or df.empty:
            return df
        
        try:
            # Create a boolean mask for matching rows
            filter_mask = pd.Series([True] * len(df), index=df.index)
            
            for column_name, filter_config in advanced_filters.items():
                if column_name not in df.columns:
                    continue
                
                column = df[column_name]
                filter_type = filter_config.get('type', 'contains')
                filter_value = filter_config.get('value', '')
                
                if not filter_value:
                    continue
                
                if filter_type == 'contains':
                    # String contains (case-insensitive)
                    column_mask = column.astype(str).str.contains(
                        filter_value,
                        case=False,
                        na=False,
                        regex=False
                    )
                elif filter_type == 'equals':
                    # Exact match
                    if pd.api.types.is_numeric_dtype(column):
                        try:
                            numeric_value = pd.to_numeric(filter_value, errors='coerce')
                            if not pd.isna(numeric_value):
                                column_mask = column == numeric_value
                            else:
                                column_mask = pd.Series([False] * len(df), index=df.index)
                        except:
                            column_mask = pd.Series([False] * len(df), index=df.index)
                    else:
                        column_mask = column.astype(str).str.lower() == str(filter_value).lower()
                elif filter_type == 'starts_with':
                    # Starts with
                    column_mask = column.astype(str).str.lower().str.startswith(str(filter_value).lower())
                elif filter_type == 'ends_with':
                    # Ends with
                    column_mask = column.astype(str).str.lower().str.endswith(str(filter_value).lower())
                elif filter_type == 'greater_than':
                    # Greater than (numeric)
                    if pd.api.types.is_numeric_dtype(column):
                        try:
                            numeric_value = pd.to_numeric(filter_value, errors='coerce')
                            if not pd.isna(numeric_value):
                                column_mask = column > numeric_value
                            else:
                                column_mask = pd.Series([False] * len(df), index=df.index)
                        except:
                            column_mask = pd.Series([False] * len(df), index=df.index)
                    else:
                        column_mask = pd.Series([False] * len(df), index=df.index)
                elif filter_type == 'less_than':
                    # Less than (numeric)
                    if pd.api.types.is_numeric_dtype(column):
                        try:
                            numeric_value = pd.to_numeric(filter_value, errors='coerce')
                            if not pd.isna(numeric_value):
                                column_mask = column < numeric_value
                            else:
                                column_mask = pd.Series([False] * len(df), index=df.index)
                        except:
                            column_mask = pd.Series([False] * len(df), index=df.index)
                    else:
                        column_mask = pd.Series([False] * len(df), index=df.index)
                elif filter_type == 'range':
                    # Range filtering (for numeric columns)
                    if pd.api.types.is_numeric_dtype(column):
                        try:
                            min_val = filter_config.get('min')
                            max_val = filter_config.get('max')
                            if min_val is not None and max_val is not None:
                                min_val = pd.to_numeric(min_val, errors='coerce')
                                max_val = pd.to_numeric(max_val, errors='coerce')
                                if not pd.isna(min_val) and not pd.isna(max_val):
                                    column_mask = (column >= min_val) & (column <= max_val)
                                else:
                                    column_mask = pd.Series([False] * len(df), index=df.index)
                            else:
                                column_mask = pd.Series([True] * len(df), index=df.index)
                        except:
                            column_mask = pd.Series([False] * len(df), index=df.index)
                    else:
                        column_mask = pd.Series([False] * len(df), index=df.index)
                else:
                    # Default to contains
                    column_mask = column.astype(str).str.contains(
                        filter_value,
                        case=False,
                        na=False,
                        regex=False
                    )
                
                filter_mask = filter_mask & column_mask
            
            return df[filter_mask]
            
        except Exception as e:
            self.log(f"Error in advanced filtering: {str(e)}", "warning", "⚠️")
            return df
    
    def _apply_sorting(self, df: pd.DataFrame, order_params: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Apply sorting based on DataTables order parameters.
        
        Args:
            df: DataFrame to sort
            order_params: List of order parameters
            
        Returns:
            Sorted DataFrame
        """
        if not order_params or df.empty:
            return df
        
        try:
            # Build sorting parameters
            sort_columns = []
            sort_ascending = []
            
            for order in order_params:
                column_idx = order['column']
                direction = order['dir']
                
                # Get column name by index
                if 0 <= column_idx < len(df.columns):
                    column_name = df.columns[column_idx]
                    sort_columns.append(column_name)
                    sort_ascending.append(direction == 'asc')
            
            if sort_columns:
                return df.sort_values(
                    by=sort_columns,
                    ascending=sort_ascending,
                    na_position='last'  # Put NaN values at the end
                )
                
        except Exception as e:
            self.log(f"Error in sorting: {str(e)}", "warning", "⚠️")
            
        return df  # Return original df if sorting fails
    
    def _apply_pagination(self, df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
        """
        Apply pagination to DataFrame.
        
        Args:
            df: DataFrame to paginate
            start: Start index
            length: Number of records per page
            
        Returns:
            Paginated DataFrame
        """
        if df.empty or length <= 0:
            return df
        
        try:
            end = start + length
            return df.iloc[start:end]
        except Exception as e:
            self.log(f"Error in pagination: {str(e)}", "warning", "⚠️")
            return df
    
    def _format_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format data according to DataTables expectations.
        
        Args:
            data: List of row dictionaries
            
        Returns:
            List of dictionaries for DataTables consumption (object format)
        """
        if not data:
            return []
        
        try:
            # Format data as objects (dictionaries) for DataTables
            formatted_rows = []
            for row in data:
                formatted_row = {}
                for key, value in row.items():
                    # Handle NaN and None values
                    if pd.isna(value) or value is None:
                        value = ''
                    formatted_row[key] = value
                formatted_rows.append(formatted_row)
            return formatted_rows
                
        except Exception as e:
            self.log(f"Error formatting data: {str(e)}", "warning", "⚠️")
        
        return []
    
    def update_data(self, new_dataframe: pd.DataFrame) -> None:
        """
        Update the underlying DataFrame.
        
        Args:
            new_dataframe: New pandas DataFrame
        """
        with self._data_lock:
            self.dataframe = new_dataframe.copy()
            self.original_dataframe = new_dataframe.copy()
        
        self.log(f"Updated data for table {self.table_id}", "info", "🔄")


def create_table_data_server(dataframe: pd.DataFrame, columns: List[Dict[str, Any]] = None) -> TableDataServer:
    """
    Create and register a new TableDataServer instance.
    
    Args:
        dataframe: pandas DataFrame containing the data
        columns: Column definitions from Table component
        
    Returns:
        TableDataServer instance
    """
    table_id = f"table_{uuid.uuid4().hex[:8]}"
    return TableDataServer(dataframe, table_id, columns)


def cleanup_table_server(table_id: str) -> None:
    """
    Clean up a table server instance.
    
    Args:
        table_id: Table ID to clean up
    """
    TableDataServer.remove_server(table_id)