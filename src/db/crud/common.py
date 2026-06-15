from __future__ import annotations

import json

from pathlib import Path
from typing import Any, Iterable, Optional

from src.db.connection import get_connection, row_to_dict, rows_to_dicts


def encode_json(value: Any) -> Optional[str]:
    """
    Store dict/list values as JSON while allowing pre-serialized strings.
    """
    if value is None:
        return None

    if isinstance(value, str):
        return value

    return json.dumps(value, default=str)


def fetch_one(sql: str, params: Iterable[Any] = (), db_path: Optional[str | Path] = None) -> Optional[dict]:
    with get_connection(db_path) as connection:
        row = connection.execute(sql, tuple(params)).fetchone()

    return row_to_dict(row)


def fetch_all(sql: str, params: Iterable[Any] = (), db_path: Optional[str | Path] = None) -> list[dict]:
    with get_connection(db_path) as connection:
        rows = connection.execute(sql, tuple(params)).fetchall()

    return rows_to_dicts(rows)


def execute(sql: str, params: Iterable[Any] = (), db_path: Optional[str | Path] = None) -> int:
    with get_connection(db_path) as connection:
        cursor = connection.execute(sql, tuple(params))
        connection.commit()

    return cursor.rowcount


def insert_and_get_id(sql: str, params: Iterable[Any] = (), db_path: Optional[str | Path] = None) -> int:
    with get_connection(db_path) as connection:
        cursor = connection.execute(sql, tuple(params))
        connection.commit()

    return int(cursor.lastrowid)


def build_filters(filters: dict[str, Any]) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []

    for column, value in filters.items():
        if value is None:
            continue

        clauses.append(f"{column} = ?")
        params.append(value)

    if not clauses:
        return "", params

    return " WHERE " + " AND ".join(clauses), params


def build_update(values: dict[str, Any]) -> tuple[str, list[Any]]:
    updates = {key: value for key, value in values.items() if value is not None}

    if not updates:
        raise ValueError("At least one update value must be provided")

    set_clause = ", ".join([f"{key} = ?" for key in updates])

    return set_clause, list(updates.values())

