"""
Data utilities for Cacao v2.

Provides helpers for loading, transforming, and displaying data.

Example:
    from cacao.data import load_csv, load_json, dataframe

    # Load data
    df = load_csv("sales.csv")

    # Display as table
    table(df, sortable=True, searchable=True)
"""

from __future__ import annotations

from typing import Any, Callable, TypeVar
from pathlib import Path
import json

T = TypeVar("T")


class DataFrame:
    """
    Simple DataFrame-like class for data manipulation.

    Provides a lightweight alternative when pandas isn't needed.
    Also works as a wrapper around pandas DataFrames.
    """

    def __init__(self, data: list[dict[str, Any]] | dict[str, list[Any]] | Any):
        """
        Create a DataFrame.

        Args:
            data: List of dicts, dict of lists, or pandas DataFrame
        """
        # Handle pandas DataFrame
        if hasattr(data, 'to_dict'):
            self._data = data.to_dict('records')
            self._pandas = data
        # Handle dict of lists (columnar format)
        elif isinstance(data, dict) and data:
            first_key = next(iter(data))
            if isinstance(data[first_key], list):
                length = len(data[first_key])
                self._data = [{k: data[k][i] for k in data} for i in range(length)]
            else:
                self._data = [data]
            self._pandas = None
        # Handle list of dicts
        elif isinstance(data, list):
            self._data = data
            self._pandas = None
        else:
            self._data = []
            self._pandas = None

    @property
    def columns(self) -> list[str]:
        """Get column names."""
        if self._data:
            return list(self._data[0].keys())
        return []

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key: str | int | slice) -> Any:
        if isinstance(key, str):
            return [row[key] for row in self._data]
        return self._data[key]

    def to_dict(self, orient: str = "records") -> Any:
        """Convert to dict format."""
        if orient == "records":
            return self._data
        elif orient == "list":
            if not self._data:
                return {}
            return {col: [row[col] for row in self._data] for col in self.columns}
        return self._data

    def filter(self, condition: Callable[[dict[str, Any]], bool]) -> "DataFrame":
        """
        Filter rows by condition.

        Example:
            df.filter(lambda row: row["age"] > 18)
        """
        return DataFrame([row for row in self._data if condition(row)])

    def select(self, *columns: str) -> "DataFrame":
        """
        Select specific columns.

        Example:
            df.select("name", "email")
        """
        return DataFrame([{col: row[col] for col in columns if col in row}
                         for row in self._data])

    def sort(self, column: str, reverse: bool = False) -> "DataFrame":
        """
        Sort by column.

        Example:
            df.sort("date", reverse=True)
        """
        return DataFrame(sorted(self._data, key=lambda x: x.get(column), reverse=reverse))

    def limit(self, n: int) -> "DataFrame":
        """
        Limit to first n rows.

        Example:
            df.limit(10)
        """
        return DataFrame(self._data[:n])

    def head(self, n: int = 5) -> "DataFrame":
        """Get first n rows."""
        return self.limit(n)

    def tail(self, n: int = 5) -> "DataFrame":
        """Get last n rows."""
        return DataFrame(self._data[-n:])

    def map(self, column: str, fn: Callable[[Any], Any]) -> "DataFrame":
        """
        Apply function to column.

        Example:
            df.map("price", lambda x: x * 1.1)
        """
        return DataFrame([{**row, column: fn(row[column])} for row in self._data])

    def add_column(self, name: str, fn: Callable[[dict[str, Any]], Any]) -> "DataFrame":
        """
        Add computed column.

        Example:
            df.add_column("total", lambda row: row["price"] * row["quantity"])
        """
        return DataFrame([{**row, name: fn(row)} for row in self._data])

    def group_by(self, column: str) -> dict[Any, "DataFrame"]:
        """
        Group by column value.

        Example:
            groups = df.group_by("category")
            for category, group_df in groups.items():
                print(category, len(group_df))
        """
        groups: dict[Any, list[dict[str, Any]]] = {}
        for row in self._data:
            key = row.get(column)
            if key not in groups:
                groups[key] = []
            groups[key].append(row)
        return {k: DataFrame(v) for k, v in groups.items()}

    def aggregate(self, **aggs: Callable[[list[Any]], Any]) -> dict[str, Any]:
        """
        Aggregate columns.

        Example:
            df.aggregate(
                total_revenue=lambda rows: sum(r["revenue"] for r in rows),
                avg_price=lambda rows: sum(r["price"] for r in rows) / len(rows)
            )
        """
        return {name: fn(self._data) for name, fn in aggs.items()}

    def unique(self, column: str) -> list[Any]:
        """Get unique values in column."""
        return list(set(row[column] for row in self._data if column in row))

    def count(self) -> int:
        """Count rows."""
        return len(self._data)

    def sum(self, column: str) -> float:
        """Sum column values."""
        return sum(row[column] for row in self._data if column in row)

    def mean(self, column: str) -> float:
        """Average column values."""
        values = [row[column] for row in self._data if column in row]
        return sum(values) / len(values) if values else 0

    def min(self, column: str) -> Any:
        """Min column value."""
        values = [row[column] for row in self._data if column in row]
        return min(values) if values else None

    def max(self, column: str) -> Any:
        """Max column value."""
        values = [row[column] for row in self._data if column in row]
        return max(values) if values else None


def load_csv(
    path: str | Path,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> DataFrame:
    """
    Load CSV file.

    Example:
        df = load_csv("data/sales.csv")
    """
    import csv

    path = Path(path)
    with open(path, newline="", encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        data = list(reader)

    # Try to convert numeric strings
    for row in data:
        for key, value in row.items():
            if isinstance(value, str):
                try:
                    if "." in value:
                        row[key] = float(value)
                    else:
                        row[key] = int(value)
                except ValueError:
                    pass

    return DataFrame(data)


def load_json(path: str | Path) -> DataFrame:
    """
    Load JSON file.

    Example:
        df = load_json("data/users.json")
    """
    path = Path(path)
    with open(path) as f:
        data = json.load(f)

    if isinstance(data, list):
        return DataFrame(data)
    elif isinstance(data, dict):
        # Check if it's columnar format
        first_value = next(iter(data.values()), None)
        if isinstance(first_value, list):
            return DataFrame(data)
        return DataFrame([data])
    return DataFrame([])


def load_parquet(path: str | Path) -> DataFrame:
    """
    Load Parquet file (requires pandas/pyarrow).

    Example:
        df = load_parquet("data/large_data.parquet")
    """
    try:
        import pandas as pd
        df = pd.read_parquet(path)
        return DataFrame(df)
    except ImportError:
        raise ImportError("pandas and pyarrow required for parquet support")


def from_pandas(df: Any) -> DataFrame:
    """
    Convert pandas DataFrame to Cacao DataFrame.

    Example:
        import pandas as pd
        pdf = pd.read_csv("data.csv")
        df = from_pandas(pdf)
    """
    return DataFrame(df)


def from_records(records: list[dict[str, Any]]) -> DataFrame:
    """
    Create DataFrame from list of records.

    Example:
        df = from_records([
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ])
    """
    return DataFrame(records)


def from_dict(data: dict[str, list[Any]]) -> DataFrame:
    """
    Create DataFrame from columnar dict.

    Example:
        df = from_dict({
            "name": ["Alice", "Bob"],
            "age": [30, 25],
        })
    """
    return DataFrame(data)


# Sample data generators for demos
def sample_sales_data(n: int = 100) -> DataFrame:
    """Generate sample sales data for demos."""
    import random
    from datetime import datetime, timedelta

    categories = ["Electronics", "Clothing", "Food", "Books", "Home"]
    data = []
    base_date = datetime.now() - timedelta(days=n)

    for i in range(n):
        data.append({
            "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "revenue": random.randint(1000, 10000),
            "orders": random.randint(10, 100),
            "category": random.choice(categories),
            "profit": random.randint(100, 2000),
        })

    return DataFrame(data)


def sample_users_data(n: int = 50) -> DataFrame:
    """Generate sample user data for demos."""
    import random

    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    domains = ["gmail.com", "yahoo.com", "company.com"]
    roles = ["Admin", "User", "Editor", "Viewer"]
    statuses = ["Active", "Inactive", "Pending"]

    data = []
    for i in range(n):
        name = random.choice(names) + str(i)
        data.append({
            "id": i + 1,
            "name": name,
            "email": f"{name.lower()}@{random.choice(domains)}",
            "role": random.choice(roles),
            "status": random.choice(statuses),
            "created": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        })

    return DataFrame(data)


__all__ = [
    "DataFrame",
    "load_csv",
    "load_json",
    "load_parquet",
    "from_pandas",
    "from_records",
    "from_dict",
    "sample_sales_data",
    "sample_users_data",
]
