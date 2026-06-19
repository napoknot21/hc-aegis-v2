from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.db.sqlite.crud.common import build_filters, build_update, execute, fetch_all, fetch_one, insert_and_get_id


def create_control_run(
    control_date: str,
    fund_id: int,
    category_id: int,
    status: str = "pending",
    severity: Optional[str] = None,
    source: Optional[str] = None,
    notes: Optional[str] = None,
    created_by: Optional[str] = None,
    updated_by: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> dict:
    run_id = insert_and_get_id(
        """
        INSERT INTO control_runs (
            control_date, fund_id, category_id, status, severity, source,
            notes, created_by, updated_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (control_date, fund_id, category_id, status, severity, source, notes, created_by, updated_by),
        db_path,
    )

    return get_control_run(run_id, db_path=db_path)


def get_control_run(run_id: int, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM control_runs WHERE id = ?", (run_id,), db_path)


def list_control_runs(
    control_date: Optional[str] = None,
    fund_id: Optional[int] = None,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> list[dict]:
    where_clause, params = build_filters(
        {
            "control_date": control_date,
            "fund_id": fund_id,
            "category_id": category_id,
            "status": status,
        }
    )

    return fetch_all(
        f"SELECT * FROM control_runs{where_clause} ORDER BY control_date DESC, id DESC",
        params,
        db_path,
    )


def update_control_run(
    run_id: int,
    control_date: Optional[str] = None,
    fund_id: Optional[int] = None,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    source: Optional[str] = None,
    notes: Optional[str] = None,
    updated_by: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> Optional[dict]:
    set_clause, params = build_update(
        {
            "control_date": control_date,
            "fund_id": fund_id,
            "category_id": category_id,
            "status": status,
            "severity": severity,
            "source": source,
            "notes": notes,
            "updated_by": updated_by,
        }
    )

    execute(
        f"UPDATE control_runs SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        [*params, run_id],
        db_path,
    )

    return get_control_run(run_id, db_path=db_path)


def delete_control_run(run_id: int, db_path: Optional[str | Path] = None) -> int:
    return execute("DELETE FROM control_runs WHERE id = ?", (run_id,), db_path)
