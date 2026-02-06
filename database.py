from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv
import urllib.parse

# Loading the variables from the .env file.
load_dotenv()

# Password definition
raw_password = "J0n@th@n"
encoded_password = urllib.parse.quote_plus(raw_password)

# PostgreSQL URL Connection
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
if password:
    password = urllib.parse.quote_plus(password)
host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

if user and password and host and db_name:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db_name}"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Temporary example

# Engine creation
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session class creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Classes definition
class Base(DeclarativeBase):
    pass


class PredictionHistory(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    frequence_deplacement = Column(String)
    revenu_mensuel = Column(Integer)
    heure_supplementaires = Column(String)
    distance_domicile_travail = Column(Integer)
    satisfaction_employee_environnement = Column(Integer)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    nombre_participation_pee = Column(Integer)
    age = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)
    nombre_experiences_precedentes = Column(Integer)
    note_evaluation_precedente = Column(Integer)
    prediction = Column(String)
    probability = Column(Float)
