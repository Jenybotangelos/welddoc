from flask import Blueprint, request, jsonify
from app.database import db
from app.models.person import User
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__)


@users_bp.route("", methods=["GET"])
def get_users():
    role = request.args.get("role")
    query = User.query
    if role:
        query = query.filter_by(role=role)
    rows = query.filter_by(archived=False).all()
    return jsonify([_serialize(u) for u in rows])


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return jsonify(_serialize(u))


@users_bp.route("", methods=["POST"])
def create_or_update_user():
    data = request.get_json()
    if "id" in data and data["id"]:
        u = User.query.get_or_404(data["id"])
        u.name = data.get("name", u.name)
        u.email = data.get("email", u.email)
        u.role = data.get("role", u.role)
        if "password" in data:
            u.password_hash = generate_password_hash(data["password"])
        if "archived" in data:
            u.archived = data["archived"]
    else:
        u = User(
            name=data["name"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"]),
            role=data["role"],
        )
        db.session.add(u)
    db.session.commit()
    return jsonify(_serialize(u)), 200


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    u = User.query.filter_by(email=data.get("email")).first()
    if not u or not check_password_hash(u.password_hash, data.get("password", "")):
        return jsonify({"error": "Invalid email or password"}), 401
    return jsonify(_serialize(u)), 200


def _serialize(u):
    return {
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role": u.role,
        "archived": u.archived,
    }
