from src.utils.validators import Validators

class RolModel:

    def __init__(self, id_rol=None, name_rol="", description_rol=None, state_rol=True):
        self.set_id_rol(id_rol)
        self.set_name_rol(name_rol)
        self.set_description_rol(description_rol)
        self.set_state_rol(state_rol)

    def get_id_rol(self): return self.__id_rol
    def get_name_rol(self): return self.__name_rol
    def get_description_rol(self): return self.__description_rol
    def get_state_rol(self): return self.__state_rol

    @Validators.integer(min_value=1, required=False)
    def set_id_rol(self, value): self.__id_rol = value

    @Validators.string(max_length=50, required=True)
    def set_name_rol(self, value): self.__name_rol = value

    @Validators.string(max_length=200, required=False)
    def set_description_rol(self, value): self.__description_rol = value

    @Validators.boolean(required=True)
    def set_state_rol(self, value): self.__state_rol = value

    def to_dict(self):
        return {
            "id_rol": self.__id_rol,
            "name_rol": self.__name_rol,
            "description_rol": self.__description_rol,
            "state_rol": self.__state_rol
        }