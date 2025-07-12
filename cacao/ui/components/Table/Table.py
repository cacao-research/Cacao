
from typing import Any, Dict
from ..base import Component

class EnhancedTable(Component):
    """
    A table component with sorting, filtering, and pagination capabilities.
    """
    def __init__(
        self,
        columns,
        data_source,
        pagination = None,
        sorting = None,
        filters = None,
        **kwargs
    ) -> None:
        self.columns = columns
        self.data_source = data_source
        self.pagination = pagination or {"page_size": 10, "current": 1}
        self.sorting = sorting
        self.filters = filters
        self.extra_props = kwargs

    def render(self) -> Dict[str, Any]:
        return {
            "type": "EnhancedTable",
            "props": {
                "columns": self.columns,
                "dataSource": self.data_source,
                "pagination": self.pagination,
                "sorting": self.sorting,
                "filters": self.filters,
                **self.extra_props
            }
        }
