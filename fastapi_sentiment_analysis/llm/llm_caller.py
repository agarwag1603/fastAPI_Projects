## Conditional workflow which detects the customer review for sentiment analysis and responds based on positive or negative feedback
from typing import TypedDict, Literal
from langgraph.graph import START,END,StateGraph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
gpt_llm= ChatOpenAI(model="gpt-4o-mini")
## Pydantic to find the sentiment as positive or negative

class Review(BaseModel):
    sentiment: Literal["Positive","Negative"] = Field(description="Review of the product in Positive and Negative")
## Pydantic to find the issue type, tone, urgency

class IssueClassifier(BaseModel):
    issue_type: str = Field(description="Issue type is the issue description")
    tone: Literal["Hard","Mild","Soft"] =  Field(description="Tone is the tone of the review")
    urgency: Literal["High","Medium","Low"] =  Field(description="Urgency categorization")

## For both pydantic class Review and IssueClassifier, defining the structuredoutput
sentiment_model=gpt_llm.with_structured_output(Review)
Issue_classifier=gpt_llm.with_structured_output(IssueClassifier)

class Product(TypedDict):
    product_review: str
    product_sentiment: str
    reply: str
    issue_type: str
    tone: str
    urgency: str

def find_sentiment(state:Product)-> Product:
    product_review=state['product_review']
    prompt=f"Help me find the sentiment of the review given by the customer: \n {product_review}"
    sentiment=sentiment_model.invoke(prompt)
    return {'product_sentiment':sentiment.sentiment}

def positive_response(state:Product)-> Product:
    product_review=state['product_review']
    product_sentiment=state['product_sentiment']
    prompt=f"Help me reply to the customer based on the product review: \n {product_review} and the sentiment of it \n {product_sentiment}"
    positive_reply=gpt_llm.invoke(prompt)
    return {'reply':positive_reply.content}

def negative_response(state:Product)-> Product:
    product_review=state['product_review']
    product_sentiment=state['product_sentiment']
    tone=state['tone']
    issue_type=state['issue_type']
    urgency=state['urgency']

    prompt=f"""Help me reply the customer in a very articulated manner based on the negative product review. Carefully device the apology: 
    \n {product_review} and the sentiment of it \n {product_sentiment}. Do consider these factors for a response. \n 
    customer tone: \n {tone} \n 
    Issue type: \n {issue_type} \n
    urgency: \n {urgency} \n"""
    
    negative_reply=gpt_llm.invoke(prompt)
    return {'reply':negative_reply.content}

def run_dagnosis(state:Product)-> Product:
    product_review=state['product_review']
    prompt=f"With the help of product review try getting classifying the issue with Issue_Type, Tone, Urgency of the issue. Product review as below: \n {product_review}"
    output=Issue_classifier.invoke(prompt)
    
    return {'issue_type':output.issue_type,'tone':output.tone,'urgency':output.urgency}
    
## Conditional check for positive or negative review - if postive, reply the customer. And if negative run diagnosis
def check_sentiment(state:Product)->  Literal["positive_response","run_dagnosis"]:
    if state["product_sentiment"] == "Positive":
        return "positive_response"
    else:
        return "run_dagnosis"
graph=StateGraph(Product)
graph.add_node("find_sentiment",find_sentiment)
graph.add_node("positive_response",positive_response)
graph.add_node("negative_response",negative_response)
graph.add_node("run_dagnosis",run_dagnosis)

graph.add_edge(START,"find_sentiment")
graph.add_conditional_edges("find_sentiment",check_sentiment)
graph.add_edge("positive_response", END)
graph.add_edge("run_dagnosis", "negative_response")
graph.add_edge("negative_response", END)
workflow=graph.compile()