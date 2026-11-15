"""
Horarios, tipos de servicio, horarios/servicios de una ruta y empleados de un bus.
Lectura: cualquier usuario logueado · Escritura: solo administradores.
"""

from flask import Blueprint, request, jsonify

from src.routes.crud_blueprint import crud_blueprint
from src.routes.link_routes import register_link_routes
from src.security.auth_middleware import token_required
from src.security.permissions import admin_required
from src.services.transit.schedule_service import (
    ScheduleService, ServiceTypeService, BusEmployeeService,
    route_schedules_service, route_service_types_service,
)

# /api/schedules  { start_time "HH:MM", end_time "HH:MM", day_type (texto, ej. "Habil") }
schedule_bp = crud_blueprint("schedule", "/api/schedules", ScheduleService(), "Horario")
# /api/service-types  { name_service_type }
service_type_bp = crud_blueprint("service_type", "/api/service-types", ServiceTypeService(), "Tipo de servicio")

# /api/routes/<id>/schedules      body POST: { id_schedule_fk }
# /api/routes/<id>/service-types  body POST: { id_service_type_fk }
route_links_bp = Blueprint("route_links", __name__, url_prefix="/api/routes")
register_link_routes(route_links_bp, "schedules", route_schedules_service(), "Horario")
register_link_routes(route_links_bp, "service-types", route_service_types_service(), "Tipo de servicio")

# /api/buses/<id>/employees  (asignacion de conductores/empleados por fecha)
bus_employee_bp = Blueprint("bus_employee", __name__, url_prefix="/api/buses")
bus_employees = BusEmployeeService()


@bus_employee_bp.get("/<int:id_bus>/employees")
@token_required
def list_bus_employees(id_bus):
    return jsonify(bus_employees.list(id_bus)), 200


@bus_employee_bp.post("/<int:id_bus>/employees")
@token_required
@admin_required
def assign_bus_employee(id_bus):
    """Body: { id_employee_fk, start_time, end_time?, service_date? (AAAA-MM-DD, por defecto hoy) }"""
    return jsonify(bus_employees.assign(id_bus, request.get_json(silent=True))), 201


@bus_employee_bp.put("/<int:id_bus>/employees/<int:id_employee>/<service_date>")
@token_required
@admin_required
def update_bus_employee(id_bus, id_employee, service_date):
    """Body: { start_time?, end_time? }  (la DB no permite quitar una asignacion)"""
    return jsonify(bus_employees.update(id_bus, id_employee, service_date, request.get_json(silent=True))), 200
