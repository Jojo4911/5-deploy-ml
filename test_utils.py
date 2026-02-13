import pytest
from utils import preprocess_input
from schemas import EmployeeData


def get_base_data():
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


# Scenario 1: Base data (All > 0)
data_nominal = get_base_data()

# Scenario 2: Income = 0
data_revenu_zero = get_base_data()
data_revenu_zero["revenu_mensuel"] = 0

# Scenario 3: experience = 0
data_exp_zero = get_base_data()
data_exp_zero["annee_experience_totale"] = 0

# Scenario 4: Both at 0
data_double_zero = get_base_data()
data_double_zero["revenu_mensuel"] = 0
data_double_zero["annee_experience_totale"] = 0


@pytest.mark.parametrize(
    "scenario, input_dict, expected_checks",
    [
        (
            "Nominal Case (All > 0)",
            data_nominal,
            {0: 0.0, 1: 0.0005, 6: 2000, 8: 0.005, 13: 100.0},
        ),
        ("No Income Case", data_revenu_zero, {0: 0, 1: 0, 6: 0, 8: 0}),
        ("No Experience Case", data_exp_zero, {13: 0}),
        ("Double Zero Case", data_double_zero, {0: 0, 1: 0, 6: 0, 8: 0, 13: 0}),
    ],
)
def test_preprocess_logic(scenario, input_dict, expected_checks):
    # Transforming the dictionary into a Pydantic object
    input_data = EmployeeData(**input_dict)

    # Function call
    result = preprocess_input(input_data)

    # Checking key points
    if isinstance(result[0], list):
        result_to_check = result[0]
    else:
        result_to_check = result

    # Verifications
    for index, expected_value in expected_checks.items():
        # First, we check that the index exists to avoid a crash
        if index < len(result_to_check):
            assert (
                result_to_check[index] == expected_value
            ), f"Failure on {scenario} at index {index}"
        else:
            pytest.fail(
                f"Index {index} out of range. "
                f"The list only has {len(result_to_check)} elements."
            )
