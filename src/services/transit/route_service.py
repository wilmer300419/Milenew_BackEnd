import psycopg2

from src.database.unit_of_work import UnitOfWork
from src.services.crud_service import CrudService
from src.services.transit.route_repository import RouteRepository
from src.services.transit.route_station_repository import RouteStationRepository
from src.services.transit.route_bus_repository import RouteBusRepository
from src.utils import payload as P
from src.utils.db_errors import translate_db_errors
from src.utils.errors import NotFoundError, ConflictError


class RouteService(CrudService):
    label = "la ruta"

    def __init__(self):
        self.repo = RouteRepository()
        self.route_stations = RouteStationRepository()
        self.route_buses = RouteBusRepository()

    def validate(self, data, current=None):
        return {
            "code_route": P.text(data, "code_route", 20),
            "description_route": P.text(data, "description_route", 200, required=False),
        }

    # ---------------- estaciones de la ruta ----------------
    def list_stations(self, id_route):
        self.get(id_route)  # 404 si la ruta no existe
        return self.route_stations.find_by_route(id_route)

    @translate_db_errors
    def add_station(self, id_route, data):
        self.get(id_route)
        data = data or {}
        id_station = P.integer(data, "id_station_fk")
        order = P.integer(data, "order_route_station")

        existing = self.route_stations.find_pair(id_route, id_station)
        if existing and existing.get("state_route_station"):
            raise ConflictError(f"La estacion {id_station} ya esta en la ruta {id_route}.")

        try:
            if existing:
                # Estaba retirada (soft-delete): se reactiva con el nuevo orden en
                # una sola transaccion, en vez de intentar insertarla de nuevo.
                with UnitOfWork() as conn:
                    self.route_stations.update_order(id_route, id_station, order, conn=conn)
                    self.route_stations.set_active(id_route, id_station, True, conn=conn)
            else:
                self.route_stations.create({
                    "id_route_fk": id_route, "id_station_fk": id_station, "order_route_station": order
                })
        except psycopg2.errors.UniqueViolation:
            raise ConflictError(self._order_taken_message(id_route, order))

        return self.route_stations.find_pair(id_route, id_station)

    @translate_db_errors
    def update_station_order(self, id_route, id_station, data):
        self._require_station(id_route, id_station)
        order = P.integer(data or {}, "order_route_station")
        try:
            return self.route_stations.update_order(id_route, id_station, order)
        except psycopg2.errors.UniqueViolation:
            raise ConflictError(self._order_taken_message(id_route, order))

    @staticmethod
    def _order_taken_message(id_route, order):
        # En la DB el orden es UNICO por ruta, contando tambien las estaciones retiradas.
        return (f"El orden {order} ya esta ocupado en la ruta {id_route} "
                "(tambien cuentan las estaciones retiradas).")

    @translate_db_errors
    def remove_station(self, id_route, id_station):
        self._require_station(id_route, id_station)
        return self.route_stations.remove(id_route, id_station)

    def _require_station(self, id_route, id_station):
        self.get(id_route)
        row = self.route_stations.find_pair(id_route, id_station)
        # sp_GetById_Route_Station no filtra por estado: una estacion retirada cuenta como "no esta".
        if row is None or not row.get("state_route_station"):
            raise NotFoundError(f"La estacion {id_station} no pertenece a la ruta {id_route}.")
        return row

    # ---------------- buses asignados a la ruta ----------------
    def list_buses(self, id_route):
        self.get(id_route)
        return self.route_buses.find_by_route(id_route)

    @translate_db_errors
    def assign_bus(self, id_route, data):
        self.get(id_route)
        data = data or {}
        id_bus = P.integer(data, "id_bus_fk")
        service_date = P.iso_date(data.get("service_date"), "service_date", required=False)
        start = P.iso_time(data.get("start_time"), "start_time")
        end = P.iso_time(data.get("end_time"), "end_time", required=False)
        if end is not None and end < start:
            raise ValueError("end_time no puede ser menor que start_time.")
        self.route_buses.create({
            "id_route_fk": id_route, "id_bus_fk": id_bus,
            "service_date": service_date, "start_time": start, "end_time": end,
        })
        from datetime import date
        return self.route_buses.find_assignment(id_route, id_bus, service_date or date.today())

    @translate_db_errors
    def update_bus_assignment(self, id_route, id_bus, service_date, data):
        d = P.iso_date(service_date, "service_date")
        current = self._require_assignment(id_route, id_bus, d)
        data = {**current, **(data or {})}
        start = P.iso_time(data.get("start_time"), "start_time")
        end = P.iso_time(data.get("end_time"), "end_time", required=False)
        if end is not None and end < start:
            raise ValueError("end_time no puede ser menor que start_time.")
        return self.route_buses.update_assignment(id_route, id_bus, d, start, end)

    @translate_db_errors
    def remove_bus_assignment(self, id_route, id_bus, service_date):
        d = P.iso_date(service_date, "service_date")
        self._require_assignment(id_route, id_bus, d)
        return self.route_buses.remove(id_route, id_bus, d)

    def _require_assignment(self, id_route, id_bus, d):
        self.get(id_route)
        row = self.route_buses.find_assignment(id_route, id_bus, d)
        if row is None:
            raise NotFoundError(f"El bus {id_bus} no esta asignado a la ruta {id_route} el {d}.")
        return row
