from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.db.crud.common import build_filters, build_update, execute, fetch_all, fetch_one, insert_and_get_id


def create_fund(
    code: str,
    name: str,
    business_line: str,
    is_active: bool = True,
    db_path: Optional[str | Path] = None,
) -> dict:
    fund_id = insert_and_get_id(
        """
        INSERT INTO funds (code, name, business_line, is_active)
        VALUES (?, ?, ?, ?)
        """,
        (code, name, business_line, int(is_active)),
        db_path,
    )

    return get_fund(fund_id, db_path=db_path)


def get_fund(fund_id: int, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM funds WHERE id = ?", (fund_id,), db_path)


def get_fund_by_code(code: str, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM funds WHERE code = ?", (code,), db_path)


def list_funds(
    business_line: Optional[str] = None,
    active_only: Optional[bool] = None,
    db_path: Optional[str | Path] = None,
) -> list[dict]:
    filters = {"business_line": business_line}

    if active_only is not None:
        filters["is_active"] = int(active_only)

    where_clause, params = build_filters(filters)

    return fetch_all(
        f"SELECT * FROM funds{where_clause} ORDER BY code",
        params,
        db_path,
    )


def update_fund(
    fund_id: int,
    code: Optional[str] = None,
    name: Optional[str] = None,
    business_line: Optional[str] = None,
    is_active: Optional[bool] = None,
    db_path: Optional[str | Path] = None,
) -> Optional[dict]:
    set_clause, params = build_update(
        {
            "code": code,
            "name": name,
            "business_line": business_line,
            "is_active": None if is_active is None else int(is_active),
        }
    )

    execute(f"UPDATE funds SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", [*params, fund_id], db_path)

    return get_fund(fund_id, db_path=db_path)


def delete_fund(fund_id: int, hard_delete: bool = False, db_path: Optional[str | Path] = None) -> int:
    if hard_delete:
        return execute("DELETE FROM funds WHERE id = ?", (fund_id,), db_path)

    return execute(
        "UPDATE funds SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (fund_id,),
        db_path,
    )
