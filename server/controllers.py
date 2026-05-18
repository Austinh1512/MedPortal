import bcrypt
from flask import request, jsonify
from models import User
from extensions import db

def register():
    data = request.get_json()

    if data is None:
        return jsonify({"message": "No json provided"}), 400

    email = data.get("email")
    username = data.get("username")
    pw = data.get("password")

    if not email or not username or not pw:
        return jsonify({"error": "Missing required data."}), 400

    pw_bytes = pw.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)

    try:
        new_user = User(
            email=email,
            username=username,
            password=hashed
        )

        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": "Could not create user."}), 500
    
    return jsonify({"message": "Hit register route"}), 200

def login():
    pass