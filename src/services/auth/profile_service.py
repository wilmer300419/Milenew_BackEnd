"""
"Mi cuenta": operaciones sobre el usuario que esta logueado (el del token).

    get_me           -> usuario + persona (+ pasajero / empleado si aplica)
    update_me        -> actualiza los datos personales (sp_Update_Person)
    change_password  -> cambia la contrasena verificando la actual
    my_cards         -> tarjetas del pasajero asociado al usuario
"""

from werkzeug.security import check_password_hash, generate_password_hash

from src.models.auth import PersonModel
from src.services.auth.app_user_repository import AppUserRepository
from src.services.auth.person_repository import PersonRepository
from src.services.employees.employee_repository import EmployeeRepository
from src.services.ticketing.card_repository import CardRepository
from src.services.ticketing.passenger_repository import PassengerRepository
from src.utils import payload as P
from src.utils.db_errors import translate_db_errors
from src.utils.errors import NotFoundError

# Campos de persona que el propio usuario puede editar.
EDITABLE_PERSON_FIELDS = (
    "id_doc_type_fk", "num_doc_person", "first_name_person", "second_name_person",
    "first_last_name_person", "second_last_name_person", "phone_number_person",
    "birthdate_person", "email_person",
)


class ProfileService:
    def __init__(self):
        self.users = AppUserRepository()
        self.persons = PersonRepository()
        self.passengers = PassengerRepository()
        self.employees = EmployeeRepository()
        self.cards = CardRepository()

    # ------------------------------------------------------------------ #
    def get_me(self, id_user):
        user = self._active_user(id_user)
        return {
            "user": self._public(user),
            "person": self.persons.find_by_id(user["id_person_fk"]),
            "passenger": self.passengers.find_by_user(id_user),   # None si no es pasajero
            "employee": self.employees.find_by_user(id_user),     # None si no es empleado
        }

    @translate_db_errors
    def update_me(self, id_user, data):
        user = self._active_user(id_user)
        current = self.persons.find_by_id(user["id_person_fk"])
        changes = {k: v for k, v in (data or {}).items() if k in EDITABLE_PERSON_FIELDS}
        if not changes:
            raise ValueError("No se envio ningun dato de persona para actualizar.")
        merged = {**current, **changes}
        person = PersonModel(
            id_person=current["id_person"],
            id_doc_type_fk=merged.get("id_doc_type_fk"),
            num_doc_person=merged.get("num_doc_person"),
            first_name_person=merged.get("first_name_person"),
            first_last_name_person=merged.get("first_last_name_person"),
            second_name_person=merged.get("second_name_person"),
            second_last_name_person=merged.get("second_last_name_person"),
            phone_number_person=merged.get("phone_number_person"),
            birthdate_person=P.iso_date(merged.get("birthdate_person"), "birthdate_person", required=False),
            email_person=merged.get("email_person"),
        )
        self.persons.update(current["id_person"], person.to_dict())
        return self.get_me(id_user)

    @translate_db_errors
    def change_password(self, id_user, data):
        data = data or {}
        # Se aceptan ambos estilos de nombre (snake_case del back / camelCase del front).
        current_pwd = data.get("current_password") or data.get("currentPassword")
        new_pwd = data.get("new_password") or data.get("newPassword")
        if not current_pwd or not new_pwd:
            raise ValueError("Envia la contrasena actual y la nueva.")
        if not isinstance(new_pwd, str) or len(new_pwd) > 255:
            raise ValueError("La contrasena nueva no es valida.")
        if current_pwd == new_pwd:
            raise ValueError("La contrasena nueva debe ser distinta de la actual.")

        user = self._active_user(id_user)
        if not check_password_hash(user["password"], current_pwd):
            # 400 (no 401) a proposito: un 401 haria que el front cierre la sesion.
            raise ValueError("La contrasena actual no es correcta.")

        self.users.update(id_user, {
            "id_person_fk": user["id_person_fk"],
            "id_rol_fk": user["id_rol_fk"],
            "username": user["username"],
            "password": generate_password_hash(new_pwd),
        })
        return {"message": "Contrasena actualizada correctamente."}

    def my_cards(self, id_user):
        self._active_user(id_user)
        passenger = self.passengers.find_by_user(id_user)
        if passenger is None:
            return []  # el usuario no es pasajero: no tiene tarjetas
        return [c for c in self.cards.find_all() if c.get("id_passenger_fk") == passenger["id_passenger"]]

    # ------------------------------------------------------------------ #
    def _active_user(self, id_user):
        user = self.users.find_by_id(id_user)
        if user is None or not user.get("state_user", True):
            raise NotFoundError("Tu usuario no existe o esta desactivado.")
        return user

    @staticmethod
    def _public(row):
        row = dict(row)
        row.pop("password", None)
        return row
