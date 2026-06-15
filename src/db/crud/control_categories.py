from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.db.crud.common import build_update, execute, fetch_all, fetch_one, insert_and_get_id


def create_control_category(
    key: str,
    name: str,
    display_order: int = 0,
    is_active: bool = True,
    db_path: Optional[str | Path] = None,
) -> dict:
    category_id = insert_and_get_id(
        """
        INSERT INTO control_categories (key, name, display_order, is_active)
        VALUES (?, ?, ?, ?)
        """,
        (key, name, display_order, int(is_active)),
        db_path,
    )

    return get_control_category(category_id, db_path=db_path)


def get_control_category(category_id: int, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM control_categories WHERE id = ?", (category_id,), db_path)


def get_control_category_by_key(key: str, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM control_categories WHERE key = ?", (key,), db_path)


def list_control_categories(
    active_only: Optional[bool] = None,
    db_path: Optional[str | Path] = None,
) -> list[dict]:
    where_clause = ""
    params: list[int] = []

    if active_only is not None:
        where_clause = " WHERE is_active = ?"
        params.append(int(active_only))

    return fetch_all(
        f"SELECT * FROM control_categories{where_clause} ORDER BY display_order, name",
        params,
        db_path,
    )


def update_control_category(
    category_id: int,
    key: Optional[str] = None,
    name: Optional[str] = None,
    display_order: Optional[int] = None,
    is_active: Optional[bool] = None,
    db_path: Optional[str | Path] = None,
) -> Optional[dict]:
    set_clause, params = build_update(
        {
            "key": key,
            "name": name,
            "display_order": display_order,
            "is_active": None if is_active is None else int(is_active),
        }
    )
    execute(
        f"UPDATE control_categories SET {set_clause} WHERE id = ?",
        [*params, category_id],
        db_path,
    )

    return get_control_category(category_id, db_path=db_path)


def delete_control_category(
    category_id: int,
    hard_delete: bool = False,
    db_path: Optional[str | Path] = None,
) -> int:
    if hard_delete:
        return execute("DELETE FROM control_categories WHERE id = ?", (category_id,), db_path)

    return execute("UPDATE control_categories SET is_active = 0 WHERE id = ?", (category_id,), db_path)

