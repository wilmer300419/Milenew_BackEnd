"""
Registra en un blueprint las rutas de una relacion N:M simple:
    GET    /<int:parent_id>/<child_path>               -> listar   (logueado)
    POST   /<int:parent_id>/<child_path>               -> asociar  (admin)
    DELETE /<int:parent_id>/<child_path>/<int:child_id> -> quitar   (admin)
"""

from flask import request, jsonify

from src.security.auth_middleware import token_required
from src.security.permissions import admin_required


def register_link_routes(bp, child_path, service, label):
    name = child_path.replace("-", "_")

    @token_required
    def list_links(parent_id):
        return jsonify(service.list(parent_id)), 200

    @token_required
    @admin_required
    def add_link(parent_id):
        return jsonify(service.add(parent_id, request.get_json(silent=True))), 201

    @token_required
    @admin_required
    def remove_link(parent_id, child_id):
        service.remove(parent_id, child_id)
        return jsonify({"message": f"{label} {child_id} quitado."}), 200

    bp.add_url_rule(f"/<int:parent_id>/{child_path}", endpoint=f"list_{name}", view_func=list_links, methods=["GET"])
    bp.add_url_rule(f"/<int:parent_id>/{child_path}", endpoint=f"add_{name}", view_func=add_link, methods=["POST"])
    bp.add_url_rule(f"/<int:parent_id>/{child_path}/<int:child_id>", endpoint=f"remove_{name}",
                    view_func=remove_link, methods=["DELETE"])
