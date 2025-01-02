from flask import Blueprint, request, jsonify
from app.models import db, User
from app.auth import encode_auth_token, token_required

routes = Blueprint("routes", __name__)

@routes.route('/')
def hello_world():
    return "Hello, World with __init__.py and routes!"

@routes.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing required fields"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 400
    user = User(
        email=data["email"],
        role=data.get("role", "customer"),
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@routes.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        token = encode_auth_token(user.id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@routes.route("/me", methods=["GET"])
@token_required
def get_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"id": user.id, "email": user.email, "role": user.role}), 200
