from flask import Blueprint, request, jsonify, g
from src.services.auth.auth_service import AuthService
from src.services.auth.registration_service import RegistrationService
from src.security.auth_middleware import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
service = AuthService()
registration = RegistrationService()


@auth_bp.post("/login")
def login():
    # Acepta { username, password } o { email, password }.
    data = request.get_json(silent=True) or {}
    result = service.login(data.get("username"), data.get("password"), email=data.get("email"))
    if result is None:
        return jsonify({
            "error": "invalid_credentials",
            "message": "Usuario o contrasena incorrectos."
        }), 401
    return jsonify(result), 200


@auth_bp.post("/register")
def register():
    """
    Auto-registro PUBLICO de pasajero (person + app_user + passenger).
    Body: { person: {...}, user: { username, password } }  (el rol lo pone el back)
    """
    return jsonify(registration.register_public_passenger(request.get_json(silent=True))), 201


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
