from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from db.sqlite.crud.common import encode_json, execute, fetch_all, fetch_one, insert_and_get_id


def create_audit_event(
    entity_type: str,
    entity_id: int,
    action: str,
    before_json: Optional[str | dict[str, Any] | list[Any]] = None,
    after_json: Optional[str | dict[str, Any] | list[Any]] = None,
    user_email: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> dict:
    event_id = insert_and_get_id(
        """
        INSERT INTO audit_events (
            entity_type, entity_id, action, before_json, after_json, user_email
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            entity_type,
            entity_id,
            action,
            encode_json(before_json),
            encode_json(after_json),
            user_email,
        ),
        db_path,
    )

    return get_audit_event(event_id, db_path=db_path)


def get_audit_event(event_id: int, db_path: Optional[str | Path] = None) -> Optional[dict]:
    return fetch_one("SELECT * FROM audit_events WHERE id = ?", (event_id,), db_path)


def list_audit_events(
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    action: Optional[str] = None,
    db_path: Optional[str | Path] = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list[Any] = []

    if entity_type is not None:
        clauses.append("entity_type = ?")
        params.append(entity_type)

    if entity_id is not None:
        clauses.append("entity_id = ?")
        params.append(entity_id)

    if action is not None:
        clauses.append("action = ?")
        params.append(action)

    where_clause = "" if not clauses else " WHERE " + " AND ".join(clauses)

    return fetch_all(
        f"SELECT * FROM audit_events{where_clause} ORDER BY created_at DESC, id DESC",
        params,
        db_path,
    )


def delete_audit_event(event_id: int, db_path: Optional[str | Path] = None) -> int:
    return execute("DELETE FROM audit_events WHERE id = ?", (event_id,), db_path)

