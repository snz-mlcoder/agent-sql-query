# Project Overview
A CLI agent that generates SQL queries from natural language questions and executes them after verifying their safety.


# Features
- Creates a sample database if one doesn't exist
- Generates SQL from natural language questions
- Executes the generated SQL
- Validates query safety before execution
- Logs every query to an audit file

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
│   └── test_generator.py
├── pyproject.toml
├── .env.example
└── README.md

# Known Limitations
`is_safe_query` only checks the first word of the generated SQL statement. If the model
produces multiple statements separated by a semicolon (e.g. `SELECT * FROM users; DROP TABLE users;`),
the second, destructive statement will not be detected, since only the first word is inspected.

# Tests
uv run pytest

# Future Improvements
- Use a proper SQL parser (e.g. `sqlparse`) instead of a first-word check, to detect
  multi-statement injection attempts
- Support other database engines (PostgreSQL, MySQL), not just SQLite
- Add an interactive chat mode, like the original sample agent
- Allow exporting query results to CSV/JSON