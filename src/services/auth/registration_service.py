"""
Operaciones MULTITABLA (todo o nada, en una sola transaccion).

    register_user      -> person + app_user
    register_employee  -> person + app_user + employee
    register_passenger -> person + app_user + passenger

Flujo de cada registro:
    1. Validar TODOS los bloques con los modelos de dominio ANTES de tocar la DB.
    2. Abrir un UnitOfWork (una conexion = una transaccion).
    3. Insertar cada tabla con su stored procedure, en orden de dependencias.
       Como los sp_Insert_* no devuelven el id, se recupera dentro de la MISMA
       transaccion via sp_GetAll_* filtrando por un campo UNIQUE
       (num_doc_person para person, username para app_user).
    4. Si algo falla -> rollback de todo. Si todo sale bien -> commit.

Cuerpo esperado (JSON):
    {
      "person":   { id_doc_type_fk, num_doc_person, first_name_person,
                    first_last_name_person, ...opcionales },
      "user":     { id_rol_fk, username, password },
      "employee": { id_employee_position_fk, id_employee_area_fk, working_hours }  <- solo empleado
    }
"""

from datetime import date

import psycopg2
from werkzeug.security import generate_password_hash

from src.database.unit_of_work import UnitOfWork
from src.models.auth import PersonModel, AppUserModel
from src.models.employees import EmployeeModel
from src.models.ticketing import PassengerModel
from src.services.auth.person_repository import PersonRepository
from src.services.auth.app_user_repository import AppUserRepository
from src.services.employees.employee_repository import EmployeeRepository
from src.services.ticketing.passenger_repository import PassengerRepository
from src.utils.errors import ConflictError

# Id ficticio usado SOLO para validar los modelos antes de insertar; el FK real
# se asigna despues, cuando la tabla padre ya existe dentro de la transaccion.
_PLACEHOLDER_ID = 1


class RegistrationService:
    def __init__(self):
        self.persons = PersonRepository()
        self.users = AppUserRepository()
        self.employees = EmployeeRepository()
        self.passengers = PassengerRepository()

    # ------------------------------------------------------------------ #
    # API publica
    # ------------------------------------------------------------------ #
    def register_user(self, data):
        person, user_block = self._validate_base(data)

        def work(conn):
            created_person, created_user = self._create_person_and_user(person, user_block, conn)
            return {"person": created_person, "user": self._public(created_user)}

        return self._run(work)

    def register_employee(self, data):
        person, user_block = self._validate_base(data)
        emp_block = self._section(data, "employee")
        self._build_employee(emp_block, _PLACEHOLDER_ID)  # validacion previa

        def work(conn):
            created_person, created_user = self._create_person_and_user(person, user_block, conn)
            employee = self._build_employee(emp_block, created_user["id_user"])
            self.employees.create(employee.to_dict(), conn=conn)
            created_employee = self._require(
                self.employees.find_by_user(created_user["id_user"], conn=conn), "employee"
            )
            return {
                "person": created_person,
                "user": self._public(created_user),
                "employee": created_employee,
            }

        return self._run(work)

    def register_passenger(self, data):
        person, user_block = self._validate_base(data)

        def work(conn):
            created_person, created_user = self._create_person_and_user(person, user_block, conn)
            passenger = PassengerModel(id_user_fk=created_user["id_user"])
            self.passengers.create(passenger.to_dict(), conn=conn)
            created_passenger = self._require(
                self.passengers.find_by_user(created_user["id_user"], conn=conn), "passenger"
            )
            return {
                "person": created_person,
                "user": self._public(created_user),
                "passenger": created_passenger,
            }

        return self._run(work)

    # ------------------------------------------------------------------ #
    # Pasos compartidos
    # ------------------------------------------------------------------ #
    def _create_person_and_user(self, person, user_block, conn):
        # 1) person
        self.persons.create(person.to_dict(), conn=conn)
        created_person = self._require(
            self.persons.find_by_num_doc(person.get_num_doc_person(), conn=conn), "person"
        )

        # 2) app_user (ahora si con el id_person real)
        user = self._build_user(user_block, created_person["id_person"])
        user_data = user.to_dict()  # to_dict no incluye password por diseno
        user_data["password"] = generate_password_hash(user.get_password())
        self.users.create(user_data, conn=conn)
        created_user = self._require(
            self.users.find_by_username(user.get_username(), conn=conn), "user"
        )
        return created_person, created_user

    @staticmethod
    def _run(work):
        """Ejecuta `work(conn)` en un UnitOfWork y traduce errores de la DB."""
        try:
            with UnitOfWork() as conn:
                return work(conn)
        except psycopg2.errors.UniqueViolation:
            raise ConflictError("Ya existe un registro con ese documento, email o username.")
        except psycopg2.errors.ForeignKeyViolation:
            raise ValueError(
                "Alguna referencia no existe (tipo de documento, rol, cargo o area)."
            )

    # ------------------------------------------------------------------ #
    # Validacion / construccion de modelos
    # ------------------------------------------------------------------ #
    def _validate_base(self, data):
        person_block = self._section(data, "person")
        user_block = self._section(data, "user")
        person = self._build_person(person_block)
        self._build_user(user_block, _PLACEHOLDER_ID)  # valida campos de usuario
        return person, user_block

    @staticmethod
    def _section(data, key):
        block = (data or {}).get(key)
        if not isinstance(block, dict):
            raise ValueError(f"Falta el bloque '{key}' en el cuerpo de la peticion.")
        return block

    @staticmethod
    def _parse_date(value):
        if value in (None, ""):
            return None
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError("birthdate_person debe tener el formato AAAA-MM-DD.")

    def _build_person(self, p):
        return PersonModel(
            id_doc_type_fk=p.get("id_doc_type_fk"),
            num_doc_person=p.get("num_doc_person"),
            first_name_person=p.get("first_name_person"),
            first_last_name_person=p.get("first_last_name_person"),
            second_name_person=p.get("second_name_person"),
            second_last_name_person=p.get("second_last_name_person"),
            phone_number_person=p.get("phone_number_person"),
            birthdate_person=self._parse_date(p.get("birthdate_person")),
            email_person=p.get("email_person"),
        )

    @staticmethod
    def _build_user(u, id_person):
        return AppUserModel(
            id_person_fk=id_person,
            id_rol_fk=u.get("id_rol_fk"),
            username=u.get("username"),
            password=u.get("password"),
        )

    @staticmethod
    def _build_employee(e, id_user):
        return EmployeeModel(
            id_employee_position_fk=e.get("id_employee_position_fk"),
            id_employee_area_fk=e.get("id_employee_area_fk"),
            id_user_fk=id_user,
            working_hours=e.get("working_hours"),
        )

    @staticmethod
    def _require(row, what):
        if row is None:
            raise RuntimeError(f"No se pudo recuperar el registro de {what} recien creado.")
        return row

    @staticmethod
    def _public(row):
        row = dict(row)
        row.pop("password", None)
        return row
