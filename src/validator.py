def is_safe_query(sql: str, allow_write: bool) -> bool:
    first_word = sql.strip().split()[0].upper()
    write_operations = {"INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"}
    if not allow_write and first_word in write_operations:
        return False
    return True