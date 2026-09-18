from flask import Blueprint, request, jsonify
from src.services.auth.rol_service import RolService

rol_bp = Blueprint("rol", __name__, url_prefix="/api/roles")
service = RolService()


@rol_bp.get("")
def list_roles():
    return jsonify(service.list_all()), 200


@rol_bp.get("/<int:id_rol>")
def get_rol(id_rol):
    return jsonify(service.get(id_rol)), 200


@rol_bp.post("")
def create_rol():
    data = request.get_json(silent=True) or {}
    return jsonify(service.create(data)), 201


@rol_bp.put("/<int:id_rol>")
def update_rol(id_rol):
    data = request.get_json(silent=True) or {}
    return jsonify(service.update(id_rol, data)), 200


@rol_bp.delete("/<int:id_rol>")
def delete_rol(id_rol):
    service.delete(id_rol)
    return jsonify({"message": f"Rol {id_rol} eliminado."}), 200
