"""
Horarios, tipos de servicio, sus relaciones con las rutas y la asignacion de
empleados (conductores) a los buses.

Nota: en la DB, schedule.day_type es TEXTO (VARCHAR 20, ej. "Habil", "Sabado",
"Festivo"). El modelo DayTypeModel / id_day_type_fk del backend no existe en la DB,
por eso aqui se valida contra la DB real y no contra ScheduleModel.
"""

from datetime import date

from src.services.crud_service import CrudService
from src.services.link_service import LinkService
from src.services.transit.bus_service import BusService
from src.services.transit.route_service import RouteService
from src.services.transit.schedule_repository import (
    ScheduleRepository, ServiceTypeRepository, RouteScheduleRepository, ServiceTypeRouteRepository,
)
from src.services.transit.bus_employee_repository import BusEmployeeRepository
from src.utils import payload as P
from src.utils.db_errors import translate_db_errors
from src.utils.errors import ConflictError, NotFoundError


class ScheduleService(CrudService):
    label = "el horario"

    def __init__(self):
        self.repo = ScheduleRepository()

    def validate(self, data, current=None):
        start = P.iso_time(data.get("start_time"), "start_time")
        end = P.iso_time(data.get("end_time"), "end_time")
        if end < start:
            raise ValueError("end_time no puede ser menor que start_time.")
        return {"start_time": start, "end_time": end, "day_type": P.text(data, "day_type", 20)}


class ServiceTypeService(CrudService):
    label = "el tipo de servicio"

    def __init__(self):
        self.repo = ServiceTypeRepository()

    def validate(self, data, current=None):
        return {"name_service_type": P.text(data, "name_service_type", 50)}


def route_schedules_service():
    return LinkService(RouteScheduleRepository(), RouteService(), "el horario")


def route_service_types_service():
    return LinkService(ServiceTypeRouteRepository(), RouteService(), "el tipo de servicio")


class BusEmployeeService:
    """Asignacion de empleados a un bus por fecha de servicio (AAAA-MM-DD)."""

    def __init__(self):
        self.repo = BusEmployeeRepository()
        self.buses = BusService()

    def list(self, id_bus):
        self.buses.get(id_bus)
        return self.repo.find_by_bus(id_bus)

    @translate_db_errors
    def assign(self, id_bus, data):
        self.buses.get(id_bus)
        data = data or {}
        id_employee = P.integer(data, "id_employee_fk")
        service_date = P.iso_date(data.get("service_date"), "service_date", required=False) or date.today()
        start = P.iso_time(data.get("start_time"), "start_time")
        end = P.iso_time(data.get("end_time"), "end_time", required=False)
        if end is not None and end < start:
            raise ValueError("end_time no puede ser menor que start_time.")
        if self.repo.find_assignment(id_bus, id_employee, service_date):
            raise ConflictError(f"El empleado {id_employee} ya esta asignado al bus {id_bus} el {service_date}.")
        self.repo.create({"id_bus_fk": id_bus, "id_employee_fk": id_employee,
                          "service_date": service_date, "start_time": start, "end_time": end})
        return self.repo.find_assignment(id_bus, id_employee, service_date)

    @translate_db_errors
    def update(self, id_bus, id_employee, service_date, data):
        d = P.iso_date(service_date, "service_date")
        self.buses.get(id_bus)
        current = self.repo.find_assignment(id_bus, id_employee, d)
        if current is None:
            raise NotFoundError(f"El empleado {id_employee} no esta asignado al bus {id_bus} el {d}.")
        merged = {**current, **(data or {})}
        start = P.iso_time(merged.get("start_time"), "start_time")
        end = P.iso_time(merged.get("end_time"), "end_time", required=False)
        if end is not None and end < start:
            raise ValueError("end_time no puede ser menor que start_time.")
        return self.repo.update_assignment(id_bus, id_employee, d, start, end)
