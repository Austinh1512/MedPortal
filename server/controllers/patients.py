from extensions import db
from models import Patient
from flask import jsonify

def getPatients():
    rows = db.session.execute(db.select(Patient)).scalars().all()
    patients = [patient.to_dict() for patient in rows]
    return jsonify({"data": patients}), 200