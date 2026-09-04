from src.utils.validators import Validators

class PassengerModel:

    def __init__(self, id_user_fk, id_passenger=None, state_passenger=True):
        self.set_id_passenger(id_passenger)
        self.set_id_user_fk(id_user_fk)
        self.set_state_passenger(state_passenger)

    def get_id_passenger(self): return self.__id_passenger
    def get_id_user_fk(self): return self.__id_user_fk
    def get_state_passenger(self): return self.__state_passenger

    @Validators.integer(min_value=1, required=False)
    def set_id_passenger(self, value): self.__id_passenger = value

    @Validators.integer(min_value=1, required=True)
    def set_id_user_fk(self, value): self.__id_user_fk = value

    @Validators.boolean(required=True)
    def set_state_passenger(self, value): self.__state_passenger = value

    def to_dict(self):
        return {
            "id_passenger": self.__id_passenger,
            "id_user_fk": self.__id_user_fk,
            "state_passenger": self.__state_passenger
        }