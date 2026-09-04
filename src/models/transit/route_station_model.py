from src.utils.validators import Validators

class RouteStationModel:

    def __init__(self, id_route_fk, id_station_fk, state_route_station=True):
        self.set_id_route_fk(id_route_fk)
        self.set_id_station_fk(id_station_fk)
        self.set_state_route_station(state_route_station)

    def get_id_route_fk(self): return self.__id_route_fk
    def get_id_station_fk(self): return self.__id_station_fk
    def get_state_route_station(self): return self.__state_route_station

    @Validators.integer(min_value=1, required=True)
    def set_id_route_fk(self, value): self.__id_route_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_station_fk(self, value): self.__id_station_fk = value

    @Validators.boolean(required=True)
    def set_state_route_station(self, value): self.__state_route_station = value

    def to_dict(self):
        return {
            "id_route_fk": self.__id_route_fk,
            "id_station_fk": self.__id_station_fk,
            "state_route_station": self.__state_route_station
        }