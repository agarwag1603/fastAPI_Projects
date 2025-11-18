import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Product Sentiment Analysis")

# Input fields
product_review = st.text_input("Product Review")

if st.button("Submit"):
    data = {
    "product_review": product_review,
}

    response = requests.post(f"{BASE_URL}/sentimentanalysis", json=data)
    if response.status_code == 200:
        result = response.json()
        
        st.write("### Analysis Summary")
        
        details = {
            "Issue Type": result.get("issue_type"),
            "Tone": result.get("tone"),
            "Urgency": result.get("urgency"),
            "Overall Sentiment": result.get("product_sentiment")
        }
        
        for label, value in details.items():
            if value:
                st.markdown(f"**{label}** • {value}")
        
        st.divider()
        
        st.write("### Suggested Customer Reply")
        if result.get("reply"):
            st.markdown(result["reply"])
    else:
        st.error(f"Failed: {response.text}")
