from __future__ import annotations

import sqlite3

from typing import Optional, Dict, List, Any

from src.db.sqlite.connection import get_connection


def get_currency_by_code(

        code: str,
        conn: Optional[sqlite3.Connection] = None,

    ) -> Optional[Dict[str, Any]]:
    """

    """
    conn = get_connection() if conn is None else conn
    conn.row_factory = _dict_factory

    with conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id_ccy AS id,
                code,
                name,
                symbol,
                iso_numeric,
                decimals,
                is_active,
                sort_order,
                created_at,
                updated_at
            FROM currencies
            WHERE code = ?
              AND is_active = 1
            LIMIT 1;
        """, (code.upper(),))

        return cursor.fetchone()


def get_currency_by_id(

        id_ccy: int,
        conn: Optional[sqlite3.Connection] = None,

    ) -> Optional[Dict[str, Any]]:
    """

    """
    conn = get_connection() if conn is None else conn
    conn.row_factory = _dict_factory

    with conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id_ccy AS id,
                code,
                name,
                symbol,
                iso_numeric,
                decimals,
                is_active,
                sort_order,
                created_at,
                updated_at
            FROM currencies
            WHERE id_ccy = ?
              AND is_active = 1
            LIMIT 1;
        """, (id_ccy,))

        return cursor.fetchone()


def search_currencies(

        search: str,
        conn: Optional[sqlite3.Connection] = None,

    ) -> List[Dict[str, Any]]:
    """

    """
    conn = get_connection() if conn is None else conn
    conn.row_factory = _dict_factory

    with conn:

        cursor = conn.cursor()
        search_term = f"%{search.strip()}%"

        cursor.execute("""
            SELECT
                id_ccy AS id,
                code,
                name,
                symbol,
                iso_numeric,
                decimals,
                is_active,
                sort_order,
                created_at,
                updated_at
            FROM currencies
            WHERE is_active = 1
              AND (
                    code LIKE ?
                 OR name LIKE ?
                 OR symbol LIKE ?
              )
            ORDER BY sort_order, code;
        """, (search_term, search_term, search_term))

        return cursor.fetchall()


def get_all_currencies(

        conn: Optional[sqlite3.Connection] = None,

    ) -> List[Dict[str, Any]]:
    """

    """
    conn = get_connection() if conn is None else conn
    conn.row_factory = _dict_factory

    with conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id_ccy AS id,
                code,
                name,
                symbol,
                iso_numeric,
                decimals,
                is_active,
                sort_order,
                created_at,
                updated_at
            FROM currencies
            WHERE is_active = 1
            ORDER BY sort_order, code;
        """)

        return cursor.fetchall()


def _dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:

    return {
        column[0]: row[index]
        for index, column in enumerate(cursor.description)
    }
