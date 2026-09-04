from src.utils.validators import Validators

class StationTypeModel:

    def __init__(self, id_station_type=None, name_station_type="", state_station_type=True):
        self.set_id_station_type(id_station_type)
        self.set_name_station_type(name_station_type)
        self.set_state_station_type(state_station_type)

    def get_id_station_type(self): return self.__id_station_type
    def get_name_station_type(self): return self.__name_station_type
    def get_state_station_type(self): return self.__state_station_type

    @Validators.integer(min_value=1, required=False)
    def set_id_station_type(self, value): self.__id_station_type = value

    @Validators.string(max_length=50, required=True)
    def set_name_station_type(self, value): self.__name_station_type = value

    @Validators.boolean(required=True)
    def set_state_station_type(self, value): self.__state_station_type = value

    def to_dict(self):
        return {
            "id_station_type": self.__id_station_type,
            "name_station_type": self.__name_station_type,
            "state_station_type": self.__state_station_type
        }