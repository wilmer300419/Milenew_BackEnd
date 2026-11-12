"""
Logica de autenticacion: valida credenciales y emite el token.
Reutiliza AppUserService.verify_credentials (que compara contra el hash guardado).
"""

from src.services.auth.app_user_service import AppUserService
from src.security.token_service import generate_token


class AuthService:
    def __init__(self):
        self.users = AppUserService()

    def login(self, username, password):
        """Devuelve {token, user} si las credenciales son validas; None si no."""
        if not username or not password:
            return None
        user = self.users.verify_credentials(username, password)
        if user is None:
            return None
        return {"token": generate_token(user), "user": user}
