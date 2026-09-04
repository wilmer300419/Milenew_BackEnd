from src.utils.validators import Validators

class BusModel:

    def __init__(self, id_bus_type_fk, code_bus, plate_bus, id_bus=None, state_bus=True):
        self.set_id_bus(id_bus)
        self.set_id_bus_type_fk(id_bus_type_fk)
        self.set_code_bus(code_bus)
        self.set_plate_bus(plate_bus)
        self.set_state_bus(state_bus)

    def get_id_bus(self): return self.__id_bus
    def get_id_bus_type_fk(self): return self.__id_bus_type_fk
    def get_code_bus(self): return self.__code_bus
    def get_plate_bus(self): return self.__plate_bus
    def get_state_bus(self): return self.__state_bus

    @Validators.integer(min_value=1, required=False)
    def set_id_bus(self, value): self.__id_bus = value

    @Validators.integer(min_value=1, required=True)
    def set_id_bus_type_fk(self, value): self.__id_bus_type_fk = value

    @Validators.string(max_length=20, required=True)
    def set_code_bus(self, value): self.__code_bus = value

    @Validators.string(max_length=10, required=True)
    def set_plate_bus(self, value): self.__plate_bus = value

    @Validators.boolean(required=True)
    def set_state_bus(self, value): self.__state_bus = value

    def to_dict(self):
        return {
            "id_bus": self.__id_bus,
            "id_bus_type_fk": self.__id_bus_type_fk,
            "code_bus": self.__code_bus,
            "plate_bus": self.__plate_bus,
            "state_bus": self.__state_bus
        }