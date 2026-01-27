---
title: 5-deploy-ml
emoji: 🔮
colorFrom: yellow
colorTo: pink
sdk: docker
pinned: false
short_description: Employee Attrition Prediction
---

# Futurisys - POC : Prédiction de l'Attrition Employé (TechNova Partners)

## 📋 Présentation du Projet

Dans le cadre d'une mission pour **Futurisys**, ce projet vise à déployer un outil de classification pour l'entreprise TechNova Partners. L'objectif est d'identifier les causes racines derrière les démissions (attrition) afin de proposer des plans d'action ciblés.

Le moteur de prédiction repose sur un modèle **Random Forest allégé**, optimisé pour la production. L'application est hébergée sur Hugging Face Spaces, offrant une interface API robuste et une traçabilité complète des prédictions via une base de données PostgreSQL.

## 🚀 Fonctionnalités

* **API REST** : Développée avec FastAPI pour des performances optimales, rapidité, validation automatique avec Pydantic, documentation Swagger native.
* **Modèle ML** : Classification binaire (Attrition: Oui/Non) via Random Forest.
* **Hébergement Cloud** : Déploiement continu sur Hugging Face Spaces.
* **Persistance PostgreSQL** : Historisation de chaque prédiction (inputs RH et scores d'attrition) pour analyse ultérieure. PostgreSQL a été choisi pour la persistance et l’intégrité des données et la scalabilité.
* **Validation Pydantic** : Contrôle strict de la conformité des données employés envoyées à l'API.
* **Tests & Qualité** : Couverture de tests unitaires et fonctionnels avec Pytest.

## 🏗️ Architecture des outils utilisés

L’ensemble des outils utilisés peuvent être représentés selon la vue d’ensemble suivante :

```mermaid
flowchart TD
    A[👩‍💻 Utilisateur / Client] -->|Envoie des données : requête HTTP| B[⚡ FastAPI - API]
    B --> C[✅ Pydantic - Validation des entrées]
    C --> D[🧠 Modèle ML - Prédiction]
    D --> E[(💾 PostgreSQL - Base de données)]
    E --> D
    D -->|Renvoie la prédiction| B
    B -->|Renvoie la réponse JSON| A

    subgraph Infrastructure
        F[🐳 Docker - Conteneur]
        G[☁️ Hugging Face Spaces - Hébergement]
        H[🤖 GitHub Actions - CI/CD]
    end

    F --> B
    H --> F
    H --> G
    G --> B
```


## 🛠️ Installation et Configuration

### Prérequis

* Python 3.12+
* PostgreSQL (local ou Docker)
* Git

### Installation locale

1. Cloner le dépôt :

```
git clone [https://github.com/votre-utilisateur/futurisys-attrition-app.git](https://github.com/votre-utilisateur/futurisys-attrition-app.git)
cd futurisys-attrition-app
```

2. Initialiser l'environnement :

```
# Installer Poetry si ce n'est pas fait
curl -sSL https://install.python-poetry.org | python3 -
# Installer les dépendances du projet
poetry install
# Activer l'environnement virtuel
poetry env activate
```
Le fichier Requirements.txt peut également être utilisé en tant qu’alternative à poetry.

3. Variables d'environnement (.env) :
```
DATABASE_URL=postgresql://user:password@localhost:5432/attrition_db
API_KEY=votre_cle_secrete
```

## 🌍 Déploiement sur Hugging Face Spaces

L'application est synchronisée automatiquement avec Hugging Face.
* **URL du Space** : https://huggingface.co/spaces/VOTRE_NOM/TechNova-Attrition-POC
* **Configuration** : Le déploiement utilise un environnement Docker pour garantir la reproductibilité des prédictions.

## 🖥️ Utilisation de l'API

### Architecture logique interne de l’API FastAPI

```mermaid
graph TD
    A[🌐 main.py - Point d'entrée API]
    A --> B[📦 routes/ - Définit les endpoints : predict, health...]
    A --> C[🧩 models/ - Modèle ML & préprocesseur]
    A --> D[🧾 schemas.py - Classes Pydantic]
    A --> E[🧰 utils/ - Fonctions utilitaires]
    A --> F[🧪 tests/ - Tests Pytest]
    A --> G[💾 database/ - Connexion PostgreSQL]

    B --> D
    B --> C
    B --> G
    F --> A
```

### Lancement local

```
uvicorn app.main:app --reload
```

### Exemple de requête (Prédiction d'attrition)

L'API attend 15 caractéristiques socio-professionnelles de l'employé :
```
curl -X 'POST' \
  '[https://votre-space.hf.space/predict](https://votre-space.hf.space/predict)' \
  -H 'X-API-KEY: votre_cle' \
  -H 'Content-Type: application/json' \
  -d '{
  "frequence_deplacement": "Occasionnel",
  "heure_supplementaires": "Non",
  "annees_dans_l_entreprise": 12,
  "nombre_participation_pee": 2,
  "age": 47,
  "revenu_mensuel": 5993,
  "annes_sous_responsable_actuel": 5,
  "distance_domicile_travail": 8,
  "satisfaction_employee_environnement": 2,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 1,
  "satisfaction_employee_equilibre_pro_perso": 3,
  "annee_experience_totale": 8,
  "nombre_experiences_precedentes": 3,
  "note_evaluation_precedente": 3
}'
```

## 📊 Structure des Données (PostgreSQL)

Chaque requête à l'API est enregistrée pour permettre au client TechNova Partners d'auditer les décisions du modèle.

Table `predictions`
* `id` : Identifiant unique.
* `employee_features` : Données envoyées (Age, Salaire, etc.) au format JSONB.
* `attrition_probability` : Score de probabilité calculé par le Random Forest.
* `prediction` : Résultat final (0 ou 1).
* `created_at` : Horodatage de la requête.

## 🧪 Tests et Fiabilité
La robustesse du déploiement est vérifiée par une suite de tests :
* **Tests Unitaires** : Validation du chargement du modèle et des fonctions de prétraitement.
* **Tests Fonctionnels** : Simulation d'appels API avec des cas limites (données manquantes, formats invalides).

```
# Lancer les tests
pytest
# Vérifier la couverture
pytest --cov=app tests/
```

## 🔄 Pipeline CI/CD

La pipeline CI/CD peut être représentée simplement de la manière suivante :

```mermaid
flowchart LR
    A[💾 Commit sur GitHub] --> B[🔍 GitHub Actions - Lancement pipeline]
    B --> C[🧪 Étape 1 : Exécution des tests : pytest]
    C --> D[🐍 Étape 2 : Vérification du code : linting, formatting]
    D --> E[🐳 Étape 3 : Build de l'image Docker]
    E --> F[☁️ Étape 4 : Déploiement sur Hugging Face Spaces]
    F --> G[✅ Application accessible en ligne]

```

Le workflow GitHub Actions assure :

1. La validation du code (Linting & Tests).
2. Le build de l'image Docker.
3. Le push vers le secret `HF_TOKEN` pour mettre à jour le Space Hugging Face en temps réel.

*Livrable réalisé pour le projet d'ingénierie IA - Client : Futurisys / Cas d'étude : TechNova Partners.*