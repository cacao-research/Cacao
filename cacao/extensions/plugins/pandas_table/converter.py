"""
Converter module for transforming pandas DataFrames into Cacao table components.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np

class DataFrameConverter:
    """Converts pandas DataFrames to Cacao table format with support for styling and pagination."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the converter with a DataFrame.
        
        Args:
            df: pandas DataFrame to convert
        """
        self.df = df
        self._page_size = 10
        self._current_page = 0
        self._sort_column = None
        self._sort_ascending = True

    @property
    def total_pages(self) -> int:
        """Calculate total number of pages based on DataFrame size and page_size."""
        return max(1, (len(self.df) + self._page_size - 1) // self._page_size)

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

    def _format_value(self, value: Any) -> str:
        """
        Format DataFrame values for display.
        
        Args:
            value: Value to format
            
        Returns:
            Formatted string representation of the value
        """
        if pd.isna(value):
            return ''
        elif isinstance(value, (float, np.floating)):
            return f'{value:.4g}'
        elif isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return str(value)

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

    def get_rows(self, page: Optional[int] = None) -> List[List[str]]:
        """
        Get formatted rows for the current page.
        
        Args:
            page: Optional page number to fetch (defaults to current page)
            
        Returns:
            List of rows with formatted values
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

        # Format rows including index if needed
        rows = []
        for idx, row in page_df.iterrows():
            formatted_row = []
            if not page_df.index.equals(pd.RangeIndex(len(page_df))):
                formatted_row.append(self._format_value(idx))
            formatted_row.extend(self._format_value(v) for v in row)
            rows.append(formatted_row)

        return rows

    def to_table_data(self) -> Dict[str, Any]:
        """
        Convert current DataFrame view to Cacao table format.
        
        Returns:
            Dictionary containing table data and metadata
        """
        return {
            "headers": self.get_headers(),
            "rows": self.get_rows(),
            "metadata": {
                "total_rows": len(self.df),
                "total_pages": self.total_pages,
                "current_page": self._current_page,
                "page_size": self._page_size,
                "sort_column": self._sort_column,
                "sort_ascending": self._sort_ascending
            }
        }
