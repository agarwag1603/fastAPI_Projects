from typing import Annotated
from pydantic import BaseModel, Field
from typing import Literal

class RAG(BaseModel):
    gpt_model: Annotated[Literal["gpt-4o-mini","gpt-5-mini","gpt-5-nano"], Field(...,description="gpt llm model for the use",example="gpt-4o-mini")]
    query:Annotated[str, Field(...,description="number of documents to be searched",example="What is the minimum deposit of car?")]
