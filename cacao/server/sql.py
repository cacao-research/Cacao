"""
SQL query handler for Cacao.

Executes SQL queries against SQLite or SQLAlchemy-compatible databases
and returns results to the client via WebSocket.
"""

from __future__ import annotations

import asyncio
import sqlite3
from typing import TYPE_CHECKING, Any

from .log import get_logger

if TYPE_CHECKING:
    from .session import Session

logger = get_logger("cacao.sql")


async def handle_sql_query(
    session: Session,
    connection: str,
    conn_type: str,
    query: str,
    max_rows: int = 1000,
) -> None:
    """Execute a SQL query and send results back to the client."""
    try:
        if conn_type == "sqlite":
            results = await asyncio.to_thread(_execute_sqlite, connection, query, max_rows)
        elif conn_type == "sqlalchemy":
            results = await asyncio.to_thread(_execute_sqlalchemy, connection, query, max_rows)
        else:
            await session.send(
                {
                    "type": "sql:result",
                    "error": f"Unsupported connection type: {conn_type}",
                }
            )
            return

        await session.send(
            {
                "type": "sql:result",
                "data": results["data"],
                "columns": results["columns"],
                "rowcount": results["rowcount"],
            }
        )
    except Exception as e:
        logger.exception("SQL query error", extra={"label": "sql"})
        await session.send(
            {
                "type": "sql:error",
                "error": str(e),
            }
        )


def _execute_sqlite(connection: str, query: str, max_rows: int) -> dict[str, Any]:
    """Execute a query against a SQLite database."""
    # Parse connection string: sqlite:///path or just path
    db_path = connection
    if db_path.startswith("sqlite:///"):
        db_path = db_path[len("sqlite:///") :]
    elif db_path.startswith("sqlite://"):
        db_path = db_path[len("sqlite://") :]

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchmany(max_rows)
        data = [dict(row) for row in rows]
        return {
            "data": data,
            "columns": columns,
            "rowcount": len(data),
        }
    finally:
        conn.close()


def _execute_sqlalchemy(connection: str, query: str, max_rows: int) -> dict[str, Any]:
    """Execute a query using SQLAlchemy."""
    try:
        from sqlalchemy import create_engine, text
    except ImportError:
        raise ImportError(
            "SQLAlchemy is required for non-SQLite databases. "
            "Install it with: pip install sqlalchemy"
        )

    engine = create_engine(connection)
    with engine.connect() as conn:
        result = conn.execute(text(query))
        columns = list(result.keys()) if result.returns_rows else []
        if result.returns_rows:
            rows = result.fetchmany(max_rows)
            data = [dict(zip(columns, row)) for row in rows]
        else:
            data = []
        return {
            "data": data,
            "columns": columns,
            "rowcount": len(data),
        }
