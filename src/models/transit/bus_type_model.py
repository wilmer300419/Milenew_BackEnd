from src.utils.validators import Validators

class BusTypeModel:

    def __init__(self, capacity_bus_type, id_bus_type=None, name_bus_type="", state_bus_type=True):
        self.set_id_bus_type(id_bus_type)
        self.set_name_bus_type(name_bus_type)
        self.set_capacity_bus_type(capacity_bus_type)
        self.set_state_bus_type(state_bus_type)

    def get_id_bus_type(self): return self.__id_bus_type
    def get_name_bus_type(self): return self.__name_bus_type
    def get_capacity_bus_type(self): return self.__capacity_bus_type
    def get_state_bus_type(self): return self.__state_bus_type

    @Validators.integer(min_value=1, required=False)
    def set_id_bus_type(self, value): self.__id_bus_type = value

    @Validators.string(max_length=50, required=True)
    def set_name_bus_type(self, value): self.__name_bus_type = value

    @Validators.integer(min_value=1, required=True)
    def set_capacity_bus_type(self, value): self.__capacity_bus_type = value

    @Validators.boolean(required=True)
    def set_state_bus_type(self, value): self.__state_bus_type = value

    def to_dict(self):
        return {
            "id_bus_type": self.__id_bus_type,
            "name_bus_type": self.__name_bus_type,
            "capacity_bus_type": self.__capacity_bus_type,
            "state_bus_type": self.__state_bus_type
        }