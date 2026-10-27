from src.generator import generate_sql
from src.schema import GeneratedQuery
from unittest.mock import patch, MagicMock

def test_generate_sql_returns_structured_query():
    fake_query = GeneratedQuery(query="SELECT * FROM users WHERE id = 1", 
                                description="Get user by ID",
                                change_data=False
                                )

    with patch('src.generator.ChatOpenAI') as mock_chat_openai:
        mock_llm = MagicMock()
        mock_llm.with_structured_output.return_value.invoke.return_value = fake_query
        mock_chat_openai.return_value = mock_llm

        result = generate_sql("Get user by ID", "Table: users (id, name, email)")

    assert result == fake_query