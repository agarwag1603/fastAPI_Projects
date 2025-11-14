from fastapi import FastAPI, Path, HTTPException
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Annotated, Literal

load_dotenv()

gpt_llm = ChatOpenAI(model="gpt-4o-mini")

app = FastAPI()

class LLM(BaseModel):
    topic: Annotated[str,(Field(...,description="Topic for the LLM"))]
    type: Annotated[Literal["Essay","Article","Poem"],(Field(...,description="Type of the generative text, should only be Essay, Article, Poem"))]


@app.post('/llm/{topic}')
def call_llm(topic: str = Path(...,description="provide your query", example = "Topic for the llm call")):

    if topic == None:
        raise HTTPException(status_code=404, detail="topic not found")
    
    prompt = PromptTemplate(
    template="Write a 2 paragraph article for {topic}",
    input_variables=["topic"]
    )

    chain = prompt | gpt_llm | StrOutputParser()

    result=chain.invoke({"topic":topic})

    return result

@app.post('/chatme')
def essay_generator(chatme:LLM):

    if chatme.topic == None:
        raise HTTPException(status_code=404, detail="topic not found")

    if chatme.type not in ["Essay","Article","Poem"]:
        raise HTTPException(status_code=404, detail="Type not right")

    prompt = PromptTemplate(
    template=(
        "Write a clear and well-structured {type} about '{topic}'.\n"
        "Follow these rules:\n"
        "- Length: 3–5 paragraphs\n"
        "- Tone: Informative and engaging\n"
        "- Do not include bullet points\n"
        "- Start with a strong introduction\n"
        "- End with a conclusion"
    ),
    input_variables=["topic", "type"]
    )

    chain = prompt | gpt_llm | StrOutputParser()

    result=chain.invoke({"topic":chatme.topic, "type":chatme.type})

    return result
    
