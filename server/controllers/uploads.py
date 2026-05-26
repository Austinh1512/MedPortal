from extensions import db
from flask import request, jsonify
from utils import s3
from models import Patient, Condition, Medication, Observation, Encounter
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

load_dotenv()

def uploadPatients():
    file = request.files.get("patients")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format. Please upload a .csv file."}), 400
    rows = pd.read_csv(file)

    required = ["Id",
                "FIRST",
                "LAST",
                "RACE",
                "ETHNICITY",
                "GENDER",
                "ADDRESS",
                "CITY",
                "STATE",
                "ZIP",
                "BIRTHDATE",
                "DEATHDATE"
                ]
    
    if not set(required).issubset(list(rows.columns)):
        return jsonify({"error": "Not all required columns are present in file upload. "}), 400
    
    for i, row in rows.iterrows():
        data = Patient(
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

        db.session.merge(data)

    try:
        file.seek(0)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        s3.upload_fileobj(file, os.getenv("AWS_BUCKET_NAME"), f"{timestamp}_{file.filename}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error uploading file or saving to database"}), 500

    return jsonify({"message": "Successfully uploaded file."}), 200

def uploadConditions():
    file = request.files.get("conditions")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format. Please upload a .csv file."}), 400
    rows = pd.read_csv(file)

    required = ["PATIENT", "START", "STOP", "CODE", "DESCRIPTION"]
    
    if not set(required).issubset(list(rows.columns)):
        return jsonify({"error": "Not all required columns are present in file upload."}), 400
    
    for i, row in rows.iterrows():
        data = Condition(
            patient_id=row["PATIENT"],
            start_date=row["START"],
            stop_date=(None if pd.isna(row["STOP"]) else row["STOP"]),
            code=row["CODE"],
            description=row["DESCRIPTION"]
        )

        db.session.add(data)

    try:
        file.seek(0)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        s3.upload_fileobj(file, os.getenv("AWS_BUCKET_NAME"), f"{timestamp}_{file.filename}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error uploading file or saving to database"}), 500

    return jsonify({"message": "Successfully uploaded file."}), 200

def uploadMedications():
    file = request.files.get("medications")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format. Please upload a .csv file."}), 400
    rows = pd.read_csv(file)

    required = ["PATIENT", "START", "STOP", "CODE", "DESCRIPTION", "REASONCODE", "REASONDESCRIPTION"]
    
    if not set(required).issubset(list(rows.columns)):
        return jsonify({"error": "Not all required columns are present in file upload."}), 400
    
    for i, row in rows.iterrows():
        data = Medication(
            patient_id=row["PATIENT"],
            start_date=row["START"],
            stop_date=(None if pd.isna(row["STOP"]) else row["STOP"]),
            code=row["CODE"],
            description=row["DESCRIPTION"],
            reason_code=(None if pd.isna(row["REASONCODE"]) else row["REASONCODE"]),
            reason_description=(None if pd.isna(row["REASONDESCRIPTION"]) else row["REASONDESCRIPTION"])
        )

        db.session.add(data)

    try:
        file.seek(0)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        s3.upload_fileobj(file, os.getenv("AWS_BUCKET_NAME"), f"{timestamp}_{file.filename}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error uploading file or saving to database"}), 500

    return jsonify({"message": "Successfully uploaded file."}), 200

def uploadObservations():
    file = request.files.get("observations")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format. Please upload a .csv file."}), 400
    rows = pd.read_csv(file)

    required = ["PATIENT", "DATE", "CATEGORY", "CODE", "DESCRIPTION", "VALUE", "UNITS", "TYPE"]
    
    if not set(required).issubset(list(rows.columns)):
        return jsonify({"error": "Not all required columns are present in file upload."}), 400
    
    for i, row in rows.iterrows():
        data = Observation(
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

    try:
        file.seek(0)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        s3.upload_fileobj(file, os.getenv("AWS_BUCKET_NAME"), f"{timestamp}_{file.filename}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error uploading file or saving to database"}), 500

    return jsonify({"message": "Successfully uploaded file."}), 200

def uploadEncounters():
    file = request.files.get("encounters")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format. Please upload a .csv file."}), 400
    rows = pd.read_csv(file)

    required = ["Id", "PATIENT", "START", "ENCOUNTERCLASS", "CODE", "DESCRIPTION", "REASONCODE", "REASONDESCRIPTION"]
    
    if not set(required).issubset(list(rows.columns)):
        return jsonify({"error": "Not all required columns are present in file upload."}), 400
    
    for i, row in rows.iterrows():
        data = Encounter(
            id=row["Id"],
            patient_id=row["PATIENT"],
            start_date=row["START"],
            encounter_class=row["ENCOUNTERCLASS"],
            code=row["CODE"],
            description=row["DESCRIPTION"],
            reason_code=(None if pd.isna(row["REASONCODE"]) else row["REASONCODE"]),
            reason_description=(None if pd.isna(row["REASONDESCRIPTION"]) else row["REASONDESCRIPTION"])
        )

        db.session.merge(data)

    try:
        file.seek(0)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        s3.upload_fileobj(file, os.getenv("AWS_BUCKET_NAME"), f"{timestamp}_{file.filename}")
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error uploading file or saving to database"}), 500

    return jsonify({"message": "Successfully uploaded file."}), 200