import json
from fastapi import FastAPI, Path, HTTPException, Query

def load_data():
    with open("students.json",'r') as f:
        data=json.load(f)
    return data

app = FastAPI()

@app.get("/")
def welcome_page():
    return {"message":"Welcome to the SRS"}

@app.get("/Home")
def home():
    return {"message":"Student Record System"}

@app.get("/students")
def students():
    data=load_data()
    return data

@app.get('/students/{student_id}')
def view_student(student_id: str = Path(...,description="Get individual student records", example = "IT001")):
    data=load_data()
    for student in data:
         if student["student_id"]==student_id:
             return student
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/sortstudent/sort") 
def sort_student(sort_by: str = Query(..., description="Sort students based on age"),order: str = Query("asc", description="Order by asc or desc")): 
    if sort_by != "age": 
        raise HTTPException(status_code=400, detail="Right query param value not provided") 

    if order not in ["asc", "desc"]: 
        raise HTTPException(status_code=400, detail="Provide the right order type") 

    data = load_data() 
    sort_order = True if order == "desc" else False 
    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=sort_order) 
    return sorted_data

