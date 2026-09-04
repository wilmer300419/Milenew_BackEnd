from src.utils.validators import Validators

class EmployeeAreaModel:

    def __init__(self, id_employee_area=None, name_employee_area="", place_employee_area=None, state_employee_area=True):
        self.set_id_employee_area(id_employee_area)
        self.set_name_employee_area(name_employee_area)
        self.set_place_employee_area(place_employee_area)
        self.set_state_employee_area(state_employee_area)

    def get_id_employee_area(self): return self.__id_employee_area
    def get_name_employee_area(self): return self.__name_employee_area
    def get_place_employee_area(self): return self.__place_employee_area
    def get_state_employee_area(self): return self.__state_employee_area

    @Validators.integer(min_value=1, required=False)
    def set_id_employee_area(self, value): self.__id_employee_area = value

    @Validators.string(max_length=50, required=True)
    def set_name_employee_area(self, value): self.__name_employee_area = value

    @Validators.string(max_length=100, required=False)
    def set_place_employee_area(self, value): self.__place_employee_area = value

    @Validators.boolean(required=True)
    def set_state_employee_area(self, value): self.__state_employee_area = value

    def to_dict(self):
        return {
            "id_employee_area": self.__id_employee_area,
            "name_employee_area": self.__name_employee_area,
            "place_employee_area": self.__place_employee_area,
            "state_employee_area": self.__state_employee_area
        }