from src.audit import log_query
import json

def test_audit_log_query(tmp_path):
    # Create a temporary log file path
    log_file_path = tmp_path / "audit_log.jsonl"

    # Sample data for logging
    question = "What is the total number of users?"
    sql = "SELECT COUNT(*) FROM users"
    allowed = True

    # Call the log_query function
    log_query(question, sql, allowed, log_path = str(log_file_path))

    # Read the log file and verify its contents
    with open(log_file_path, "r") as log_file:
        lines = log_file.readlines()
        assert len(lines) == 1  # Ensure one record is logged

        # Parse the JSON record
        record = json.loads(lines[0])
        assert record["question"] == question
        assert record["sql"] == sql
        assert record["allowed"] == allowed
        assert "timestamp" in record  # Ensure timestamp is present

def test_log_query_records_execution_outcome(tmp_path):
    log_file_path = tmp_path / "audit_log.jsonl"

    # Log a query that is not allowed
    question = "how many users are there?"
    sql = "SELECT COUNT(*) FROM missing_table"
    allowed = True
    
    # Call the log_query function
    log_query(question, sql, allowed, executed=False, error="no such table: missing_table", log_path = str(log_file_path))
    # Read the log file and verify its contents
    with open(log_file_path, "r") as log_file:  
        lines = log_file.readlines()
        record = json.loads(lines[0])
        assert record["executed"] == False
        assert record["error"] == "no such table: missing_table"
# executed=True و error=None
def test_log_query_records_successful_execution(tmp_path):
    log_file_path = tmp_path / "audit_log.jsonl"

    # Log a query that is allowed and executed successfully
    question = "how many users are there?"
    sql = "SELECT COUNT(*) FROM users"
    allowed = True

    # Call the log_query function
    log_query(question, sql, allowed, executed=True, error=None, log_path = str(log_file_path))

    # Read the log file and verify its contents
    with open(log_file_path, "r") as log_file:
        lines = log_file.readlines()
        record = json.loads(lines[0])
        assert record["executed"] == True
        assert record["error"] == None