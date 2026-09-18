from flask import Blueprint, request, jsonify
from src.services.auth.app_user_service import AppUserService

user_bp = Blueprint("user", __name__, url_prefix="/api/users")
service = AppUserService()


@user_bp.get("")
def list_users():
    return jsonify(service.list_all()), 200


@user_bp.get("/<int:id_user>")
def get_user(id_user):
    return jsonify(service.get(id_user)), 200


@user_bp.post("")
def create_user():
    data = request.get_json(silent=True) or {}
    return jsonify(service.create(data)), 201


@user_bp.put("/<int:id_user>")
def update_user(id_user):
    data = request.get_json(silent=True) or {}
    return jsonify(service.update(id_user, data)), 200


@user_bp.delete("/<int:id_user>")
def delete_user(id_user):
    service.delete(id_user)
    return jsonify({"message": f"Usuario {id_user} eliminado."}), 200
