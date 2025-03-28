"""
Pandas DataFrame Table Plugin for Cacao
Provides table visualization for pandas DataFrames with sorting, pagination, and styling.
"""

from .plugin import PandasTablePlugin

__version__ = "0.1.0"

# Export the plugin class
__all__ = ["PandasTablePlugin"]

# Plugin registration function
def register_plugin():
    """Register the pandas table plugin with Cacao."""
    return PandasTablePlugin()
