from fastapi import FastAPI
from schemas import EmployeeData
from utils import preprocess_input

app = FastAPI(
    title="Employee Retention Prediction API",
    description="API to predict whether an employee will resign",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Prediction API!"}


@app.post("/predict")
def predict_attrition(input_data: EmployeeData):
    feature_vector = preprocess_input(input_data)
    prediction = 1
    probability = 0.85

    if prediction == 1:
        result = "The employee is about to resign."
    else:
        result = "The employee stays"

    return {
        "prediction": result,
        "probability": probability,
        "input_processed": feature_vector,
    }
