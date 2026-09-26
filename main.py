from fastapi import FastAPI, Path, HTTPException, Query 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json


app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description = 'The ID of the patient', example = 'P001')]
    Name: Annotated[str, Field(..., description = 'Name of the patient')]
    City: Annotated[str, Field(..., description = 'City where the patient is living')]
    Age: Annotated[int, Field(..., gt= 0, lt= 120, description = 'Age of the patient')]
    Gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description = 'Gender of the patient')]
    Height : Annotated[float, Field(..., description = 'Height of the patient in mtrs')]
    Weight : Annotated[float, Field(..., description = 'Weight of the patient in kg')]

    @computed_field
    @property   
    def BMI(self) -> float:
        BMI = round(self.Weight / (self.Height ** 2), 2)
        return BMI
        
    @computed_field
    @property
    def Verdict(self) -> str:
        BMI = self.BMI

        if BMI < 18.5:
            return "Underweight"
        elif BMI < 25:
            return "Normal weight"
        elif BMI < 30:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open ("patients.json") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")

def Hello():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A Fully Functional API To Manage Patient Record "}

@app.get("/view")
def view():
    data = load_data()

    return data


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description = "The ID of the patient in the DB" ,example = "P001")):
    # load the data from the JSON file
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description ="sort on the basis of the height , weight , bmi or verdict "), order: str = Query("asc" , description ="sort order can br asc or desc")):

    valid_field = ["Height" , "Weight" , "BMI" , "Verdict"]

    if sort_by not in valid_field:
        raise HTTPException (status_code=400, detail=f"invalid field select from {valid_field}")

    if order not in ["asc", "desc"]:
        raise HTTPException (status_code=400, detail="invalid order select from asc or desc")

    data = load_data() 

    sort_order = True if order == "desc" else False    

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by , 0), reverse=sort_order)

    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):

    # Load the existing to the database from the json file
    data = load_data()

    # Check if the patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="the patient id already exist")

    # Add the new patient to the database
    data[patient.id] = patient.model_dump(exclude=["id"])

    # Save into the json file
    save_data(data)

    return JSONResponse(status_code=201,content={"message": "patient created successfully"})