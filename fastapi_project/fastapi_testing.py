import json
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,Optional
import os

app = FastAPI()

current_script_path = os.path.abspath(__file__)
current_script_directory = os.path.dirname(os.path.dirname(current_script_path))
file_name= os.path.join(current_script_directory,"students.json")

class Student(BaseModel):
    student_id: Annotated[str,Field(..., description = "student roll number",example = "IT001")]
    student_name: Annotated[str,Field(..., description = "student name",example = "Gaurav")]
    age: Annotated[int,Field(..., gt=0, lt=121, description = "Student age",example = 15)]
    std: Annotated[str,Field(..., description = "Student class grade",example = "8th Grade")]
    favorite_subject: Annotated[str,Field(..., description = "Faviorite subject",example = "Physics")]
    school_name: Annotated[str,Field(..., description = "name of the school",example = "SD Jain")]
    city: Annotated[str,Field(..., description = "name of the city",example = "Mumbai")]
    total_marks: Annotated[int,Field(..., lt=501, description = "total marks in exam",example = 451)]

    @computed_field
    @property
    def total_percentage(self) -> float:
        total_percentage=(self.total_marks/500)*100
        return total_percentage

class UpdateStudent(BaseModel):
    student_id: Annotated[Optional[str],Field(default=None)]
    student_name: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None, gt=0, lt=121)]
    std: Annotated[Optional[str],Field(default=None)]
    favorite_subject: Annotated[Optional[str],Field(default=None)]
    school_name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    total_marks: Annotated[Optional[int],Field(default=None, gt=0, lt=501)]

def load_data():
    with open(file_name,'r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open(file_name,'w') as f:
        json.dump(data,f)

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
    if student_id in data:
        return data[student_id]
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/sortstudent/sort") 
def sort_student(sort_by: str = Query(..., description="Sort students based on age"),order: str = Query("asc", description="Order by asc or desc")): 
    if sort_by != "age": 
        raise HTTPException(status_code=400, detail="Right query param value not provided") 

    if order not in ["asc", "desc"]: 
        raise HTTPException(status_code=400, detail="Provide the right order type") 

    data = load_data() 
    sort_order = True if order == "desc" else False 
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order) 
    return sorted_data

@app.post('/create')
def create_student(student:Student):

    data = load_data()

    if student.student_id in data:
        raise HTTPException(status_code=400, detail="Student already exists")
    
    data[student.student_id] = student.model_dump(exclude=['student_id'])
    save_data(data)

    return JSONResponse(status_code=201, content={"message":"student added"})

@app.put('/update/{student_id}')
def update_student(student_id: str, student_update:UpdateStudent):

    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student record not found")
    
    existing_info=data[student_id]
    updated_info=student_update.model_dump(exclude_unset=True)

    for key, values in updated_info.items():
        existing_info[key]=values

    existing_info['student_id']=student_id
    student_pydantic_obj = Student(**existing_info)

    existing_info=student_pydantic_obj.model_dump(exclude='student_id')

    data[student_id]=existing_info
    save_data(data)
    return JSONResponse(status_code=200, content={"message":"student updated"})

