from __future__ import annotations

import sqlite3
from typing import Optional, Dict, List

from src.db.sqlite.connection import get_connection


def get_random_quote (
    
        category : Optional[str] = None,
        conn : Optional[sqlite3.Connection] = None,

    ) -> Optional[Dict] :
    """
    
    """
    conn = get_connection() if conn is None else conn

    with conn :

        conn.row_factory = _dict_factory
        cursor = conn.cursor()

        if category is None :

            cursor.execute("""
                SELECT id, category, author, quote, created_at
                FROM quotes
                ORDER BY RANDOM()
                LIMIT 1;
            """)

        else :

            cursor.execute("""
                SELECT id, category, author, quote, created_at
                FROM quotes
                WHERE category = ?
                ORDER BY RANDOM()
                LIMIT 1;
            """, (category,)
            )

        return cursor.fetchone()


def get_quotes_by_category (
        
        category : str = "Economics",
        conn : Optional[sqlite3.Connection] = None,

    ) -> List[Dict]:
    """
    
    """
    conn = get_connection if conn is None else conn

    with conn :

        conn.row_factory = _dict_factory
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, category, author, quote, created_at
            FROM quotes
            WHERE category = ?
            ORDER BY author;
        """, (category,))

        return cursor.fetchall()


def get_all_quotes (
        
        conn : Optional[sqlite3.Connection] = None,

    ) -> List[Dict] :
    """
    
    """
    conn = get_connection if conn is None else conn

    with conn :

        conn.row_factory = _dict_factory
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, category, author, quote, created_at
            FROM quotes
            ORDER BY category, author;
        """)

        return cursor.fetchall()


def _dict_factory (cursor, row) :

    factory = {
    
        column[0]: row[index]
        for index, column in enumerate(cursor.description)
    
    }

    return factory