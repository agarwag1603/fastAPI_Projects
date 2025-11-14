import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("PDF RAG Chatbot")

# Input fields
chunk_size = int(st.number_input("Chunk size value", value=0))
chunk_overlap = int(st.number_input("Chunk overlap value",value=0))
gpt_model = st.selectbox("Choose a Model", ("gpt-4o-mini","gpt-5-mini","gpt-5-nano"))
embedding_model = "text-embedding-3-small"
dimension = int(st.number_input("Dimension value for embedding",value=0))
search_kwargs = int(st.number_input("search kwargs for retrieval",value=0))
query = st.text_input("Your query related to the document")


if st.button("Submit"):
    data = {
    "chunk_size": chunk_size,
    "chunk_overlap": chunk_overlap,
    "gpt_model": gpt_model,
    "embedding_model": embedding_model,
    "dimension": dimension,
    "search_kwargs": search_kwargs,
    "query": query
}

    response = requests.post(f"{BASE_URL}/rag", json=data)
    if response.status_code == 200:
        result = response.json()
        st.markdown(result["answer"])
    else:
        st.error(f"Failed: {response.text}")
