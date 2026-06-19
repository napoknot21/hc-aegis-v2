from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.db.sqlite.connection import DATABASE_PATH, apply_migrations


def create_database(db_path: Optional[str | Path] = None) -> list[str]:
    """
    Create or update the SQLite database from migration files.
    """
    return apply_migrations(db_path=db_path)


def main() -> None:
    applied = create_database()
    target = DATABASE_PATH

    if applied:
        print(f"Database ready at {target}. Applied migrations: {', '.join(applied)}")
    else:
        print(f"Database ready at {target}. No pending migrations.")


if __name__ == "__main__":
    main()
