import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("LLM Topic Generator")

# Input fields
topic = st.text_input("Topic")
type_of_content = st.text_input("Type of content")


if st.button("Submit"):
    data = {
        "topic": topic,
        "type": type_of_content
    }

    response = requests.post(f"{BASE_URL}/chatme", json=data)
    if response.status_code == 200:
        result = response.json()
        st.markdown(result)
    else:
        st.error(f"Failed: {response.text}")
