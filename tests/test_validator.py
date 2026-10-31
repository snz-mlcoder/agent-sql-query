from src.validator import is_safe_query

def test_validator_safe_query():
    # Test case 1: Safe query
    safe_query = "SELECT * FROM users WHERE id = 1"
    assert is_safe_query(safe_query, allow_write=False) == True


def test_validator_unsafe_query():
    # Test case 2: Unsafe query
    unsafe_query = "DELETE FROM users WHERE id = 1"
    assert is_safe_query(unsafe_query, allow_write=False) == False


def test_validator_unsafe_query_with_write_allowed():
    # Test case 3: Unsafe query with write allowed
    unsafe_query = "DELETE FROM users WHERE id = 1" 
    assert is_safe_query(unsafe_query, allow_write=True) == True

    print("All test cases passed for is_safe_query function.")

def test_validator_blocks_write_hidden_in_cte():
    sql = "WITH x AS (SELECT 1) DELETE FROM customers"
    assert is_safe_query(sql, allow_write=False) == False


def test_validator_blocks_replace_into():
    sql = "REPLACE INTO customers (name, email) VALUES ('a', 'b')"
    assert is_safe_query(sql, allow_write=False) == False


def test_validator_blocks_pragma():
    sql = "PRAGMA writable_schema=1"
    assert is_safe_query(sql, allow_write=False) == False

def test_validator_blocks_empty_string():
    sql = ""
    assert is_safe_query(sql, allow_write=False) == False