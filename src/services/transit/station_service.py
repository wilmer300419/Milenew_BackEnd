from decimal import Decimal

from src.models.transit import StationModel
from src.services.crud_service import CrudService
from src.services.transit.station_repository import StationRepository
from src.services.transit.station_type_repository import StationTypeRepository
from src.utils import payload as P


class StationService(CrudService):
    label = "la estacion"

    def __init__(self):
        self.repo = StationRepository()

    def validate(self, data, current=None):
        # Primero mensajes claros por campo; luego StationModel valida el resto
        P.integer(data, "id_station_type_fk")
        P.text(data, "name_station", 100)
        st = StationModel(
            id_station_type_fk=data.get("id_station_type_fk"),
            name_station=data.get("name_station"),
            address_station=data.get("address_station"),
            latitude_station=data.get("latitude_station"),
            longitude_station=data.get("longitude_station"),
        )
        d = st.to_dict()
        lat, lon = d["latitude_station"], d["longitude_station"]
        if lat is not None and not -90 <= lat <= 90:
            raise ValueError("latitude_station debe estar entre -90 y 90.")
        if lon is not None and not -180 <= lon <= 180:
            raise ValueError("longitude_station debe estar entre -180 y 180.")
        return {k: d[k] for k in self.repo.insert_params}


class StationTypeService(CrudService):
    label = "el tipo de estacion"

    def __init__(self):
        self.repo = StationTypeRepository()

    def validate(self, data, current=None):
        return {"name_station_type": P.text(data, "name_station_type", 50)}
