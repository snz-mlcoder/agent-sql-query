import re

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
        write_words = ["INSERT", "UPDATE", "DELETE", "REPLACE", "PRAGMA"]
        if set(re.findall(r"\w+", sql.upper())) & set(write_words):
            return False
    return True
