from src.utils.validators import Validators

class BusEmployeeModel:

    def __init__(self, id_bus_fk, id_employee_fk):
        self.set_id_bus_fk(id_bus_fk)
        self.set_id_employee_fk(id_employee_fk)

    def get_id_bus_fk(self): return self.__id_bus_fk
    def get_id_employee_fk(self): return self.__id_employee_fk

    @Validators.integer(min_value=1, required=True)
    def set_id_bus_fk(self, value): self.__id_bus_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_employee_fk(self, value): self.__id_employee_fk = value

    def to_dict(self):
        return {
            "id_bus_fk": self.__id_bus_fk,
            "id_employee_fk": self.__id_employee_fk
        }