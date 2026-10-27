import argparse
import os
from src.database import get_schema_description, create_demo_database
from src.audit import log_query
from src.generator import generate_sql
from src.executor import execute_query
from src.validator import is_safe_query

def main():
    parser = argparse.ArgumentParser(description="SQL Query Agent: Generate and execute SQL queries based on natural language questions.")
    parser.add_argument("--db", type=str, default="demo.sqlite", help="Path to the database file.")
    parser.add_argument("--question", type=str, required=True, help="The question to generate SQL for.")
    parser.add_argument("--allow-write", action="store_true", help="Allow write operations in the generated SQL query.")
    args = parser.parse_args()

    if args.db == "demo.sqlite3" and not os.path.exists(args.db):
        create_demo_database(args.db)

    schema = get_schema_description(args.db)
    generated_sql = generate_sql(args.question, schema)

    safe = is_safe_query(generated_sql.query, args.allow_write)
    log_query(args.question, generated_sql.query,allowed = safe)

    if not safe:
        print("The generated SQL query is not safe to execute. Write operations are not allowed.")
        print(f"Generated SQL: {generated_sql.query}")
        return  

    result = execute_query(args.db, generated_sql.query, args.allow_write)
    print("Query Result:")
    if isinstance(result, list):
        for row in result:
            print(row)  

if __name__ == "__main__":
    main()
