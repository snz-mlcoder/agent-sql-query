from pydantic import BaseModel


class GeneratedQuery(BaseModel):
    query: str
    description: str
    change_data: bool
