import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import boto3
import os

load_dotenv()

#JWT
jwt_secret = os.getenv("JWT_SECRET_KEY")

def generateAccessToken(user_id):
    return jwt.encode({"id": user_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}, jwt_secret, algorithm="HS256")

def generateRefreshToken(user_id):
    return jwt.encode({"id": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=7)}, jwt_secret, algorithm="HS256")

def decodeJWT(token):
    try:
        return jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
        return None

#Route Protector Decorator   
def protected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization").split(" ")[1]
            if not decodeJWT(token):
                return jsonify({"error": "Unauthorized access."}), 401
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized access."}), 401
        
    return wrapper

#AWS S3 Setup
s3 = boto3.client("s3")