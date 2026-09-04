from src.utils.validators import Validators

class RouteModel:

    def __init__(self, id_schedule_fk, code_route, id_route=None, description_route=None, state_route=True):
        self.set_id_route(id_route)
        self.set_id_schedule_fk(id_schedule_fk)
        self.set_code_route(code_route)
        self.set_description_route(description_route)
        self.set_state_route(state_route)

    def get_id_route(self): return self.__id_route
    def get_id_schedule_fk(self): return self.__id_schedule_fk
    def get_code_route(self): return self.__code_route
    def get_description_route(self): return self.__description_route
    def get_state_route(self): return self.__state_route

    @Validators.integer(min_value=1, required=False)
    def set_id_route(self, value): self.__id_route = value

    @Validators.integer(min_value=1, required=True)
    def set_id_schedule_fk(self, value): self.__id_schedule_fk = value

    @Validators.string(max_length=20, required=True)
    def set_code_route(self, value): self.__code_route = value

    @Validators.string(max_length=200, required=False)
    def set_description_route(self, value): self.__description_route = value

    @Validators.boolean(required=True)
    def set_state_route(self, value): self.__state_route = value

    def to_dict(self):
        return {
            "id_route": self.__id_route,
            "id_schedule_fk": self.__id_schedule_fk,
            "code_route": self.__code_route,
            "description_route": self.__description_route,
            "state_route": self.__state_route
        }