

from src.schema import GeneratedQuery
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def generate_sql(question: str ,schema_description: str):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt =f"""please generate a SQL query based on the following question and schema description.only generate the SQL query without any explanation or additional text.
    use only table and column names from the schema description provided.
    Question: {question}
    Schema: {schema_description}"""

    structured_llm =llm.with_structured_output(GeneratedQuery)
    result = structured_llm.invoke(prompt)
    return result
