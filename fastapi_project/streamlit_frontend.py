import streamlit as st
import requests

# Base URL of your FastAPI app
BASE_URL = "http://127.0.0.1:8000"

st.title("Student Record System")

# Tabs for viewing and adding students
tab1, tab2 = st.tabs(["View Students", "Add Student"])

with tab1:
    st.subheader("All Students")
    if st.button("Load Students"):
        response = requests.get(f"{BASE_URL}/students")
        if response.status_code == 200:
            students = response.json()
            if isinstance(students, dict):
                students = students.values()
            st.table(students)
        else:
            st.error("Failed to fetch students.")

with tab2:
    st.subheader("Add New Student")

    # Input fields
    student_id = st.text_input("Student ID (e.g. IT001)")
    student_name = st.text_input("Name")
    age = st.number_input("Age",step=1)
    std = st.text_input("Class Grade")
    favorite_subject = st.text_input("Favorite Subject")
    school_name = st.text_input("School Name")
    city = st.text_input("City")
    total_marks = st.number_input("Total Marks", step=1)

    if st.button("Submit"):
        data = {
            "student_id": student_id,
            "student_name": student_name,
            "age": age,
            "std": std,
            "favorite_subject": favorite_subject,
            "school_name": school_name,
            "city": city,
            "total_marks": total_marks
        }

        response = requests.post(f"{BASE_URL}/create", json=data)
        if response.status_code == 201:
            st.success("Student added successfully!")
        else:
            st.error(f"Failed: {response.text}")
