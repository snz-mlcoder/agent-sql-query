def is_safe_query(sql: str, allow_write: bool) -> bool:

    if sql.strip() == "":
        return False
    if allow_write :
        return True
    
    first_word = sql.strip().split()[0].upper()
    allowed_starts = {"SELECT", "WITH"}    
    if first_word not in allowed_starts:
        return False
    else:
        return True

