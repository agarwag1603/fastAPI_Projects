from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from schema.user_input import LLM, LLMResponse
from llm.llm_caller import workflow

load_dotenv()

app = FastAPI()

@app.post('/langgraph', response_model=LLMResponse)
def langgraph_caller(langgraph:LLM):

    try:
        result=workflow.invoke({"query":langgraph.query, "gpt_model":langgraph.gpt_model, "content_type":langgraph.content_type})
        return LLMResponse(query=result["query"],  gpt_model=result["gpt_model"], content_type= result["content_type"], output = result["output"])
    except Exception as e:
        return HTTPException(status_code=500, detail= str(e))