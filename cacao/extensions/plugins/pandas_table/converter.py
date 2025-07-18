"""
Converter module for transforming pandas DataFrames into Cacao table components.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
import sys
from datetime import datetime, timezone
import json
from enum import Enum

class ProcessingStrategy(Enum):
    """Enumeration of processing strategies for DataFrames."""
    IN_MEMORY = "in_memory"
    SERVER_SIDE = "server_side"

class DataFrameSizeAnalyzer:
    """Utility class for analyzing DataFrame size and determining optimal processing strategy."""
    
    # Default thresholds
    DEFAULT_ROW_THRESHOLD = 10000
    DEFAULT_MEMORY_THRESHOLD_MB = 5
    
    def __init__(self, row_threshold: int = DEFAULT_ROW_THRESHOLD,
                 memory_threshold_mb: float = DEFAULT_MEMORY_THRESHOLD_MB):
        """
        Initialize the size analyzer.
        
        Args:
            row_threshold: Maximum number of rows for in-memory processing
            memory_threshold_mb: Maximum memory usage in MB for in-memory processing
        """
        self.row_threshold = row_threshold
        self.memory_threshold_mb = memory_threshold_mb
    
    def calculate_memory_footprint(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate DataFrame memory footprint.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary containing memory statistics
        """
        # Get memory usage in bytes
        memory_usage = df.memory_usage(deep=True)
        total_memory_bytes = int(memory_usage.sum())  # Convert to native int
        total_memory_mb = float(total_memory_bytes / (1024 * 1024))  # Convert to native float
        
        # Calculate per-column memory usage
        column_memory = {}
        for col in df.columns:
            col_memory_bytes = int(df[col].memory_usage(deep=True))  # Convert to native int
            col_memory_mb = float(col_memory_bytes / (1024 * 1024))  # Convert to native float
            column_memory[col] = {
                'bytes': col_memory_bytes,
                'mb': col_memory_mb,
                'dtype': str(df[col].dtype)
            }
        
        # Index memory usage
        index_memory_bytes = int(memory_usage.iloc[0]) if len(memory_usage) > 0 else 0
        index_memory_mb = float(index_memory_bytes / (1024 * 1024))
        
        return {
            'total_memory_bytes': total_memory_bytes,
            'total_memory_mb': total_memory_mb,
            'index_memory_bytes': index_memory_bytes,
            'index_memory_mb': index_memory_mb,
            'column_memory': column_memory,
            'row_count': int(len(df)),  # Convert to native int
            'column_count': int(len(df.columns))  # Convert to native int
        }
    
    def determine_processing_strategy(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Determine optimal processing strategy for DataFrame.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary containing strategy recommendation and analysis
        """
        memory_stats = self.calculate_memory_footprint(df)
        
        # Check thresholds
        exceeds_row_threshold = memory_stats['row_count'] > self.row_threshold
        exceeds_memory_threshold = memory_stats['total_memory_mb'] > self.memory_threshold_mb
        
        # Determine strategy
        if exceeds_row_threshold or exceeds_memory_threshold:
            strategy = ProcessingStrategy.SERVER_SIDE
            reason = []
            if exceeds_row_threshold:
                reason.append(f"Row count ({memory_stats['row_count']:,}) exceeds threshold ({self.row_threshold:,})")
            if exceeds_memory_threshold:
                reason.append(f"Memory usage ({memory_stats['total_memory_mb']:.2f} MB) exceeds threshold ({self.memory_threshold_mb} MB)")
        else:
            strategy = ProcessingStrategy.IN_MEMORY
            reason = ["DataFrame is within thresholds for in-memory processing"]
        
        return {
            'strategy': strategy.value,  # Convert enum to string for JSON serialization
            'reason': reason,
            'memory_stats': memory_stats,
            'thresholds': {
                'row_threshold': self.row_threshold,
                'memory_threshold_mb': self.memory_threshold_mb
            },
            'recommendations': self._generate_recommendations(memory_stats, strategy)
        }
    
    def _generate_recommendations(self, memory_stats: Dict[str, Any],
                                strategy: ProcessingStrategy) -> List[str]:
        """
        Generate performance recommendations.
        
        Args:
            memory_stats: Memory statistics
            strategy: Recommended processing strategy
            
        Returns:
            List of performance recommendations
        """
        recommendations = []
        
        if strategy == ProcessingStrategy.SERVER_SIDE:
            recommendations.append("Consider server-side processing for better performance")
            recommendations.append("Enable pagination to reduce client-side memory usage")
            
            # Check for memory-heavy columns
            if memory_stats['column_memory']:
                heavy_columns = [
                    col for col, info in memory_stats['column_memory'].items()
                    if info['mb'] > 1.0  # Columns using more than 1MB
                ]
                if heavy_columns:
                    recommendations.append(f"Consider optimizing heavy columns: {', '.join(heavy_columns)}")
        
        # Check for object dtypes that might be optimized
        if memory_stats['column_memory']:
            object_columns = [
                col for col, info in memory_stats['column_memory'].items()
                if 'object' in info['dtype']
            ]
            if object_columns:
                recommendations.append(f"Consider converting object columns to categorical: {', '.join(object_columns)}")
        
        return recommendations

class DataFrameConverter:
    """Converts pandas DataFrames to Cacao table format with support for styling and pagination."""
    
    def __init__(self, df: pd.DataFrame, size_analyzer: Optional[DataFrameSizeAnalyzer] = None):
        """
        Initialize the converter with a DataFrame.
        
        Args:
            df: pandas DataFrame to convert
            size_analyzer: Optional size analyzer instance
        """
        self.df = df
        self._page_size = 10
        self._current_page = 0
        self._sort_column = None
        self._sort_ascending = True
        self._size_analyzer = size_analyzer or DataFrameSizeAnalyzer()
        self._processing_strategy = None
        self._dtype_metadata = None
        self._column_metadata = None
        self._analyze_dataframe()
    
    def _analyze_dataframe(self) -> None:
        """Analyze the DataFrame to determine processing strategy and extract metadata."""
        # Get processing strategy recommendation
        strategy_info = self._size_analyzer.determine_processing_strategy(self.df)
        self._processing_strategy = strategy_info
        
        # Extract column metadata
        self._column_metadata = self._extract_column_metadata()
        
        # Extract dtype metadata
        self._dtype_metadata = self._extract_dtype_metadata()
    
    def _extract_column_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata for each column.
        
        Returns:
            Dictionary containing column metadata
        """
        metadata = {}
        
        for col in self.df.columns:
            series = self.df[col]
            col_metadata = {
                'name': col,
                'dtype': str(series.dtype),
                'null_count': int(series.isnull().sum()),  # Convert to native int
                'non_null_count': int(series.count()),  # Convert to native int
                'unique_count': int(series.nunique()),  # Convert to native int
                'memory_usage_mb': float(series.memory_usage(deep=True) / (1024 * 1024))  # Convert to native float
            }
            
            # Add type-specific metadata
            if pd.api.types.is_numeric_dtype(series):
                min_val = series.min() if series.count() > 0 else None
                max_val = series.max() if series.count() > 0 else None
                mean_val = series.mean() if series.count() > 0 else None
                std_val = series.std() if series.count() > 0 else None
                
                col_metadata.update({
                    'min_value': float(min_val) if min_val is not None and not pd.isna(min_val) else None,
                    'max_value': float(max_val) if max_val is not None and not pd.isna(max_val) else None,
                    'mean_value': float(mean_val) if mean_val is not None and not pd.isna(mean_val) else None,
                    'std_value': float(std_val) if std_val is not None and not pd.isna(std_val) else None
                })
            elif pd.api.types.is_datetime64_any_dtype(series):
                min_date = series.min() if series.count() > 0 else None
                max_date = series.max() if series.count() > 0 else None
                col_metadata.update({
                    'min_date': min_date.isoformat() if min_date is not None and not pd.isna(min_date) else None,
                    'max_date': max_date.isoformat() if max_date is not None and not pd.isna(max_date) else None,
                    'timezone': str(series.dtype.tz) if hasattr(series.dtype, 'tz') and series.dtype.tz else None
                })
            elif isinstance(series.dtype, pd.CategoricalDtype):
                col_metadata.update({
                    'categories': series.cat.categories.tolist() if hasattr(series, 'cat') else [],
                    'ordered': bool(series.cat.ordered) if hasattr(series, 'cat') else False
                })
            elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
                if series.count() > 0:
                    max_len = series.str.len().max() if hasattr(series, 'str') else None
                    min_len = series.str.len().min() if hasattr(series, 'str') else None
                    avg_len = series.str.len().mean() if hasattr(series, 'str') else None
                    col_metadata.update({
                        'max_length': int(max_len) if max_len is not None and not pd.isna(max_len) else None,
                        'min_length': int(min_len) if min_len is not None and not pd.isna(min_len) else None,
                        'avg_length': float(avg_len) if avg_len is not None and not pd.isna(avg_len) else None
                    })
            
            metadata[col] = col_metadata
        
        return metadata
    
    def _extract_dtype_metadata(self) -> Dict[str, Any]:
        """
        Extract comprehensive dtype information for serialization.
        
        Returns:
            Dictionary containing dtype metadata
        """
        dtype_info = {}
        
        for col in self.df.columns:
            series = self.df[col]
            dtype_str = str(series.dtype)
            
            # Categorize dtype
            if pd.api.types.is_integer_dtype(series):
                dtype_category = 'integer'
                dtype_info[col] = {
                    'category': dtype_category,
                    'dtype': dtype_str,
                    'nullable': pd.api.types.is_extension_array_dtype(series),
                    'signed': not dtype_str.startswith('uint')
                }
            elif pd.api.types.is_float_dtype(series):
                dtype_category = 'float'
                dtype_info[col] = {
                    'category': dtype_category,
                    'dtype': dtype_str,
                    'nullable': pd.api.types.is_extension_array_dtype(series)
                }
            elif pd.api.types.is_bool_dtype(series):
                dtype_category = 'boolean'
                dtype_info[col] = {
                    'category': dtype_category,
                    'dtype': dtype_str,
                    'nullable': pd.api.types.is_extension_array_dtype(series)
                }
            elif pd.api.types.is_datetime64_any_dtype(series):
                dtype_category = 'datetime'
                dtype_info[col] = {
                    'category': dtype_category,
                    'dtype': dtype_str,
                    'timezone': str(series.dtype.tz) if hasattr(series.dtype, 'tz') and series.dtype.tz else None,
                    'unit': series.dtype.unit if hasattr(series.dtype, 'unit') else None
                }
            elif isinstance(series.dtype, pd.CategoricalDtype):
                dtype_category = 'categorical'
                dtype_info[col] = {
                    'category': dtype_category,
                    'dtype': dtype_str,
                    'categories': series.cat.categories.tolist(),
                    'ordered': series.cat.ordered,
                    'codes_dtype': str(series.cat.codes.dtype)
                }
            elif pd.api.types.is_string_dtype(series):
                dtype_category = 'string'
                dtype_info[col] = {
                    'category': dtype_category,
                    'dtype': dtype_str,
                    'nullable': True
                }
            else:
                dtype_category = 'object'
                dtype_info[col] = {
                    'category': dtype_category,
                    'dtype': dtype_str,
                    'nullable': True
                }
        
        return dtype_info
    
    def get_processing_strategy(self) -> Dict[str, Any]:
        """
        Get the processing strategy recommendation.
        
        Returns:
            Processing strategy information
        """
        return self._processing_strategy
    
    def get_column_metadata(self) -> Dict[str, Any]:
        """
        Get column metadata.
        
        Returns:
            Column metadata dictionary
        """
        return self._column_metadata
    
    def get_dtype_metadata(self) -> Dict[str, Any]:
        """
        Get dtype metadata.
        
        Returns:
            Dtype metadata dictionary
        """
        return self._dtype_metadata

    @property
    def total_pages(self) -> int:
        """Calculate total number of pages based on DataFrame size and page_size."""
        return int(max(1, (len(self.df) + self._page_size - 1) // self._page_size))

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the converter with pagination and sorting settings.
        
        Args:
            config: Dictionary containing configuration options
        """
        self._page_size = config.get('page_size', 10)
        self._current_page = config.get('current_page', 0)
        self._sort_column = config.get('sort_column', None)
        self._sort_ascending = config.get('sort_ascending', True)

    def _format_value(self, value: Any, dtype_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Format DataFrame values for display with enhanced type preservation.
        
        Args:
            value: Value to format
            dtype_info: Optional dtype information for enhanced formatting
            
        Returns:
            Dictionary containing formatted value and metadata
        """
        if pd.isna(value):
            return {
                'display_value': '',
                'raw_value': None,
                'is_null': True,
                'value_type': 'null'
            }
        
        # Handle different data types with preservation
        if isinstance(value, (int, np.integer)):
            return {
                'display_value': str(value),
                'raw_value': int(value),
                'is_null': False,
                'value_type': 'integer'
            }
        elif isinstance(value, (float, np.floating)):
            return {
                'display_value': f'{value:.4g}',
                'raw_value': float(value),
                'is_null': False,
                'value_type': 'float'
            }
        elif isinstance(value, (bool, np.bool_)):
            return {
                'display_value': str(value),
                'raw_value': bool(value),
                'is_null': False,
                'value_type': 'boolean'
            }
        elif isinstance(value, (pd.Timestamp, np.datetime64)):
            formatted_date = value.strftime('%Y-%m-%d %H:%M:%S') if hasattr(value, 'strftime') else str(value)
            return {
                'display_value': formatted_date,
                'raw_value': value.isoformat() if hasattr(value, 'isoformat') else str(value),
                'is_null': False,
                'value_type': 'datetime',
                'timezone': str(value.tz) if hasattr(value, 'tz') and value.tz else None
            }
        elif isinstance(value, pd.CategoricalDtype) or (hasattr(value, 'categories')):
            return {
                'display_value': str(value),
                'raw_value': str(value),
                'is_null': False,
                'value_type': 'categorical'
            }
        elif isinstance(value, str):
            return {
                'display_value': value,
                'raw_value': value,
                'is_null': False,
                'value_type': 'string'
            }
        else:
            return {
                'display_value': str(value),
                'raw_value': str(value),
                'is_null': False,
                'value_type': 'object'
            }
    
    def _format_value_simple(self, value: Any) -> str:
        """
        Simple format for backward compatibility.
        
        Args:
            value: Value to format
            
        Returns:
            Formatted string representation of the value
        """
        formatted = self._format_value(value)
        return formatted['display_value']

    def get_headers(self) -> List[str]:
        """
        Get column headers including the index if visible.
        
        Returns:
            List of column headers
        """
        headers = []
        if self.df.index.name:
            headers.append(self.df.index.name)
        elif not self.df.index.equals(pd.RangeIndex(len(self.df))):
            headers.append('Index')
        headers.extend(self.df.columns.tolist())
        return headers

    def get_rows(self, page: Optional[int] = None, enhanced: bool = False) -> List[List[str]]:
        """
        Get formatted rows for the current page.
        
        Args:
            page: Optional page number to fetch (defaults to current page)
            enhanced: If True, store enhanced metadata but still return simple display strings
            
        Returns:
            List of rows with formatted string values for display
        """
        if page is not None:
            self._current_page = max(0, min(page, self.total_pages - 1))

        # Apply sorting if specified
        df = self.df
        if self._sort_column and self._sort_column in df.columns:
            df = df.sort_values(by=self._sort_column, ascending=self._sort_ascending)

        # Calculate slice indices for pagination
        start_idx = self._current_page * self._page_size
        end_idx = start_idx + self._page_size
        page_df = df.iloc[start_idx:end_idx]

        # Format rows including index if needed - always use simple format for display
        rows = []
        for idx, row in page_df.iterrows():
            formatted_row = []
            
            # Add index if needed
            if not page_df.index.equals(pd.RangeIndex(len(page_df))):
                formatted_row.append(self._format_value_simple(idx))
            
            # Add row values - always use simple format for display
            formatted_row.extend(self._format_value_simple(v) for v in row)
            
            rows.append(formatted_row)

        return rows
    
    def get_enhanced_rows(self, page: Optional[int] = None) -> List[List[str]]:
        """
        Get enhanced formatted rows with full metadata for current page.
        Note: This now returns the same as get_rows but with enhanced metadata stored.
        
        Args:
            page: Optional page number to fetch (defaults to current page)
            
        Returns:
            List of rows with formatted string values for display
        """
        return self.get_rows(page=page, enhanced=True)

    def to_table_data(self, enhanced: bool = False, include_all_rows: bool = False) -> Dict[str, Any]:
        """
        Convert current DataFrame view to Cacao table format.
        
        Args:
            enhanced: If True, include enhanced metadata and processing info
            include_all_rows: If True, include all rows instead of just current page
        
        Returns:
            Dictionary containing table data and metadata
        """
        # For large datasets that will use advanced mode, provide all rows
        if include_all_rows or self.should_use_server_side_processing():
            rows = self.get_all_rows()
        else:
            rows = self.get_rows(enhanced=enhanced)
        
        base_data = {
            "headers": self.get_headers(),
            "rows": rows,
            "metadata": {
                "total_rows": int(len(self.df)),  # Convert to native int
                "total_pages": int(self.total_pages),  # Convert to native int
                "current_page": int(self._current_page),  # Convert to native int
                "page_size": int(self._page_size),  # Convert to native int
                "sort_column": self._sort_column,
                "sort_ascending": bool(self._sort_ascending)  # Convert to native bool
            }
        }
        
        if enhanced:
            base_data["metadata"].update({
                "processing_strategy": self._processing_strategy,
                "column_metadata": self._column_metadata,
                "dtype_metadata": self._dtype_metadata,
                "enhanced_format": True
            })
        
        return base_data
    
    def get_all_rows(self) -> List[List[str]]:
        """
        Get all formatted rows for large datasets using advanced mode.
        
        Returns:
            List of all rows with formatted string values for display
        """
        # Apply sorting if specified
        df = self.df
        if self._sort_column and self._sort_column in df.columns:
            df = df.sort_values(by=self._sort_column, ascending=self._sort_ascending)
        
        # Format all rows - always use simple format for display
        rows = []
        for idx, row in df.iterrows():
            formatted_row = []
            
            # Add index if needed
            if not df.index.equals(pd.RangeIndex(len(df))):
                formatted_row.append(self._format_value_simple(idx))
            
            # Add row values - always use simple format for display
            formatted_row.extend(self._format_value_simple(v) for v in row)
            
            rows.append(formatted_row)
        
        return rows
    
    def to_enhanced_table_data(self) -> Dict[str, Any]:
        """
        Convert DataFrame to enhanced table format with full metadata.
        
        Returns:
            Dictionary containing enhanced table data and comprehensive metadata
        """
        return self.to_table_data(enhanced=True)
    
    def get_conversion_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the conversion process and recommendations.
        
        Returns:
            Dictionary containing conversion summary
        """
        strategy = self._processing_strategy
        
        return {
            "dataframe_shape": [int(x) for x in self.df.shape],  # Convert tuple to list of native ints
            "memory_usage_mb": float(strategy['memory_stats']['total_memory_mb']),
            "processing_strategy": strategy['strategy'],  # Already converted to string value
            "strategy_reason": strategy['reason'],
            "recommendations": strategy['recommendations'],
            "dtype_summary": {
                category: len([col for col, info in self._dtype_metadata.items()
                              if info['category'] == category])
                for category in ['integer', 'float', 'boolean', 'datetime', 'categorical', 'string', 'object']
            },
            "null_columns": [
                col for col, info in self._column_metadata.items()
                if info['null_count'] > 0
            ]
        }
    
    def should_use_server_side_processing(self) -> bool:
        """
        Determine if server-side processing should be used.
        
        Returns:
            True if server-side processing is recommended
        """
        return self._processing_strategy['strategy'] == ProcessingStrategy.SERVER_SIDE.value
