from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from schema.user_input import Article, LLMResponse
from llm.llm_caller import workflow

load_dotenv()

app = FastAPI()

@app.get("/")
def article_home_page():
    return {"message":"Welcome to Article generator"}

@app.post("/article", response_model=LLMResponse)
def generate_article(article: Article):

    try:
        result=workflow.invoke({"topic":article.topic, "paragraph":article.paragraph})
        return LLMResponse(topic=result["topic"],  paragraph=result["paragraph"], article=result["article"], named_entity = result["named_entity"],summary=result["summary"])
    except Exception as e:
        return HTTPException(status_code=500, detail= str(e))