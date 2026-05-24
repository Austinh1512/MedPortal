from extensions import db
from models import Patient, Condition, Medication, Observation, Encounter
from flask import jsonify

def getPatients():
    rows = db.session.execute(db.select(Patient)).scalars().all()
    patients = [patient.to_dict() for patient in rows]
    return jsonify({"data": patients}), 200

def getPatientById(id):
    row = db.session.get(Patient, id)
    if row is None:
        return jsonify({"error": "Patient not found."}), 404
    patient = row.to_dict()
    return jsonify({"data": patient}), 200

def getPatientConditions(id):
    rows = db.session.execute(db.select(Condition).filter_by(patient_id=id)).scalars().all()
    conditions = [condition.to_dict() for condition in rows]
    return jsonify({"data": conditions}), 200

def getPatientMedications(id):
    rows = db.session.execute(db.select(Medication).filter_by(patient_id=id)).scalars().all()
    medications = [medication.to_dict() for medication in rows]
    return jsonify({"data": medications}), 200

def getPatientObservations(id):
    rows = db.session.execute(db.select(Observation).filter_by(patient_id=id)).scalars().all()
    observations = [observation.to_dict() for observation in rows]
    return jsonify({"data": observations}), 200

def getPatientEncounters(id):
    rows = db.session.execute(db.select(Encounter).filter_by(patient_id=id)).scalars().all()
    encounters = [encounter.to_dict() for encounter in rows]
    return jsonify({"data": encounters}), 200
