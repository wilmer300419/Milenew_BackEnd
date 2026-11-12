from flask import Blueprint, request, jsonify, g
from src.services.auth.auth_service import AuthService
from src.security.auth_middleware import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
service = AuthService()


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    result = service.login(data.get("username"), data.get("password"))
    if result is None:
        return jsonify({
            "error": "invalid_credentials",
            "message": "Usuario o contrasena incorrectos."
        }), 401
    return jsonify(result), 200


@auth_bp.get("/me")
@token_required
def me():
    # g.current_user viene del token ya validado por el decorador
    return jsonify(g.current_user), 200


@auth_bp.post("/logout")
@token_required
def logout():
    # Con JWT stateless, cerrar sesion = que el cliente descarte el token.
    return jsonify({"message": "Sesion cerrada. Descarta el token en el cliente."}), 200
