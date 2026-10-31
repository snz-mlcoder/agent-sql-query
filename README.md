# Project Overview
A CLI agent that generates SQL queries from natural language questions and executes them after verifying their safety.


# Features
- Creates a sample database if one doesn't exist
- Generates SQL from natural language questions
- Executes the generated SQL
- Validates query safety before execution (keyword whitelist + write-keyword scan)
- Opens the database read-only unless `--allow-write` is set
- Logs every query to an audit file, including whether it was executed and any error

# Installation
uv sync

# Usage (--db, --question ,--allow-write)
- Ask a question (read-only by default)
uv run python main.py --question "How many customers are from USA?"

- Allow write operations
uv run python main.py --question "Update customer 1's country to Canada" --allow-write

- Use your own database
uv run python main.py --db mydata.sqlite --question "..."

# Technologies
- Python
- LangChain
- LangChain-OpenAI
- Pydantic
- pytest
- python-dotenv


# Project Structure
agent-sql-query/
├── main.py
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── generator.py
│   ├── validator.py
│   ├── executor.py
│   ├── audit.py
│   └── schema.py
├── tests/
│   ├── test_validator.py
│   ├── test_executor.py
│   ├── test_audit.py
│   └── test_generator.py

├── pyproject.toml
├── .env.example
└── README.md
# Safety Layers
Generated SQL goes through three independent layers before it can change data:

1. **Validator** (`src/validator.py`): in read-only mode the statement must start with
   `SELECT` or `WITH`, and none of `INSERT`, `UPDATE`, `DELETE`, `REPLACE`, `PRAGMA` may appear anywhere in it. This catches writes hidden inside `WITH ... DELETE`.
   Statements starting with anything else (e.g. `CREATE`, `DROP`) are rejected by the whitelist.
2. **Read-only connection** (`src/executor.py`): without `--allow-write`, SQLite is opened
   with `mode=ro`, so even a query that bypasses the validator cannot modify the database.
3. **SQLite itself**: `execute()` runs one statement at a time, so
   `SELECT ...; DROP TABLE ...` is rejected by the driver.


# Known Limitations
- The write-keyword scan is conservative: a harmless query containing a write keyword as text (e.g. `WHERE name = 'delete'`) is rejected.
- Queries starting with a parenthesis, e.g. `(SELECT ...)`, are rejected.
- With `--allow-write`, no restriction applies to the generated SQL.
- Text comparison in SQLite is case-sensitive, so a model-generated `country = 'Usa'`
  will not match `'USA'`. Result quality depends on the model.
- Older entries in `audit_log.jsonl` lack the `executed` and `error` fields.

# Tests
uv run pytest

# Future Improvements
- Use a proper SQL parser (e.g. `sqlparse`) instead of keyword scanning, to avoid false positives on string literals
- Separate audit logging from the execution `try` block, so a logging failure cannot be recorded as an SQL error
- Support other database engines (PostgreSQL, MySQL), not just SQLite
- Add an interactive chat mode, like the original sample agent
- Allow exporting query results to CSV/JSON
