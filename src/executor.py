
from pathlib import Path
from src.validator import is_safe_query
import sqlite3

def _connect(db_path: str, allow_write: bool)->sqlite3.Connection:
    if allow_write:
        return sqlite3.connect(db_path)
    else:
        uri = Path(db_path).resolve().as_uri() + "?mode=ro"
        return sqlite3.connect(uri, uri=True)
def execute_query(db_path: str, sql: str, allow_write: bool = False):
    if not is_safe_query(sql, allow_write):
        raise ValueError("Unsafe SQL query detected. Write operations are not allowed.")

    conn = _connect(db_path, allow_write)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        if cursor.description is not None:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.rowcount
    finally:
        cursor.close()
        conn.close()

    return result