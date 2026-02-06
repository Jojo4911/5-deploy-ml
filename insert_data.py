import pandas as pd
import datetime
from database import SessionLocal, PredictionHistory, engine

# Loading and merging
print("Data loading and merging...")
df_eval = pd.read_csv("extrait_eval.csv")
df_sirh = pd.read_csv("extrait_sirh.csv")
df_sondage = pd.read_csv("extrait_sondage.csv")

# Key cleaning
df_eval["eval_number_clean"] = df_eval["eval_number"].astype(str).str.replace('E_', '').astype(int)

# Merges
df_merged = pd.merge(
    left=df_sirh,
    right=df_eval,
    how='inner',
    left_on='id_employee',
    right_on='eval_number_clean'
)

df_final = pd.merge(
    left=df_merged,
    right=df_sondage,
    how='inner',
    left_on='id_employee',
    right_on='code_sondage'
)

print(f"Merger complete. {len(df_final)} lines ready.")

# Preparing for insertion
session = SessionLocal()
count = 0

expected_columns = PredictionHistory.__table__.columns.keys()

print("Inserting into database in progress...")

for index, row in df_final.iterrows():
    row_dict = row.to_dict()
    raw_target = row_dict.get("a_quitte_l_entreprise")
    if raw_target == "Oui":
        prediction_val = "1"
        proba_val = 1.0
    else:
        prediction_val = "0"
        proba_val = 0.0

    # Building the filtered data dictionary
    db_data = {}
    for col in expected_columns:
        if col in row_dict:
            db_data[col] = row_dict[col]

    # Adding the missing calculated fields
    db_data["prediction"] = prediction_val
    db_data["probability"] = proba_val
    db_data["timestamp"] = datetime.datetime.now()

    # Object creation
    entry = PredictionHistory(**db_data)
    session.add(entry)
    count += 1

session.commit()
session.close()

print(f"Done! {count} lines inserted.")