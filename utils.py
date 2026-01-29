from schemas import EmployeeData


def preprocess_input(data: EmployeeData):
    # 1. Conversion of categorical variables (mapping)
    mapping_deplacement = {"Aucun": 0, "Occasionnel": 1, "Frequent": 2}
    mapping_heures_sup = {"Non": 0, "Oui": 1}

    CONV_frequence_deplacement = mapping_deplacement[
        data.frequence_deplacement
    ]
    CONV_heure_supplementaires = mapping_heures_sup[data.heure_supplementaires]
    
    # 2. Feature Engineering Calculations (FE_)
    if data.revenu_mensuel == 0:
        FE_tension_deplacement = 0
        FE_tension_heures_sup = 0
        FE_tension_distance = 0
    else:
        FE_tension_deplacement = (
            CONV_frequence_deplacement / data.revenu_mensuel
        )
        FE_tension_heures_sup = (
            CONV_heure_supplementaires / data.revenu_mensuel
        )
        FE_tension_distance = (
            data.distance_domicile_travail / data.revenu_mensuel
        )


    FE_moyenne_satisfaction = (
        data.satisfaction_employee_environnement +
        data.satisfaction_employee_nature_travail +
        data.satisfaction_employee_equipe +
        data.satisfaction_employee_equilibre_pro_perso
    ) / 4

    if data.annee_experience_totale == 0:
        FE_rentabilite_experience = 0
    else:
        FE_rentabilite_experience = (
            data.revenu_mensuel / data.annee_experience_totale
        )

    # 3. Return the transformed data
    transformed_features = [
        FE_tension_deplacement,
        FE_tension_heures_sup,
        data.annees_dans_l_entreprise,
        data.nombre_participation_pee,
        CONV_heure_supplementaires,
        data.age,
        data.revenu_mensuel,
        data.annes_sous_responsable_actuel,
        FE_tension_distance,
        FE_moyenne_satisfaction,
        data.annee_experience_totale,
        data.distance_domicile_travail,
        data.nombre_experiences_precedentes,
        FE_rentabilite_experience,
        data.satisfaction_employee_environnement,
        data.note_evaluation_precedente,
        data.satisfaction_employee_equilibre_pro_perso
    ]
    
    return [transformed_features]
