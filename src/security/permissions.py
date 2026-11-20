"""
Permisos por rol.

    - Los roles con permisos de administrador se configuran en el .env:
          ADMIN_ROLES=Administrador,Taquillero
      (por defecto solo "Administrador"; no distingue mayusculas).
    - El nombre del rol viaja dentro del token (claim "rol"), asi no hay que
      consultar la DB en cada peticion.

Uso (siempre DESPUES de @token_required, que es quien carga g.current_user):
    @bp.post("")
    @token_required
    @admin_required
    def crear(): ...
"""

from functools import wraps

from decouple import config, Csv
from flask import g, jsonify

ADMIN_ROLES = {r.strip().lower() for r in config("ADMIN_ROLES", default="Administrador", cast=Csv()) if r.strip()}


def is_admin(user=None):
    user = user if user is not None else (getattr(g, "current_user", None) or {})
    return (user.get("rol") or "").strip().lower() in ADMIN_ROLES


def current_user_id():
    return int(g.current_user["sub"])


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_admin():
            return jsonify({
                "error": "forbidden",
                "message": "No tienes permisos para realizar esta accion."
            }), 403
        return f(*args, **kwargs)
    return wrapper
