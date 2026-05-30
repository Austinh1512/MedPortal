from extensions import db
from flask import jsonify
from models import Patient, Condition
from sqlalchemy import func, select, desc
from datetime import date

def getDashboardSummary():
    patient_count = db.session.scalar(select(func.count()).select_from(Patient))

    genders = db.session.execute(select(Patient.gender, func.count()).select_from(Patient).group_by(Patient.gender)).all()
    gender_breakdown = {}
    for gender, count in genders:
        gender_breakdown[gender] = count

    age_distribution = {
        "0-10": 0,
        "11-20": 0,
        "21-40": 0,
        "41-60": 0,
        "61-80": 0,
        "80+": 0
    }

    ages = db.session.execute(select(Patient.birth_date, Patient.death_date).select_from(Patient)).all()

    for birth_date, death_date in ages:
        end_date = death_date if death_date else date.today()
        age = end_date.year - birth_date.year - ((end_date.month, end_date.day) < (birth_date.month, birth_date.day))
        
        if age <= 10:
            age_distribution["0-10"] += 1
        elif age <= 20:
            age_distribution["11-20"] += 1
        elif age <= 40:
            age_distribution["21-40"] += 1
        elif age <= 60:
            age_distribution["41-60"] += 1
        elif age <= 80:
            age_distribution["61-80"] += 1
        else:
            age_distribution["80+"] += 1

    conditions_query = db.session.execute(select(Condition.description, func.count()).select_from(Condition).group_by(Condition.description).order_by(desc(func.count())).limit(10)).all()
    top_10_conditions = []
    for condition, count in conditions_query:
        top_10_conditions.append({"condition": condition, "count": count})


    return jsonify({"patient_count": patient_count, "gender_breakdown": gender_breakdown, "age_distribution": age_distribution, "top_10_conditions": top_10_conditions}), 200