import pandas as pd
from dotenv import load_dotenv
from app import app
from extensions import db
import models
from sqlalchemy import delete
import os

load_dotenv()

path = os.getenv("SYNTHEA_DATA_PATH")

patients_df = pd.read_csv(f"{path}/patients.csv")
conditions_df = pd.read_csv(f"{path}/conditions.csv")
medications_df = pd.read_csv(f"{path}/medications.csv")
observations_df = pd.read_csv(f"{path}/observations.csv")
encounters_df = pd.read_csv(f"{path}/encounters.csv")

with app.app_context():
    db.session.execute(delete(models.Patient))
    db.session.execute(delete(models.Condition))
    db.session.execute(delete(models.Medication))
    db.session.execute(delete(models.Observation))
    db.session.execute(delete(models.Encounter))
    db.session.commit()

    for i, row in patients_df.iterrows():
        data = models.Patient(
            id=row["Id"],
            first_name=row["FIRST"],
            last_name=row["LAST"],
            race=row["RACE"],
            ethnicity=row["ETHNICITY"],
            gender=row["GENDER"],
            address=row["ADDRESS"],
            city=row["CITY"],
            state=row["STATE"],
            zip=str(row["ZIP"]),
            birth_date=row["BIRTHDATE"],
            death_date=(None if pd.isna(row["DEATHDATE"]) else row["DEATHDATE"])
        )
        
        db.session.add(data)

    print("Committing Patients...")
    db.session.commit()
    print("Patients Committed\n")

    for i, row in conditions_df.iterrows():
        data = models.Condition(
            patient_id=row["PATIENT"],
            start_date=row["START"],
            stop_date=(None if pd.isna(row["STOP"]) else row["STOP"]),
            code=row["CODE"],
            description=row["DESCRIPTION"]
        )

        db.session.add(data)

    print("Committing Conditions...")
    db.session.commit()
    print("Conditions Committed\n")

    for i, row in medications_df.iterrows():
        data = models.Medication(
            patient_id=row["PATIENT"],
            start_date=row["START"],
            stop_date=(None if pd.isna(row["STOP"]) else row["STOP"]),
            code=row["CODE"],
            description=row["DESCRIPTION"],
            reason_code=(None if pd.isna(row["REASONCODE"]) else row["REASONCODE"]),
            reason_description=(None if pd.isna(row["REASONDESCRIPTION"]) else row["REASONDESCRIPTION"])
        )

        db.session.add(data)

    print("Committing Medications...")
    db.session.commit()
    print("Medications Committed\n")

    for i, row in observations_df.iterrows():
        data = models.Observation(
            patient_id=row["PATIENT"],
            observation_date=row["DATE"],
            category=(None if pd.isna(row["CATEGORY"]) else row["CATEGORY"]),
            code=row["CODE"],
            description=row["DESCRIPTION"],
            value=(None if pd.isna(row["VALUE"]) else row["VALUE"]),
            units=(None if pd.isna(row["UNITS"]) else row["UNITS"]),
            type=(None if pd.isna(row["TYPE"]) else row["TYPE"])
        )

        db.session.add(data)

    print("Committing Observations...")
    db.session.commit()
    print("Observations Committed\n")

    for i, row in encounters_df.iterrows():
        data = models.Encounter(
            id=row["Id"],
            patient_id=row["PATIENT"],
            start_date=row["START"],
            encounter_class= row["ENCOUNTERCLASS"],
            code=row["CODE"],
            description=row["DESCRIPTION"],
            reason_code=(None if pd.isna(row["REASONCODE"]) else row["REASONCODE"]),
            reason_description=(None if pd.isna(row["REASONDESCRIPTION"]) else row["REASONDESCRIPTION"])
        )

        db.session.add(data)

    print("Committing Encounters...")
    db.session.commit()
    print("Encounters Committed\n")

print("Done")

    