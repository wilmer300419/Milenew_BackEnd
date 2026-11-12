"""
Decorador de autenticacion. Protege una ruta exigiendo un token JWT valido
en la cabecera Authorization: Bearer <token>. Si falta o es invalido -> 401.
El usuario decodificado queda disponible en flask.g.current_user.
"""

from functools import wraps
from flask import request, jsonify, g
import jwt

from src.security.token_service import decode_token


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({
                "error": "unauthorized",
                "message": "Falta el token. Envia 'Authorization: Bearer <token>'."
            }), 401

        token = header.split(" ", 1)[1].strip()
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token_expired", "message": "El token expiro, inicia sesion de nuevo."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid_token", "message": "Token invalido."}), 401

        g.current_user = payload
        return f(*args, **kwargs)

    return wrapper
