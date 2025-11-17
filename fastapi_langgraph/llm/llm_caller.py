from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class StateLG(TypedDict):
    query: str
    gpt_model: str
    content_type: str
    output: str
    
def chatbot(state: StateLG):
    prompt= f"You are an AI assistant who can help in generating {state['content_type']} about: \n {state['query']}"
    gpt_llm = ChatOpenAI(model=state['gpt_model'])
    response=gpt_llm.invoke(prompt)
    return {"output":response.content}

graph=StateGraph(StateLG)
graph.add_node("chatbot",chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge( "chatbot",END)

workflow=graph.compile()