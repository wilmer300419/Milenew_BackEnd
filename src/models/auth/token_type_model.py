from src.utils.validators import Validators

class TokenTypeModel:

    def __init__(self, id_token_type=None, name_token_type="", state_token_type=True):
        self.set_id_token_type(id_token_type)
        self.set_name_token_type(name_token_type)
        self.set_state_token_type(state_token_type)

    def get_id_token_type(self): return self.__id_token_type
    def get_name_token_type(self): return self.__name_token_type
    def get_state_token_type(self): return self.__state_token_type

    @Validators.integer(min_value=1, required=False)
    def set_id_token_type(self, value): self.__id_token_type = value

    @Validators.string(max_length=50, required=True)
    def set_name_token_type(self, value): self.__name_token_type = value

    @Validators.boolean(required=True)
    def set_state_token_type(self, value): self.__state_token_type = value

    def to_dict(self):
        return {
            "id_token_type": self.__id_token_type,
            "name_token_type": self.__name_token_type,
            "state_token_type": self.__state_token_type
        }