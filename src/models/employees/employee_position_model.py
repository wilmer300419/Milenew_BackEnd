from src.utils.validators import Validators

class EmployeePositionModel:

    def __init__(self, id_employee_position=None, name_employee_position="", state_employee_position=True):
        self.set_id_employee_position(id_employee_position)
        self.set_name_employee_position(name_employee_position)
        self.set_state_employee_position(state_employee_position)

    def get_id_employee_position(self): return self.__id_employee_position
    def get_name_employee_position(self): return self.__name_employee_position
    def get_state_employee_position(self): return self.__state_employee_position

    @Validators.integer(min_value=1, required=False)
    def set_id_employee_position(self, value): self.__id_employee_position = value

    @Validators.string(max_length=50, required=True)
    def set_name_employee_position(self, value): self.__name_employee_position = value

    @Validators.boolean(required=True)
    def set_state_employee_position(self, value): self.__state_employee_position = value

    def to_dict(self):
        return {
            "id_employee_position": self.__id_employee_position,
            "name_employee_position": self.__name_employee_position,
            "state_employee_position": self.__state_employee_position
        }