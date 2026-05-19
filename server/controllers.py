import bcrypt
from flask import request, jsonify, make_response
from models import User
from extensions import db
from utils import generateAccessToken, generateRefreshToken
from dotenv import load_dotenv
import os

def register():
    data = request.get_json()

    if data is None:
        return jsonify({"message": "No json provided"}), 400

    email = data.get("email").lower()
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
    
    accessToken = generateAccessToken(new_user.id)
    refreshToken = generateRefreshToken(new_user.id)

    try:
        new_user.refresh_token = refreshToken
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": "Could not update user session."}), 500
    
    response = make_response(jsonify({"email": new_user.email, "username": new_user.username, "accessToken": accessToken}), 200)
    environment = os.getenv("FLASK_ENV")
    secure = environment == "production"
    samesite = "Lax" if environment == "development" else "None"
    response.set_cookie("refresh", refreshToken, httponly=True, secure=secure, samesite=samesite)
    return response

def login():
    data = request.get_json()

    email = data.get("email").lower()
    pw = data.get("password")

    if not email or not pw:
        return jsonify({"error": "Missing required data."}), 400

    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

    if not user:
        return jsonify({"error": "User can not be found."}), 404

    pw_bytes = pw.encode("utf-8")
    result = bcrypt.checkpw(pw_bytes, user.password.encode("utf-8"))

    if result:
        accessToken = generateAccessToken(user.id)
        refreshToken = generateRefreshToken(user.id)
        
        try:
            user.refresh_token = refreshToken
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"error": "Could not update user session."}), 500

        response = make_response(jsonify({"email": user.email, "username": user.username, "accessToken": accessToken}), 200)
        environment = os.getenv("FLASK_ENV")
        secure = environment == "production"
        samesite = "Lax" if environment == "development" else "None"
        response.set_cookie("refresh", refreshToken, httponly=True, secure=secure, samesite=samesite)
        return response
    
    return jsonify({"error": "Incorrect password"}), 401