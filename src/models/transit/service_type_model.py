from src.utils.validators import Validators

class ServiceTypeModel:

    def __init__(self, id_service_type=None, name_service_type="", state_service_type=True):
        self.set_id_service_type(id_service_type)
        self.set_name_service_type(name_service_type)
        self.set_state_service_type(state_service_type)

    def get_id_service_type(self): return self.__id_service_type
    def get_name_service_type(self): return self.__name_service_type
    def get_state_service_type(self): return self.__state_service_type

    @Validators.integer(min_value=1, required=False)
    def set_id_service_type(self, value): self.__id_service_type = value

    @Validators.string(max_length=50, required=True)
    def set_name_service_type(self, value): self.__name_service_type = value

    @Validators.boolean(required=True)
    def set_state_service_type(self, value): self.__state_service_type = value

    def to_dict(self):
        return {
            "id_service_type": self.__id_service_type,
            "name_service_type": self.__name_service_type,
            "state_service_type": self.__state_service_type
        }