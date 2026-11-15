"""
Administracion de personas, pasajeros y empleados (CRUD con soft-delete).
Normalmente se crean juntos con los registros multitabla (/api/register/...);
estos endpoints sirven para listarlos, corregirlos o crearlos por separado.
"""

from src.models.auth import PersonModel
from src.models.employees import EmployeeModel
from src.services.crud_service import CrudService
from src.services.auth.person_repository import PersonRepository
from src.services.employees.employee_repository import EmployeeRepository
from src.services.ticketing.passenger_repository import PassengerRepository
from src.utils import payload as P
from src.utils.errors import ConflictError


class PersonService(CrudService):
    label = "la persona"

    def __init__(self):
        self.repo = PersonRepository()

    def validate(self, data, current=None):
        person = PersonModel(
            id_doc_type_fk=P.integer(data, "id_doc_type_fk"),
            num_doc_person=data.get("num_doc_person"),
            first_name_person=data.get("first_name_person"),
            first_last_name_person=data.get("first_last_name_person"),
            second_name_person=data.get("second_name_person"),
            second_last_name_person=data.get("second_last_name_person"),
            phone_number_person=data.get("phone_number_person"),
            birthdate_person=P.iso_date(data.get("birthdate_person"), "birthdate_person", required=False),
            email_person=data.get("email_person"),
        )
        d = person.to_dict()
        return {k: d[k] for k in self.repo.insert_params}


def _ensure_one_per_user(repo, id_user, current, pk, what):
    """El back asume un pasajero / un empleado por usuario: evita duplicados."""
    own_id = current[pk] if current else None
    for row in repo.find_all():
        if row.get("id_user_fk") == id_user and row.get(pk) != own_id:
            raise ConflictError(f"El usuario {id_user} ya tiene un registro de {what} ({pk} {row[pk]}).")


class PassengerService(CrudService):
    label = "el pasajero"

    def __init__(self):
        self.repo = PassengerRepository()

    def validate(self, data, current=None):
        id_user = P.integer(data, "id_user_fk")
        _ensure_one_per_user(self.repo, id_user, current, "id_passenger", "pasajero")
        return {"id_user_fk": id_user}


class EmployeeService(CrudService):
    label = "el empleado"

    def __init__(self):
        self.repo = EmployeeRepository()

    def validate(self, data, current=None):
        employee = EmployeeModel(
            id_employee_position_fk=P.integer(data, "id_employee_position_fk"),
            id_employee_area_fk=P.integer(data, "id_employee_area_fk"),
            id_user_fk=P.integer(data, "id_user_fk"),
            working_hours=P.text(data, "working_hours", 50, required=False),
        )
        _ensure_one_per_user(self.repo, employee.get_id_user_fk(), current, "id_employee", "empleado")
        d = employee.to_dict()
        return {k: d[k] for k in self.repo.insert_params}
