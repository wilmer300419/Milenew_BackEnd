from src.utils.validators import Validators

class StationModel:

    def __init__(self, id_station_type_fk, name_station, id_station=None, address_station=None,
                 latitude_station=None, longitude_station=None, state_station=True):
        self.set_id_station(id_station)
        self.set_id_station_type_fk(id_station_type_fk)
        self.set_name_station(name_station)
        self.set_address_station(address_station)
        self.set_latitude_station(latitude_station)
        self.set_longitude_station(longitude_station)
        self.set_state_station(state_station)

    def get_id_station(self): return self.__id_station
    def get_id_station_type_fk(self): return self.__id_station_type_fk
    def get_name_station(self): return self.__name_station
    def get_address_station(self): return self.__address_station
    def get_latitude_station(self): return self.__latitude_station
    def get_longitude_station(self): return self.__longitude_station
    def get_state_station(self): return self.__state_station

    @Validators.integer(min_value=1, required=False)
    def set_id_station(self, value): self.__id_station = value

    @Validators.integer(min_value=1, required=True)
    def set_id_station_type_fk(self, value): self.__id_station_type_fk = value

    @Validators.string(max_length=100, required=True)
    def set_name_station(self, value): self.__name_station = value

    @Validators.string(max_length=150, required=False)
    def set_address_station(self, value): self.__address_station = value

    @Validators.decimal(required=False)
    def set_latitude_station(self, value): self.__latitude_station = value

    @Validators.decimal(required=False)
    def set_longitude_station(self, value): self.__longitude_station = value

    @Validators.boolean(required=True)
    def set_state_station(self, value): self.__state_station = value

    def to_dict(self):
        return {
            "id_station": self.__id_station,
            "id_station_type_fk": self.__id_station_type_fk,
            "name_station": self.__name_station,
            "address_station": self.__address_station,
            "latitude_station": float(self.__latitude_station) if self.__latitude_station is not None else None,
            "longitude_station": float(self.__longitude_station) if self.__longitude_station is not None else None,
            "state_station": self.__state_station
        }