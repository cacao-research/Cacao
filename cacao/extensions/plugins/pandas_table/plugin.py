"""
Main plugin implementation for pandas DataFrame table visualization.
"""

from typing import Any, Dict, Optional
import pandas as pd
from cacao.plugins.base_plugin import BasePlugin
from cacao.ui.components.data import Table
from .converter import DataFrameConverter, DataFrameSizeAnalyzer, ProcessingStrategy

class PandasTablePlugin(BasePlugin):
    """Plugin for rendering pandas DataFrames as interactive tables."""

    def __init__(self, enhanced_mode: bool = False,
                 row_threshold: int = 10000,
                 memory_threshold_mb: float = 5.0):
        super().__init__()
        self._version = "0.2.0"
        self._dependencies = {
            "pandas": ">=2.0.0",
            "numpy": ">=1.24.0"
        }
        self._converters: Dict[str, DataFrameConverter] = {}
        self._table_counter = 0
        self._enhanced_mode = enhanced_mode
        self._size_analyzer = DataFrameSizeAnalyzer(
            row_threshold=row_threshold,
            memory_threshold_mb=memory_threshold_mb
        )

    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate plugin configuration.
        
        Args:
            config: Configuration dictionary
            
        Raises:
            ValueError: If configuration is invalid
        """
        if 'page_size' in config and not isinstance(config['page_size'], int):
            raise ValueError("page_size must be an integer")
        if 'page_size' in config and config['page_size'] < 1:
            raise ValueError("page_size must be greater than 0")

    def _initialize_resources(self) -> None:
        """Initialize plugin resources."""
        self._converters.clear()
        self._table_counter = 0

    def _cleanup_resources(self) -> None:
        """Cleanup plugin resources."""
        self._converters.clear()

    def _get_table_id(self) -> str:
        """Generate unique table ID."""
        table_id = f"pandas_table_{self._table_counter}"
        self._table_counter += 1
        return table_id

    def process(self, data: Any) -> Any:
        """
        Process input data and convert DataFrame to table component.
        
        Args:
            data: Input data (expected to be a pandas DataFrame)
            
        Returns:
            Table component or original data if not a DataFrame
            
        Raises:
            TypeError: If data is a DataFrame but required columns are missing
        """
        if not isinstance(data, pd.DataFrame):
            return data

        # Create new converter for this DataFrame with enhanced analyzer
        table_id = self._get_table_id()
        converter = DataFrameConverter(data, size_analyzer=self._size_analyzer)
        
        # Apply configuration if available
        if self.config:
            converter.configure(self.config)
        
        # Store converter for future updates
        self._converters[table_id] = converter
        
        # Determine if we should use advanced mode based on dataset size
        should_use_advanced = converter.should_use_server_side_processing()
        
        # Choose output mode - include all rows for large datasets
        table_data = converter.to_table_data(enhanced=self._enhanced_mode, include_all_rows=should_use_advanced)
        
        if should_use_advanced:
            # Use modern API with advanced features for large datasets
            columns = [{"title": header, "dataIndex": header} for header in table_data["headers"]]
            dataSource = []
            for row in table_data["rows"]:
                row_dict = {}
                for i, header in enumerate(table_data["headers"]):
                    row_dict[header] = row[i] if i < len(row) else ""
                dataSource.append(row_dict)
            
            return Table(
                columns=columns,
                dataSource=dataSource,
                advanced=True,
                page_length=10,  # More rows per page for large datasets
                searching=True,
                ordering=True,
                responsive=True,
                info=True,
                pagination=True,
                metadata={
                    "table_id": table_id,
                    "plugin": "pandas_table",
                    **table_data["metadata"]
                }
            )
        else:
            # Use modern API with advanced mode for small datasets too (for sorting functionality)
            columns = [{"title": header, "dataIndex": header} for header in table_data["headers"]]
            dataSource = []
            for row in table_data["rows"]:
                row_dict = {}
                for i, header in enumerate(table_data["headers"]):
                    row_dict[header] = row[i] if i < len(row) else ""
                dataSource.append(row_dict)
            
            return Table(
                columns=columns,
                dataSource=dataSource,
                advanced=True,  # Enable advanced mode for proper sorting
                page_length=10,  # Default page size for small datasets
                searching=True,
                ordering=True,
                responsive=True,
                info=True,
                pagination=True,
                metadata={
                    "table_id": table_id,
                    "plugin": "pandas_table",
                    **table_data["metadata"]
                }
            )

    def update_table(self, table_id: str, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update existing table with new configuration.
        
        Args:
            table_id: ID of the table to update
            config: New configuration settings
            
        Returns:
            Updated table data or None if table_id not found
        """
        converter = self._converters.get(table_id)
        if not converter:
            return None

        # Update converter configuration
        converter.configure(config)
        
        # Return updated table data
        return converter.to_table_data()
