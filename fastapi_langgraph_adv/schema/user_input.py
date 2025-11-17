from typing import Annotated, Literal
from pydantic import BaseModel, Field

class Article(BaseModel):
    topic:Annotated[str, Field(...,description="User query",example="Virat Kohli")]
    paragraph:Annotated[int, Field(...,description="Number of paragraphs",example=2)]
    
class LLMResponse(BaseModel):
    topic: str
    paragraph: int
    article: str
    named_entity: str
    summary: str
