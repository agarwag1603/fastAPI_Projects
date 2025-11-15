from dotenv import load_dotenv
from langsmith import traceable
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

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