from src.routes.crud_blueprint import crud_blueprint
from src.services.transit.station_service import StationService, StationTypeService

station_bp = crud_blueprint("station", "/api/stations", StationService(), "Estacion")
station_type_bp = crud_blueprint("station_type", "/api/station-types", StationTypeService(), "Tipo de estacion")
