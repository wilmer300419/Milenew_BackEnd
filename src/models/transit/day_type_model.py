from src.utils.validators import Validators

class DayTypeModel:

    def __init__(self, id_day_type=None, name_day_type="", state_day_type=True):
        self.set_id_day_type(id_day_type)
        self.set_name_day_type(name_day_type)
        self.set_state_day_type(state_day_type)

    def get_id_day_type(self): return self.__id_day_type
    def get_name_day_type(self): return self.__name_day_type
    def get_state_day_type(self): return self.__state_day_type

    @Validators.integer(min_value=1, required=False)
    def set_id_day_type(self, value): self.__id_day_type = value

    @Validators.string(max_length=50, required=True)
    def set_name_day_type(self, value): self.__name_day_type = value

    @Validators.boolean(required=True)
    def set_state_day_type(self, value): self.__state_day_type = value

    def to_dict(self):
        return {
            "id_day_type": self.__id_day_type,
            "name_day_type": self.__name_day_type,
            "state_day_type": self.__state_day_type
        }
