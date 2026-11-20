"""
Logica de autenticacion: valida credenciales y emite el token.
Se puede iniciar sesion con username O con email (el front de Develop usa email).
El token incluye el nombre del rol, que es lo que revisan los permisos.
"""

from src.services.auth.app_user_service import AppUserService
from src.services.auth.rol_repository import RolRepository
from src.security.token_service import generate_token


class AuthService:
    def __init__(self):
        self.users = AppUserService()
        self.roles = RolRepository()

    def login(self, username, password, email=None):
        """Devuelve {token, user} si las credenciales son validas; None si no."""
        if not password or not (username or email):
            return None
        if email:
            user = self.users.verify_credentials_by_email(email, password)
        else:
            user = self.users.verify_credentials(username, password)
        if user is None:
            return None

        rol = self.roles.find_by_id(user["id_rol_fk"])
        user = {**user, "name_rol": rol["name_rol"] if rol else None}
        return {"token": generate_token(user), "user": user}
