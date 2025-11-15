import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("PDF RAG Chatbot")

# Input fields
gpt_model = st.selectbox("Choose a Model", ("gpt-4o-mini","gpt-5-mini","gpt-5-nano"))
query = st.text_input("Your query related to the document")


if st.button("Submit"):
    data = {
    "gpt_model": gpt_model,
    "query": query
}

    response = requests.post(f"{BASE_URL}/rag", json=data)
    if response.status_code == 200:
        result = response.json()
        st.markdown(result["answer"])
    else:
        st.error(f"Failed: {response.text}")
