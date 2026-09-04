from src.utils.validators import Validators

class UserTokenModel:

    def __init__(self, id_token_type_fk, id_user_fk, id_user_token=None, start_time=None, end_time=None, state_user_token=True):
        self.set_id_user_token(id_user_token)
        self.set_id_token_type_fk(id_token_type_fk)
        self.set_id_user_fk(id_user_fk)
        self.set_start_time(start_time)
        self.set_end_time(end_time)
        self.set_state_user_token(state_user_token)

    def get_id_user_token(self): return self.__id_user_token
    def get_id_token_type_fk(self): return self.__id_token_type_fk
    def get_id_user_fk(self): return self.__id_user_fk
    def get_start_time(self): return self.__start_time
    def get_end_time(self): return self.__end_time
    def get_state_user_token(self): return self.__state_user_token

    @Validators.integer(min_value=1, required=False)
    def set_id_user_token(self, value): self.__id_user_token = value

    @Validators.integer(min_value=1, required=True)
    def set_id_token_type_fk(self, value): self.__id_token_type_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_user_fk(self, value): self.__id_user_fk = value

    @Validators.datetime(required=False)
    def set_start_time(self, value): self.__start_time = value

    @Validators.datetime(required=False)
    def set_end_time(self, value): self.__end_time = value

    @Validators.boolean(required=True)
    def set_state_user_token(self, value): self.__state_user_token = value

    def to_dict(self):
        return {
            "id_user_token": self.__id_user_token,
            "id_token_type_fk": self.__id_token_type_fk,
            "id_user_fk": self.__id_user_fk,
            "start_time": self.__start_time.isoformat() if self.__start_time else None,
            "end_time": self.__end_time.isoformat() if self.__end_time else None,
            "state_user_token": self.__state_user_token
        }