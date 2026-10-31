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


    if args.db == "demo.sqlite" and not os.path.exists(args.db):
        create_demo_database(args.db)

    if args.db != "demo.sqlite" and not os.path.exists(args.db):
        print(f"Database file '{args.db}' does not exist. Please provide a valid database path.")
        return

    

    schema = get_schema_description(args.db)
    try:
        generated_sql = generate_sql(args.question, schema)
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return

    safe = is_safe_query(generated_sql.query, args.allow_write)

    if not safe:
        log_query(args.question, generated_sql.query, allowed=False)

        print("The generated SQL query is not safe to execute. Write operations are not allowed.")
        print(f"Generated SQL: {generated_sql.query}")
        return 
    try:
        result = execute_query(args.db, generated_sql.query, args.allow_write)
        log_query(args.question, generated_sql.query, allowed=True, executed=True, error=None)
        print("Query executed successfully. Result:")
        if isinstance(result, list):
            for row in result:
                print(row)
        else:
            print(result)

    except Exception as e:
        log_query(args.question, generated_sql.query, allowed=True, executed=False, error=str(e))
        print(f"Error executing SQL: {e}")
        return


if __name__ == "__main__":
    main()
