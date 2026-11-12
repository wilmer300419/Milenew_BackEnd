"""
Registros MULTITABLA (todo o nada). Cada endpoint crea varias filas en una
sola transaccion; si un paso falla no queda nada a medias.
"""

from flask import Blueprint, request, jsonify
from src.services.auth.registration_service import RegistrationService
from src.security.auth_middleware import token_required

registration_bp = Blueprint("registration", __name__, url_prefix="/api/register")
service = RegistrationService()


@registration_bp.post("/user")
@token_required
def register_user():
    """person + app_user"""
    return jsonify(service.register_user(request.get_json(silent=True))), 201


@registration_bp.post("/employee")
@token_required
def register_employee():
    """person + app_user + employee"""
    return jsonify(service.register_employee(request.get_json(silent=True))), 201


@registration_bp.post("/passenger")
@token_required
def register_passenger():
    """person + app_user + passenger"""
    return jsonify(service.register_passenger(request.get_json(silent=True))), 201
