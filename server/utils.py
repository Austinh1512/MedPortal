import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

load_dotenv()

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