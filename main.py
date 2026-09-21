from fastapi import FastAPI , Path , HTTPException , Query
import json

app = FastAPI()

def load_data():
    with open ("patients.json") as f:
        data = json.load(f)

    return data


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
def sort_patients(sort_by: str = Query(..., description ="sort on the basis of the height , weight or verdict "), order: str = Query("asc" , description ="sort order can br asc or desc")):

    valid_field = ["Height" , "Weight" , "Verdict"]

    if sort_by not in valid_field:
        raise HTTPException (status_code=400, detail="invalid field select form the {valid_field}")

    if order not in ["asc", "desc"]:
        raise HTTPException (status_code=400, detail="invalid order select from asc or desc")

    data = load_data()

    sort_order = True if order == "desc" else False    

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by , 0), reverse=sort_order)

    return sorted_data

    