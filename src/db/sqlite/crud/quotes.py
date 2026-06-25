from __future__ import annotations

import sqlite3

from typing import Optional, Dict, List, Any

from src.db.sqlite.connection import get_connection


def get_random_quote(

        category: Optional[str] = None,
        conn: Optional[sqlite3.Connection] = None,

    ) -> Optional[Dict[str, Any]]:
    """

    """
    conn = get_connection() if conn is None else conn
    conn.row_factory = _dict_factory

    with conn:

        cursor = conn.cursor()

        if category is None:

            cursor.execute("""
                SELECT
                    id_quote AS id,
                    category,
                    author,
                    quote,
                    is_active,
                    sort_order,
                    created_at,
                    updated_at
                FROM quotes
                WHERE is_active = 1
                ORDER BY RANDOM()
                LIMIT 1;
            """)

        else:

            cursor.execute("""
                SELECT
                    id_quote AS id,
                    category,
                    author,
                    quote,
                    is_active,
                    sort_order,
                    created_at,
                    updated_at
                FROM quotes
                WHERE category = ?
                  AND is_active = 1
                ORDER BY RANDOM()
                LIMIT 1;
            """, (category,))

        return cursor.fetchone()


def get_quotes_by_category(

        category: str = "Economics",
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
                id_quote AS id,
                category,
                author,
                quote,
                is_active,
                sort_order,
                created_at,
                updated_at
            FROM quotes
            WHERE category = ?
              AND is_active = 1
            ORDER BY sort_order, author;
        """, (category,))

        return cursor.fetchall()


def get_all_quotes(

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
                id_quote AS id,
                category,
                author,
                quote,
                is_active,
                sort_order,
                created_at,
                updated_at
            FROM quotes
            WHERE is_active = 1
            ORDER BY category, sort_order, author;
        """)

        return cursor.fetchall()


def _dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:

    return {
        column[0]: row[index]
        for index, column in enumerate(cursor.description)
    }