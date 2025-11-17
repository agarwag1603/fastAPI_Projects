from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

gpt_llm=ChatOpenAI(model="gpt-4o-mini")

class StateArticle(TypedDict):
    topic: str
    paragraph: int
    article: str
    named_entity: str
    summary: str
    #topic_classifier: str

def generate_article(state:StateArticle)-> StateArticle:

    prompt = PromptTemplate(
    template=f"""Write a detailed article in {state['paragraph']} paragraph for the {state['topic']}
    Make sure you generate 
    -The childhood background of the person
    -Educational background 
    -Major contribution
    """,
    input_variables=[{state['paragraph']},{state['topic']}]
    )

    chain = prompt | gpt_llm | StrOutputParser()

    response=chain.invoke({"paragraph":state['paragraph'], "topic":state['topic']})

    return {"article":response}

def generate_named_entity(state:StateArticle)-> StateArticle:
    prompt = f"""You are an AI assistant that helps in finding the named entity recognition [NER] for the personality {state['topic']} from below article \n\n 
                                          {state['article']}
                                          """
    named_entity=gpt_llm.invoke(prompt)

    return {"named_entity": named_entity.content}


def generate_summary(state:StateArticle)-> StateArticle:
    prompt = f"""Please help in generating the bullet points for the article {state["article"]}."""

    summary=gpt_llm.invoke(prompt)

    return {"summary": summary.content}

graph=StateGraph(StateArticle)
graph.add_node("generate_article",generate_article)
graph.add_node("generate_named_entity",generate_named_entity)
graph.add_node("generate_summary",generate_summary)
graph.add_edge(START,"generate_article")
graph.add_edge("generate_article", "generate_named_entity")
graph.add_edge("generate_article", "generate_summary")

workflow=graph.compile()

