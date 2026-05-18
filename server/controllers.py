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
    hashed = bcrypt.hashpw(pw_bytes, salt).decode("utf-8")

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
    
    return jsonify({"email": email, "username": username}), 200

def login():
    data = request.get_json()

    email = data.get("email")
    pw = data.get("password")

    if not email or not pw:
        return jsonify({"error": "Missing required data."}), 400

    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

    if not user:
        return jsonify({"error": "User can not be found."}), 404

    pw_bytes = pw.encode("utf-8")
    result = bcrypt.checkpw(pw_bytes, user.password.encode("utf-8"))

    if result:
        return jsonify({"email": user.email, "username": user.username}), 200
    elif not result:
        return jsonify({"error": "Incorrect password"}), 401
    
    return jsonify({"error": "Something went wrong"}), 500