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

load_dotenv()

app = FastAPI()

class RAG(BaseModel):
    chunk_size: Annotated[int, Field(...,description="chunk size for the file splitting",example=500)]
    chunk_overlap: Annotated[int, Field(...,description="chunk overlap for the overlapping of the sentences",example=50)]
    gpt_model: Annotated[Literal["gpt-4o-mini","gpt-5-mini","gpt-5-nano"], Field(...,description="gpt llm model for the use",example="gpt-4o-mini")]
    embedding_model: Annotated[str, Field(...,description="gpt embedding model",example="text-embedding-3-small")]
    dimension: Annotated[int, Field(...,description="gpt embedding model dimension",example=1024)]
    search_kwargs: Annotated[int, Field(...,description="number of documents to be searched",example=3, gt=0, lt=5)]
    query:Annotated[str, Field(...,description="number of documents to be searched",example="What is the minimum deposit of car?")]

@app.post('/rag')
def create_rag_chatter(ragchatter: RAG):

    gpt_llm=ChatOpenAI(model=ragchatter.gpt_model)

    pdf_path = Path(__file__).parent / "RentalConditions.pdf"

    pypdf_loader=PyPDFLoader(str(pdf_path))
    rentalcondition_loader=pypdf_loader.load()

    pdf_document_splitter=RecursiveCharacterTextSplitter(chunk_size=ragchatter.chunk_size,chunk_overlap=ragchatter.chunk_overlap)
    final_pdf_document=pdf_document_splitter.split_documents(rentalcondition_loader)

    openai_embedding = OpenAIEmbeddings(model=ragchatter.embedding_model,dimensions=ragchatter.dimension)

    chromavectordb=Chroma.from_documents(final_pdf_document,openai_embedding)
    chroma_retriever=chromavectordb.as_retriever(search_kwargs={"k": ragchatter.search_kwargs})

    prompts_template=ChatPromptTemplate.from_messages([
        ("system","You an AI assistant that helps answer the user questions."),
        ("user","Input: {input}\n\n Context:{context}")
        ])

    output_parse=StrOutputParser()

    chain= ({"input": RunnablePassthrough(), "context":chroma_retriever} | prompts_template | gpt_llm | output_parse)
    response=chain.invoke(ragchatter.query)
    
    return JSONResponse(status_code=200, content={"answer": response})


