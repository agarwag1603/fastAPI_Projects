from typing import Annotated, Literal
from pydantic import BaseModel, Field

class LLM(BaseModel):
    query:Annotated[str, Field(...,description="User query",example="what is black hole?")]
    gpt_model: Annotated[Literal["gpt-4o-mini", "gpt-5-nano", "gpt-5-mini"], Field(..., description="OpenAI model to use", example="gpt-4o-mini")]
    content_type: Annotated[Literal["Poem", "Article", "Blog"], Field(..., description="Content type used", example="Poem")]

class LLMResponse(BaseModel):
    query: str
    gpt_model : str
    content_type: str
    output: str
