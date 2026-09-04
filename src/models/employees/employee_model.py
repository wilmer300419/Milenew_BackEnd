from src.utils.validators import Validators

class EmployeeModel:

    def __init__(self, id_employee_position_fk, id_employee_area_fk, id_user_fk,
                 id_employee=None, working_hours=None, state_employee=True):
        self.set_id_employee(id_employee)
        self.set_id_employee_position_fk(id_employee_position_fk)
        self.set_id_employee_area_fk(id_employee_area_fk)
        self.set_id_user_fk(id_user_fk)
        self.set_working_hours(working_hours)
        self.set_state_employee(state_employee)

    def get_id_employee(self): return self.__id_employee
    def get_id_employee_position_fk(self): return self.__id_employee_position_fk
    def get_id_employee_area_fk(self): return self.__id_employee_area_fk
    def get_id_user_fk(self): return self.__id_user_fk
    def get_working_hours(self): return self.__working_hours
    def get_state_employee(self): return self.__state_employee

    @Validators.integer(min_value=1, required=False)
    def set_id_employee(self, value): self.__id_employee = value

    @Validators.integer(min_value=1, required=True)
    def set_id_employee_position_fk(self, value): self.__id_employee_position_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_employee_area_fk(self, value): self.__id_employee_area_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_user_fk(self, value): self.__id_user_fk = value

    @Validators.string(max_length=50, required=False)
    def set_working_hours(self, value): self.__working_hours = value

    @Validators.boolean(required=True)
    def set_state_employee(self, value): self.__state_employee = value

    def to_dict(self):
        return {
            "id_employee": self.__id_employee,
            "id_employee_position_fk": self.__id_employee_position_fk,
            "id_employee_area_fk": self.__id_employee_area_fk,
            "id_user_fk": self.__id_user_fk,
            "working_hours": self.__working_hours,
            "state_employee": self.__state_employee
        }