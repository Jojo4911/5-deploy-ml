from typing import Literal
from pydantic import BaseModel, NonNegativeInt, PositiveInt

class EmployeeData(BaseModel):
    frequence_deplacement: Literal["Aucun", "Occasionnel", "Frequent"]
    revenu_mensuel: NonNegativeInt
    heure_supplementaires: Literal["Oui", "Non"]
    distance_domicile_travail: NonNegativeInt
    satisfaction_employee_environnement: PositiveInt
    satisfaction_employee_nature_travail: PositiveInt
    satisfaction_employee_equipe: PositiveInt
    satisfaction_employee_equilibre_pro_perso: PositiveInt
    annee_experience_totale: NonNegativeInt
    annees_dans_l_entreprise: NonNegativeInt
    nombre_participation_pee: NonNegativeInt
    age: NonNegativeInt
    annes_sous_responsable_actuel: NonNegativeInt
    nombre_experiences_precedentes: NonNegativeInt
    note_evaluation_precedente: PositiveInt
