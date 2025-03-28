"""
Main plugin implementation for pandas DataFrame table visualization.
"""

from typing import Any, Dict, Optional
import pandas as pd
from cacao.plugins.base_plugin import BasePlugin
from cacao.ui.components.data import Table
from .converter import DataFrameConverter

class PandasTablePlugin(BasePlugin):
    """Plugin for rendering pandas DataFrames as interactive tables."""

    def __init__(self):
        super().__init__()
        self._version = "0.1.0"
        self._dependencies = {
            "pandas": ">=2.0.0",
            "numpy": ">=1.24.0"
        }
        self._converters: Dict[str, DataFrameConverter] = {}
        self._table_counter = 0

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

        # Create new converter for this DataFrame
        table_id = self._get_table_id()
        converter = DataFrameConverter(data)
        
        # Apply configuration if available
        if self.config:
            converter.configure(self.config)
        
        # Store converter for future updates
        self._converters[table_id] = converter
        
        # Convert DataFrame to table data
        table_data = converter.to_table_data()
        
        # Create and return Table component
        return Table(
            headers=table_data["headers"],
            rows=table_data["rows"],
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
