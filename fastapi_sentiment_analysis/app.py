from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from schema.user_input import LLM, LLMResponse
from llm.llm_caller import workflow
from fastapi.responses import Response

load_dotenv()

app = FastAPI()

@app.get("/")
def sentimentanalysis_home_page():
    return {"message":"Sentiment analysis generator"}

@app.post("/sentimentanalysis", response_model=LLMResponse)
def generate_sentiment(llm: LLM):
    try:
        result=workflow.invoke({"product_review":llm.product_review})
        return LLMResponse(product_review=result["product_review"],  product_sentiment=result["product_sentiment"], reply=result["reply"], 
                           issue_type = result["issue_type"],tone=result["tone"],urgency=result["urgency"])
    except Exception as e:
        return HTTPException(status_code=500, detail= str(e))
    
@app.get('/graph')
def graph_image():
    img_bytes = workflow.get_graph().draw_mermaid_png()
    return Response(content=img_bytes, media_type="image/png")
