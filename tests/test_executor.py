import pytest
import sqlite3
from src.database import create_demo_database
from src.executor import execute_query


def test_execute_with_select_returns_rows(tmp_path):
    db_path = str(tmp_path / "test.sqlite")
    create_demo_database(db_path)

    sql = "WITH c AS (SELECT * FROM customers) SELECT name FROM c"
    result = execute_query(db_path, sql)

    assert result == [("John Doe",), ("Jane Smith",)]

def test_execute_simple_select(tmp_path):
    db_path = str(tmp_path / "test.sqlite")
    create_demo_database(db_path)

    sql = "SELECT name FROM customers"
    result = execute_query(db_path, sql)

    assert result == [("John Doe",), ("Jane Smith",)]

#UPDATE customers SET country = 'Italy' WHERE id = 1
def test_execute_with_update(tmp_path):
    db_path = str(tmp_path / "test.sqlite")
    create_demo_database(db_path)

    sql = "UPDATE customers SET country = 'Italy' WHERE id = 1"
    result = execute_query(db_path, sql, allow_write=True)

    assert result == 1  # One row should be updated

    # Verify the update
    verify_sql = "SELECT country FROM customers WHERE id = 1"
    verify_result = execute_query(db_path, verify_sql)
    assert verify_result == [("Italy",)]

def test_readonly_connection_blocks_write_even_if_validator_bypassed(tmp_path,monkeypatch):
    db_path = str(tmp_path / "test.sqlite")
    create_demo_database(db_path)

    monkeypatch.setattr("src.executor.is_safe_query", lambda sql, allow_write: True)  # Bypass the validator
    with pytest.raises(sqlite3.OperationalError):
        execute_query(db_path, "DELETE FROM customers", allow_write=False)  # This should raise an error due to the read-only connection

