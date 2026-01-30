import joblib
from fastapi import FastAPI
from schemas import EmployeeData
from utils import preprocess_input
from sklearn.ensemble import RandomForestClassifier

model: RandomForestClassifier = joblib.load("model.joblib")

app = FastAPI(
    title="Employee Retention Prediction API",
    description="API to predict whether an employee will resign",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Prediction API!"}


@app.get("/health")
def health_check():
    return {"status": "ok", "machine_learning_model": "loaded"}


@app.get("/model-info")
def get_model_info():
    return {
        "model_name": "RandomForestClassifier",
        "version": "1.0.0",
        "description": "Employee attrition prediction model",
        "author": "Jonathan Fernandez",
    }


@app.post("/predict")
def predict_attrition(input_data: EmployeeData):
    features_vector = preprocess_input(input_data)

    prediction = model.predict(features_vector)

    try:
        probability = model.predict_proba(features_vector)[0][1]
    except Exception:
        probability = None

    predicted_class = int(prediction[0])

    if predicted_class == 1:
        result = "The employee is likely to resign."
    else:
        result = "The employee is likely to stay"

    return {
        "prediction": result,
        "probability": probability,
        "input_processed": features_vector,
    }
