"""
Permisos, permisos de un rol y administracion de personas, pasajeros y empleados.

    /api/permissions               CRUD     (lectura: logueado · escritura: admin)
    /api/roles/<id>/permissions    listar / asociar { id_permission_fk } / quitar
    /api/persons                   CRUD     (todo solo admin: datos personales)
    /api/passengers                CRUD     (todo solo admin)
    /api/employees                 CRUD     (todo solo admin)
"""

from flask import Blueprint

from src.routes.crud_blueprint import crud_blueprint
from src.routes.link_routes import register_link_routes
from src.services.crud_service import CrudService
from src.services.link_service import LinkService
from src.services.catalog_services import RolService
from src.services.auth.permission_repository import PermissionRepository, RolPermissionRepository
from src.services.people_services import PersonService, PassengerService, EmployeeService
from src.utils import payload as P


class PermissionService(CrudService):
    label = "el permiso"

    def __init__(self):
        self.repo = PermissionRepository()

    def validate(self, data, current=None):
        return {
            "name_permission": P.text(data, "name_permission", 50),
            "description_permission": P.text(data, "description_permission", 200, required=False),
        }


permission_bp = crud_blueprint("permission", "/api/permissions", PermissionService(), "Permiso")

rol_permission_bp = Blueprint("rol_permission", __name__, url_prefix="/api/roles")
register_link_routes(rol_permission_bp, "permissions",
                     LinkService(RolPermissionRepository(), RolService(), "el permiso"), "Permiso")

person_bp = crud_blueprint("person", "/api/persons", PersonService(), "Persona",
                           list_access="admin", get_access="admin")
passenger_bp = crud_blueprint("passenger", "/api/passengers", PassengerService(), "Pasajero",
                              list_access="admin", get_access="admin")
employee_bp = crud_blueprint("employee", "/api/employees", EmployeeService(), "Empleado",
                             list_access="admin", get_access="admin")
