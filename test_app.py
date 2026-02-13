from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError


# ---Root Endpoint---
def test_read_root(client):
    response_read_root = client.get("/")
    assert response_read_root.status_code == 200
    assert response_read_root.json()["message"] == "Welcome to the Prediction API!"


# ---Health Endpoint---
def test_get_health(client):
    response_health = client.get("/health")
    assert response_health.status_code == 200
    assert response_health.json()["status"] == "ok"


# ---Model Info Endpoint---
def test_get_model_info(client):
    response_model_info = client.get("/model-info")
    assert response_model_info.status_code == 200
    assert response_model_info.json()["model_name"] == "RandomForestClassifier"


# ---Predict Endpoint---
# Testing endpoint with a correct payload
def test_predict_endpoint(client):
    # Testing correct request
    payload_correct = correct_payload()
    make_prediction_response = client.post("/predict", json=payload_correct)
    assert make_prediction_response.status_code == 200
    assert (
        make_prediction_response.json()["prediction"]
        == "The employee is likely to resign."
    )


# Testing endpoint with a missing field in the payload
def test_predict_missing_endpoint(client):
    payload_missing = missing_payload()
    make_missing_prediction_response = client.post("/predict", json=payload_missing)
    assert make_missing_prediction_response.status_code == 422


# Testing endpoint with a wrong field type in the payload
def test_predict_wrong_endpoint(client):
    payload_wrong = wrong_payload()
    make_wrong_prediction_response = client.post("/predict", json=payload_wrong)
    assert make_wrong_prediction_response.status_code == 422


# Testing endpoint if probability can’t be calculated
def test_predict_endpoint_proba_error(client):
    """
    Test that simulates an error during probability calculation
    to verify that the API continues to function (try/except coverage).
    """
    proba_error_payload = correct_payload()

    # Mocking predict (to avoid crash) AND predict_proba (to trigger error)
    with patch("app.model.predict", return_value=[0]), \
         patch("app.model.predict_proba", side_effect=ValueError("Mock Error")):
        proba_error_response = client.post("/predict", json=proba_error_payload)
        assert proba_error_response.status_code == 200
        assert "prediction" in proba_error_response.json()


# Testing endpoint if the database doesn’t work
def test_predict_endpoint_db_error(client):
    """
    Testing the 'degraded' mode: If the database crashes, the API must still
    return the prediction (code 200) without crashing.
    """
    db_error_payload = correct_payload()
    with patch(
        "sqlalchemy.orm.Session.add",
        side_effect=SQLAlchemyError("Simulated database error"),
    ):
        make_db_error_response = client.post("/predict", json=db_error_payload)
        assert make_db_error_response.status_code == 200
        db_error_data = make_db_error_response.json()
        assert "prediction" in db_error_data
        assert db_error_data["prediction"] == "The employee is likely to resign."


# Testing endpoint if the employee will stay
def test_predict_endpoint_employee_stay(client):
    payload_stay = {
        "frequence_deplacement": "Aucun",
        "revenu_mensuel": 19000,  # High Salary
        "heure_supplementaires": "Non",  # No overtime
        "distance_domicile_travail": 0,  # Lives really close
        "satisfaction_employee_environnement": 4,  # Max
        "satisfaction_employee_nature_travail": 4,  # Max
        "satisfaction_employee_equipe": 4,  # Max
        "satisfaction_employee_equilibre_pro_perso": 4,  # Max
        "annee_experience_totale": 40,
        "annees_dans_l_entreprise": 40,
        "nombre_participation_pee": 3,
        "age": 60,
        "annes_sous_responsable_actuel": 40,
        "nombre_experiences_precedentes": 0,
        "note_evaluation_precedente": 4,  # Max
    }
    make_stay_response = client.post("/predict", json=payload_stay)
    assert make_stay_response.status_code == 200
    assert make_stay_response.json()["prediction"] == "The employee is likely to stay"


# ---Useful functions---
def correct_payload():  # Generates a working json request
    return {
        "frequence_deplacement": "Aucun",
        "revenu_mensuel": 2000,
        "heure_supplementaires": "Oui",
        "distance_domicile_travail": 10,
        "satisfaction_employee_environnement": 1,
        "satisfaction_employee_nature_travail": 1,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "annee_experience_totale": 20,
        "annees_dans_l_entreprise": 10,
        "nombre_participation_pee": 0,
        "age": 50,
        "annes_sous_responsable_actuel": 5,
        "nombre_experiences_precedentes": 2,
        "note_evaluation_precedente": 1,
    }


def missing_payload():  # Generates a json request missing the "age" field
    return {
        "frequence_deplacement": "Aucun",
        "revenu_mensuel": 2000,
        "heure_supplementaires": "Oui",
        "distance_domicile_travail": 10,
        "satisfaction_employee_environnement": 1,
        "satisfaction_employee_nature_travail": 1,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "annee_experience_totale": 20,
        "annees_dans_l_entreprise": 10,
        "nombre_participation_pee": 0,
        "annes_sous_responsable_actuel": 5,
        "nombre_experiences_precedentes": 2,
        "note_evaluation_precedente": 1,
    }


def wrong_payload():  # Generates a json request with wrong type for the "age" field
    return {
        "frequence_deplacement": "Aucun",
        "revenu_mensuel": 2000,
        "heure_supplementaires": "Oui",
        "distance_domicile_travail": 10,
        "satisfaction_employee_environnement": 1,
        "satisfaction_employee_nature_travail": 1,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "annee_experience_totale": 20,
        "annees_dans_l_entreprise": 10,
        "nombre_participation_pee": 0,
        "age": "fifty",
        "annes_sous_responsable_actuel": 5,
        "nombre_experiences_precedentes": 2,
        "note_evaluation_precedente": 1,
    }
