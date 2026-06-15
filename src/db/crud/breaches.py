from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.db.crud.common import build_filters, build_update, execute, fetch_all, fetch_one, insert_and_get_id


def create_breach(
    run_id: int,
    metric_id: Optional[int] = None,
    validation_status: str = "pending",
    validator: Optional[str] = None,
    validation_comment: Optional[str] = None,
    validated_at: Optional[str] = None,
    remediation_due_date: Optional[str] = None,
    remediation_comment: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> dict:
    breach_id = insert_and_get_id(
        """
        INSERT INTO breaches (
            run_id, metric_id, validation_status, validator, validation_comment,
            validated_at, remediation_due_date, remediation_comment
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            metric_id,
            validation_status,
            validator,
            validation_comment,
            validated_at,
            remediation_due_date,
            remediation_comment,
        ),
        db_path,
    )

    return get_breach(breach_id, db_path=db_path)


def get_breach(breach_id: int, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM breaches WHERE id = ?", (breach_id,), db_path)


def list_breaches(
    run_id: Optional[int] = None,
    metric_id: Optional[int] = None,
    validation_status: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> list[dict]:
    where_clause, params = build_filters(
        {
            "run_id": run_id,
            "metric_id": metric_id,
            "validation_status": validation_status,
        }
    )

    return fetch_all(
        f"SELECT * FROM breaches{where_clause} ORDER BY created_at DESC, id DESC",
        params,
        db_path,
    )


def update_breach(
    breach_id: int,
    metric_id: Optional[int] = None,
    validation_status: Optional[str] = None,
    validator: Optional[str] = None,
    validation_comment: Optional[str] = None,
    validated_at: Optional[str] = None,
    remediation_due_date: Optional[str] = None,
    remediation_comment: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> Optional[dict]:
    set_clause, params = build_update(
        {
            "metric_id": metric_id,
            "validation_status": validation_status,
            "validator": validator,
            "validation_comment": validation_comment,
            "validated_at": validated_at,
            "remediation_due_date": remediation_due_date,
            "remediation_comment": remediation_comment,
        }
    )

    execute(
        f"UPDATE breaches SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        [*params, breach_id],
        db_path,
    )

    return get_breach(breach_id, db_path=db_path)


def delete_breach(breach_id: int, db_path: Optional[str | Path] = None) -> int:
    return execute("DELETE FROM breaches WHERE id = ?", (breach_id,), db_path)
