from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from schema.user_input import RAG
from llm.llm_caller import llm_caller_func

load_dotenv()

app = FastAPI()

##This route will only run the embedding once we load the fastapi.
@app.post('/rag')
def create_rag_chatter(ragchatter: RAG):

    try:
        response=llm_caller_func(ragchatter.gpt_model, ragchatter.query)

        return JSONResponse(status_code=200, content={"answer": response})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))





    


