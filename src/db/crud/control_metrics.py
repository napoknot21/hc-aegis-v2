from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from src.db.crud.common import build_update, encode_json, execute, fetch_all, fetch_one, insert_and_get_id


def create_control_metric(
    run_id: int,
    metric_name: str,
    metric_value: Optional[float] = None,
    threshold_value: Optional[float] = None,
    threshold_operator: Optional[str] = None,
    unit: Optional[str] = None,
    status: str = "pending",
    details_json: Optional[str | dict[str, Any] | list[Any]] = None,
    db_path: Optional[str | Path] = None,
) -> dict:
    metric_id = insert_and_get_id(
        """
        INSERT INTO control_metrics (
            run_id, metric_name, metric_value, threshold_value,
            threshold_operator, unit, status, details_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            metric_name,
            metric_value,
            threshold_value,
            threshold_operator,
            unit,
            status,
            encode_json(details_json),
        ),
        db_path,
    )

    return get_control_metric(metric_id, db_path=db_path)


def get_control_metric(metric_id: int, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM control_metrics WHERE id = ?", (metric_id,), db_path)


def list_control_metrics(
    run_id: Optional[int] = None,
    status: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list[Any] = []

    if run_id is not None:
        clauses.append("run_id = ?")
        params.append(run_id)

    if status is not None:
        clauses.append("status = ?")
        params.append(status)

    where_clause = "" if not clauses else " WHERE " + " AND ".join(clauses)

    return fetch_all(
        f"SELECT * FROM control_metrics{where_clause} ORDER BY id",
        params,
        db_path,
    )


def update_control_metric(
    metric_id: int,
    metric_name: Optional[str] = None,
    metric_value: Optional[float] = None,
    threshold_value: Optional[float] = None,
    threshold_operator: Optional[str] = None,
    unit: Optional[str] = None,
    status: Optional[str] = None,
    details_json: Optional[str | dict[str, Any] | list[Any]] = None,
    db_path: Optional[str | Path] = None,
) -> Optional[dict]:
    set_clause, params = build_update(
        {
            "metric_name": metric_name,
            "metric_value": metric_value,
            "threshold_value": threshold_value,
            "threshold_operator": threshold_operator,
            "unit": unit,
            "status": status,
            "details_json": encode_json(details_json),
        }
    )
    execute(
        f"UPDATE control_metrics SET {set_clause} WHERE id = ?",
        [*params, metric_id],
        db_path,
    )

    return get_control_metric(metric_id, db_path=db_path)


def delete_control_metric(metric_id: int, db_path: Optional[str | Path] = None) -> int:
    return execute("DELETE FROM control_metrics WHERE id = ?", (metric_id,), db_path)

