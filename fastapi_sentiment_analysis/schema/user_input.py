from typing import Annotated, Literal
from pydantic import BaseModel, Field

class LLM(BaseModel):
    product_review:Annotated[str, Field(...,description="Product review from customer",example="My graphic card's performance is not up to the mark, but it doesn't cause much of an issue cause I have not been using it")]
    
class LLMResponse(BaseModel):
    product_review: str
    product_sentiment: str
    reply: str
    issue_type: str
    tone: str
    urgency: str
