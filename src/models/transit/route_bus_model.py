from src.utils.validators import Validators

class RouteBusModel:

    def __init__(self, id_route_fk, id_bus_fk):
        self.set_id_route_fk(id_route_fk)
        self.set_id_bus_fk(id_bus_fk)

    def get_id_route_fk(self): return self.__id_route_fk
    def get_id_bus_fk(self): return self.__id_bus_fk

    @Validators.integer(min_value=1, required=True)
    def set_id_route_fk(self, value): self.__id_route_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_bus_fk(self, value): self.__id_bus_fk = value

    def to_dict(self):
        return {
            "id_route_fk": self.__id_route_fk,
            "id_bus_fk": self.__id_bus_fk
        }