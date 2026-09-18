from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

from src.models.auth import AppUserModel
from src.services.auth.app_user_repository import AppUserRepository
from src.utils.errors import NotFoundError, ConflictError


class AppUserService:
    def __init__(self):
        self.repo = AppUserRepository()

    @staticmethod
    def _public(row):
        """Nunca devolver el hash de la contrasena al exterior."""
        if row is None:
            return None
        row = dict(row)
        row.pop("password", None)
        return row

    def list_all(self):
        return [self._public(r) for r in self.repo.find_all()]

    def get(self, id_user):
        row = self.repo.find_by_id(id_user)
        if row is None:
            raise NotFoundError(f"No existe el usuario con id {id_user}.")
        return self._public(row)

    def create(self, data):
        # Validacion via el modelo (incluye que password sea obligatorio y valido)
        user = AppUserModel(
            id_person_fk=data.get("id_person_fk"),
            id_rol_fk=data.get("id_rol_fk"),
            username=data.get("username"),
            password=data.get("password"),
            state_user=data.get("state_user", True),
        )
        payload = user.to_dict()                       # no trae password (por diseno)
        payload["password"] = generate_password_hash(user.get_password())
        try:
            row = self.repo.create(payload)
        except psycopg2.errors.UniqueViolation:
            raise ConflictError(f"El username '{data.get('username')}' ya esta en uso.")
        return self._public(row)

    def update(self, id_user, data):
        current = self.repo.find_by_id(id_user)
        if current is None:
            raise NotFoundError(f"No existe el usuario con id {id_user}.")
        merged = {**current, **data}
        user = AppUserModel(
            id_user=id_user,
            id_person_fk=merged.get("id_person_fk"),
            id_rol_fk=merged.get("id_rol_fk"),
            username=merged.get("username"),
            password=merged.get("password"),
            state_user=merged.get("state_user", True),
        )
        payload = user.to_dict()
        # Solo re-hashear si llega una contrasena nueva; si no, conservar la actual
        if "password" in data and data["password"]:
            payload["password"] = generate_password_hash(data["password"])
        else:
            payload["password"] = current["password"]
        try:
            row = self.repo.update(id_user, payload)
        except psycopg2.errors.UniqueViolation:
            raise ConflictError(f"El username '{data.get('username')}' ya esta en uso.")
        return self._public(row)

    def delete(self, id_user):
        if self.repo.find_by_id(id_user) is None:
            raise NotFoundError(f"No existe el usuario con id {id_user}.")
        return self.repo.delete(id_user)

    def verify_credentials(self, username, password):
        """Util para el futuro login: valida usuario/contrasena."""
        row = self.repo.find_by_username(username)
        if row is None or not check_password_hash(row["password"], password):
            return None
        return self._public(row)
