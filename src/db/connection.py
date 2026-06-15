from __future__ import annotations

import sqlite3

from pathlib import Path
from typing import Optional


DATABASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE_PATH = DATABASE_DIR / "AEGIS_DATABASE.db"
LEGACY_DATABASE_PATH = DATABASE_DIR / "AEGIS.db"
DATABASE_PATH = DEFAULT_DATABASE_PATH if DEFAULT_DATABASE_PATH.exists() else LEGACY_DATABASE_PATH


def get_connection(db_path: Optional[str | Path] = None) -> sqlite3.Connection:
    """
    Return a SQLite connection configured for AEGIS.
    """
    path = Path(db_path) if db_path is not None else DATABASE_PATH
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def row_to_dict(row: Optional[sqlite3.Row]) -> Optional[dict]:
    """
    Convert one SQLite row to a dict.
    """
    if row is None:
        return None

    return dict(row)


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    """
    Convert SQLite rows to plain dicts.
    """
    return [dict(row) for row in rows]
