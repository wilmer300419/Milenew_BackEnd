from src.models.transit import BusModel
from src.services.crud_service import CrudService
from src.services.transit.bus_repository import BusRepository, BusTypeRepository
from src.utils import payload as P


class BusService(CrudService):
    label = "el bus"

    def __init__(self):
        self.repo = BusRepository()

    def validate(self, data, current=None):
        P.integer(data, "id_bus_type_fk")
        P.text(data, "code_bus", 20)
        P.text(data, "plate_bus", 10)
        bus = BusModel(
            id_bus_type_fk=data.get("id_bus_type_fk"),
            code_bus=data.get("code_bus"),
            plate_bus=data.get("plate_bus"),
        )
        d = bus.to_dict()
        return {k: d[k] for k in self.repo.insert_params}


class BusTypeService(CrudService):
    label = "el tipo de bus"

    def __init__(self):
        self.repo = BusTypeRepository()

    def validate(self, data, current=None):
        return {
            "name_bus_type": P.text(data, "name_bus_type", 50),
            "capacity_bus_type": P.integer(data, "capacity_bus_type", min_value=1),
        }
