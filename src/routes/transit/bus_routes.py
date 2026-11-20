from src.routes.crud_blueprint import crud_blueprint
from src.services.transit.bus_service import BusService, BusTypeService

bus_bp = crud_blueprint("bus", "/api/buses", BusService(), "Bus")
bus_type_bp = crud_blueprint("bus_type", "/api/bus-types", BusTypeService(), "Tipo de bus")
