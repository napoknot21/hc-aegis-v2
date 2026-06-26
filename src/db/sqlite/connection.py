import os
import sqlite3

from typing import Optional, List

from src.config.paths import AEGIS_DATABASE_ABS_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MIGRATIONS_DIR = os.path.join(BASE_DIR, "migrations")
CRUD_DIR = os.path.join(BASE_DIR, "crud")
SEEDS_DIR = os.path.join(BASE_DIR, "seeds")


def database_exists(db_path : Optional[str] = None) -> bool :
    """
    Check whether the SQLite database file already exists.
    """
    db_path = AEGIS_DATABASE_ABS_PATH if db_path is None else db_path
    db_exists = os.path.exists(db_path)

    return db_exists


def get_connection (db_path : Optional[str] = None) -> sqlite3.Connection:
    """
    Return a SQLite connection.

    sqlite3.connect(...) automatically creates the database file
    if it does not already exist.

    Foreign keys are disabled by default in SQLite, so we enable them
    explicitly for each connection.
    """
    db_path = AEGIS_DATABASE_ABS_PATH if db_path is None else db_path
    db_dir = os.path.dirname(db_path)

    if db_dir :
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


def execute_sql_file (
        
        sql_file_path : str,
        conn : Optional[sqlite3.Connection] = None,
    
    ) -> None :
    """
    Execute a .sql file using the provided SQLite connection.
    """
    conn = get_connection() if conn is None else conn

    if not os.path.exists(sql_file_path) :
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    with open(sql_file_path, "r", encoding="utf-8") as file :
        sql_script = file.read()

    if sql_script.strip() :
        conn.executescript(sql_script)

    return None


def get_sql_files (directory : Optional[str] = None) -> List[str]:
    """
    Return all .sql files from a directory, sorted lexicographically.

    Example:
    001_create_quotes.sql
    002_create_users.sql
    003_create_permissions.sql
    """
    directory = MIGRATIONS_DIR if directory is None else directory

    if not os.path.exists(directory) :
        return []

    sql_files = sorted(os.path.join(directory, filename)
    
        for filename in os.listdir(directory) if filename.endswith(".sql")
    
    )
    
    return sql_files


def run_migrations (
    
        conn : Optional[sqlite3.Connection] = None,

        migration_files : Optional[List[str]] = None,
        directory : Optional[str] = None

    ) -> None:
    """
    Run all SQL migration files in order.
    """
    conn = get_connection() if conn is None else conn
    directory = MIGRATIONS_DIR if directory is None else directory

    migration_files = get_sql_files(directory) if migration_files is None else migration_files

    for migration_file in migration_files :
        execute_sql_file(migration_file, conn)

    return None


def run_seeds (
        
        conn : Optional[sqlite3.Connection] = None,

        seed_files : Optional[List[str]] = None,
        directory : Optional[str] = None,

    
    ) -> None:
    """
    Run all SQL seed files in order.
    """
    conn = get_connection() if conn is None else conn
    directory = SEEDS_DIR if directory is None else directory

    seed_files = get_sql_files(directory) if seed_files is None else seed_files
    
    for seed_file in seed_files :
        execute_sql_file(seed_file, conn)

    return None


def init_database (
        
        db_path : Optional[str] = None,
        seed : bool = True
    
    ) -> None:
    """
    Initialize the SQLite database.

    Behavior:
    - create the database file if needed
    - run idempotent migrations
    - run idempotent seeds if seed=True
    """
    db_path = AEGIS_DATABASE_ABS_PATH if db_path is None else db_path

    with get_connection(db_path) as conn :

        run_migrations(conn)

        if seed:
            run_seeds(conn)

        conn.commit()


def reset_database (
        
        db_path : Optional[str] = None,
        seed : bool = True
    
    ) -> None :
    """
    Delete and recreate the database.

    Useful in local development only.
    Be careful: this removes all existing data.
    """
    db_path = AEGIS_DATABASE_ABS_PATH if db_path is None else db_path

    if os.path.exists(db_path) :
        os.remove(db_path)

    with get_connection(db_path) as conn :

        run_migrations(conn)

        if seed :
            run_seeds(conn)

        conn.commit()


def execute_query (
        
        query : str,
        params : Optional[tuple] = None,
        fetchone : bool = False,
        fetchall : bool = False,
    
    ):
    """
    Generic helper for simple CRUD operations.

    For more complex cases, prefer writing explicit CRUD functions.
    """
    params = params or ()

    with get_connection() as conn :

        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        if fetchone :
            return cursor.fetchone()

        if fetchall :
            return cursor.fetchall()

        return None
    
