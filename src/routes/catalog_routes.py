"""Catalogos para formularios: /api/roles, /api/employee-areas, /api/employee-positions."""

from src.routes.crud_blueprint import crud_blueprint
from src.services.catalog_services import RolService, EmployeeAreaService, EmployeePositionService

rol_bp = crud_blueprint("rol", "/api/roles", RolService(), "Rol")
employee_area_bp = crud_blueprint("employee_area", "/api/employee-areas", EmployeeAreaService(), "Area")
employee_position_bp = crud_blueprint(
    "employee_position", "/api/employee-positions", EmployeePositionService(), "Cargo"
)
