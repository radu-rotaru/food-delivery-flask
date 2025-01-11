import jwt
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta, timezone
from app.config import Config

SECRET_KEY = Config.SECRET_KEY

def encode_auth_token(user_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "iat": datetime.now(timezone.utc),
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token is missing"}), 403
        try:
            token = auth_header.split(" ")[1]
            user_id = decode_auth_token(token)
            if isinstance(user_id, str):
                raise ValueError(user_id)
        except Exception as e:
            return jsonify({"message": str(e)}), 403
        return f(user_id, *args, **kwargs)

    return decorated
