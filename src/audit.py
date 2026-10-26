import json
from datetime import datetime

def log_query(question: str, sql: str, allowed: bool, log_path: str = "audit_log.jsonl"):
    record = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "sql": sql,
        "allowed": allowed
    }

    with open(log_path, "a") as log_file:
        log_file.write(json.dumps(record) + "\n")