"""
"Mi cuenta" del usuario logueado. El usuario sale del token, no de la URL,
asi nadie puede ver ni editar la cuenta de otro cambiando un id.
"""

from flask import Blueprint, request, jsonify, g

from src.security.auth_middleware import token_required
from src.services.auth.profile_service import ProfileService

profile_bp = Blueprint("profile", __name__, url_prefix="/api/users/me")
service = ProfileService()


def _current_user_id():
    return int(g.current_user["sub"])


@profile_bp.get("")
@token_required
def get_me():
    return jsonify(service.get_me(_current_user_id())), 200


@profile_bp.put("")
@token_required
def update_me():
    return jsonify(service.update_me(_current_user_id(), request.get_json(silent=True))), 200


@profile_bp.put("/password")
@token_required
def change_password():
    return jsonify(service.change_password(_current_user_id(), request.get_json(silent=True))), 200


@profile_bp.get("/cards")
@token_required
def my_cards():
    return jsonify(service.my_cards(_current_user_id())), 200
