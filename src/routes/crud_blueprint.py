"""
Fabrica de blueprints CRUD (GET lista, GET uno, POST, PUT, DELETE).

Permisos:
    - Lecturas: segun list_access / get_access:
        "public" -> sin token
        "auth"   -> cualquier usuario logueado (por defecto)
        "admin"  -> solo administradores
        None     -> no se crea la ruta (para definirla aparte, p. ej. con control de dueno)
    - Escrituras (POST / PUT / DELETE): siempre solo administradores.
"""

from flask import Blueprint, request, jsonify

from src.security.auth_middleware import token_required
from src.security.permissions import admin_required


def _admin(f):
    return token_required(admin_required(f))


_ACCESS = {"public": lambda f: f, "auth": token_required, "admin": _admin}


def crud_blueprint(name, url_prefix, service, label, allow_delete=True,
                   list_access="auth", get_access="auth"):
    bp = Blueprint(name, __name__, url_prefix=url_prefix)

    if list_access:
        def list_all():
            return jsonify(service.list_all()), 200
        bp.add_url_rule("", endpoint="list", view_func=_ACCESS[list_access](list_all), methods=["GET"])

    if get_access:
        def get_one(item_id):
            return jsonify(service.get(item_id)), 200
        bp.add_url_rule("/<int:item_id>", endpoint="get", view_func=_ACCESS[get_access](get_one), methods=["GET"])

    def create():
        return jsonify(service.create(request.get_json(silent=True) or {})), 201
    bp.add_url_rule("", endpoint="create", view_func=_admin(create), methods=["POST"])

    def update(item_id):
        return jsonify(service.update(item_id, request.get_json(silent=True) or {})), 200
    bp.add_url_rule("/<int:item_id>", endpoint="update", view_func=_admin(update), methods=["PUT"])

    if allow_delete:
        def delete(item_id):
            service.delete(item_id)
            return jsonify({"message": f"{label} {item_id} desactivado (soft-delete)."}), 200
        bp.add_url_rule("/<int:item_id>", endpoint="delete", view_func=_admin(delete), methods=["DELETE"])

    return bp
