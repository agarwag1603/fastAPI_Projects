from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Literal
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from langsmith import traceable

load_dotenv()

VECTOR_DB_PATH = "./chroma_db"

##For tracing the vector DB initilization on langsmith
@traceable(name="initialize_vector_db")
def initialize_vectordb():
# Check if vector DB already exists
    if Path(VECTOR_DB_PATH).exists():
    # Load existing vector DB (fast!)
        openai_embedding = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
        chromavectordb = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=openai_embedding)
        chroma_retriever = chromavectordb.as_retriever(search_kwargs={"k": 3})
    else:
        pdf_path = Path(__file__).parent / "RentalConditions.pdf"
        pypdf_loader=PyPDFLoader(str(pdf_path))
        rentalcondition_loader=pypdf_loader.load()
        pdf_document_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
        final_pdf_document=pdf_document_splitter.split_documents(rentalcondition_loader)
        openai_embedding = OpenAIEmbeddings(model="text-embedding-3-small",dimensions=1024)
        chromavectordb=Chroma.from_documents(final_pdf_document,openai_embedding,persist_directory=VECTOR_DB_PATH)
        chromavectordb.persist()#Persistent db added, so that retrieval next time is faster
        chroma_retriever=chromavectordb.as_retriever(search_kwargs={"k": 3})
    return chroma_retriever

chroma_retriever=initialize_vectordb()

app = FastAPI()

class RAG(BaseModel):
    gpt_model: Annotated[Literal["gpt-4o-mini","gpt-5-mini","gpt-5-nano"], Field(...,description="gpt llm model for the use",example="gpt-4o-mini")]
    query:Annotated[str, Field(...,description="number of documents to be searched",example="What is the minimum deposit of car?")]

##This route will only run the embedding once we load the fastapi.

@app.post('/rag')
def create_rag_chatter(ragchatter: RAG):

    gpt_llm=ChatOpenAI(model=ragchatter.gpt_model)

    prompts_template=ChatPromptTemplate.from_messages([
        ("system","You an AI assistant that helps answer the user questions."),
        ("user","Input: {input}\n\n Context:{context}")
        ])

    output_parse=StrOutputParser()

    chain= ({"input": RunnablePassthrough(), "context":chroma_retriever} | prompts_template | gpt_llm | output_parse)
    response=chain.invoke(ragchatter.query)
    
    return JSONResponse(status_code=200, content={"answer": response})


