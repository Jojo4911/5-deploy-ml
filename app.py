import joblib
from fastapi import FastAPI, Depends
from schemas import EmployeeData
from utils import preprocess_input
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy.orm import Session
from database import SessionLocal, PredictionHistory
import datetime

model: RandomForestClassifier = joblib.load("model.joblib")

app = FastAPI(
    title="Employee Retention Prediction API",
    description="API to predict whether an employee will resign",
    version="1.0.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def predict_attrition(input_data: EmployeeData, db: Session = Depends(get_db)):
    # Preprocessing
    features_vector = preprocess_input(input_data)

    # Compute the Prediction with the model
    prediction = model.predict(features_vector)

    # Get the probability of the prediction
    try:
        probability = model.predict_proba(features_vector)[0][1]
    except Exception:
        probability = None

    predicted_class = int(prediction[0])

    # Database addition
    try:
        new_entry = PredictionHistory(
            timestamp = datetime.datetime.now(),
            **input_data.model_dump(),
            prediction=str(predicted_class),
            probability=float(probability)
        )

        # Database saving
        db.add(new_entry)
        db.commit()
    except Exception as e:
        print(f"Warning: Impossible to save into the database. (Error: {e})")
        print('The API continues in "no-persistent" mode')

    # Response message
    if predicted_class == 1:
        result = "The employee is likely to resign."
    else:
        result = "The employee is likely to stay"

    return {
        "prediction": result,
        "probability": probability,
        "input_processed": features_vector,
    }
