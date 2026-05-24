from extensions import db
from models import Patient
from flask import jsonify

def getPatients():
    rows = db.session.execute(db.select(Patient)).scalars().all()
    patients = [patient.to_dict() for patient in rows]
    return jsonify({"data": patients}), 200

def getPatientById(id):
    row = db.session.execute(db.select(Patient).filter_by(id=id)).scalar_one_or_none()
    if row is None:
        return jsonify({"error": "Patient not found."}), 404
    patient = row.to_dict()
    return jsonify({"data": patient}), 200