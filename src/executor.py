

from src.validator import is_safe_query
import sqlite3


def execute_query(db_path: str, sql: str, allow_write: bool = False):
    if not is_safe_query(sql, allow_write):
        raise ValueError("Unsafe SQL query detected. Write operations are not allowed.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        if sql.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.rowcount
    finally:
        cursor.close()
        conn.close()

    return result