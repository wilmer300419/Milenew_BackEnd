"""
Catalogos que el front necesita para llenar los desplegables de los
formularios de registro: roles, areas y cargos de empleado.
Usan el CRUD generico (CrudService) y validan con los mismos largos de la DB.
"""

from src.services.crud_service import CrudService
from src.services.auth.rol_repository import RolRepository
from src.services.employees.employee_catalog_repository import (
    EmployeeAreaRepository, EmployeePositionRepository,
)
from src.utils import payload as P


class RolService(CrudService):
    label = "el rol"

    def __init__(self):
        self.repo = RolRepository()

    def validate(self, data, current=None):
        return {
            "name_rol": P.text(data, "name_rol", 50),
            "description_rol": P.text(data, "description_rol", 200, required=False),
        }


class EmployeeAreaService(CrudService):
    label = "el area"

    def __init__(self):
        self.repo = EmployeeAreaRepository()

    def validate(self, data, current=None):
        return {
            "name_employee_area": P.text(data, "name_employee_area", 50),
            "place_employee_area": P.text(data, "place_employee_area", 100, required=False),
        }


class EmployeePositionService(CrudService):
    label = "el cargo"

    def __init__(self):
        self.repo = EmployeePositionRepository()

    def validate(self, data, current=None):
        return {"name_employee_position": P.text(data, "name_employee_position", 50)}
