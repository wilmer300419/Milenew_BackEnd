from src.utils.validators import Validators

class ServiceTypeRouteModel:

    def __init__(self, id_route_fk, id_service_type_fk):
        self.set_id_route_fk(id_route_fk)
        self.set_id_service_type_fk(id_service_type_fk)

    def get_id_route_fk(self): return self.__id_route_fk
    def get_id_service_type_fk(self): return self.__id_service_type_fk

    @Validators.integer(min_value=1, required=True)
    def set_id_route_fk(self, value): self.__id_route_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_service_type_fk(self, value): self.__id_service_type_fk = value

    def to_dict(self):
        return {
            "id_route_fk": self.__id_route_fk,
            "id_service_type_fk": self.__id_service_type_fk
        }