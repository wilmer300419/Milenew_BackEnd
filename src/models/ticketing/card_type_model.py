from src.utils.validators import Validators

class CardTypeModel:

    def __init__(self, id_card_type=None, name_card_type="", state_card_type=True):
        self.set_id_card_type(id_card_type)
        self.set_name_card_type(name_card_type)
        self.set_state_card_type(state_card_type)

    def get_id_card_type(self): return self.__id_card_type
    def get_name_card_type(self): return self.__name_card_type
    def get_state_card_type(self): return self.__state_card_type

    @Validators.integer(min_value=1, required=False)
    def set_id_card_type(self, value): self.__id_card_type = value

    @Validators.string(max_length=50, required=True)
    def set_name_card_type(self, value): self.__name_card_type = value

    @Validators.boolean(required=True)
    def set_state_card_type(self, value): self.__state_card_type = value

    def to_dict(self):
        return {
            "id_card_type": self.__id_card_type,
            "name_card_type": self.__name_card_type,
            "state_card_type": self.__state_card_type
        }