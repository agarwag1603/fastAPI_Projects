import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Langgraph Chatbot")

# Input fields
topic = st.text_input("Topic")
paragraph = int(st.number_input("Number of paragraph",value=0))


if st.button("Submit"):
    data = {
    "topic": topic,
    "paragraph": paragraph,
}

    response = requests.post(f"{BASE_URL}/article", json=data)
    if response.status_code == 200:
        result = response.json()
        tab1, tab2, tab3, tab4 = st.tabs(["Graph workflow","Article", "Summary","NER"])
        with tab1:
            response_image = requests.get(f"{BASE_URL}/graph")
            st.image(response_image.content)
        with tab2:
            st.markdown(result["article"])
        with tab3:
            st.markdown(result["summary"])
        with tab4:
            st.markdown(result["named_entity"])
        
    else:
        st.error(f"Failed: {response.text}")
