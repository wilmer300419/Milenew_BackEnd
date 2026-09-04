from src.utils.validators import Validators

class CardStateModel:

    def __init__(self, id_card_state=None, name_card_state="", state_card_state=True):
        self.set_id_card_state(id_card_state)
        self.set_name_card_state(name_card_state)
        self.set_state_card_state(state_card_state)

    def get_id_card_state(self): return self.__id_card_state
    def get_name_card_state(self): return self.__name_card_state
    def get_state_card_state(self): return self.__state_card_state

    @Validators.integer(min_value=1, required=False)
    def set_id_card_state(self, value): self.__id_card_state = value

    @Validators.string(max_length=50, required=True)
    def set_name_card_state(self, value): self.__name_card_state = value

    @Validators.boolean(required=True)
    def set_state_card_state(self, value): self.__state_card_state = value

    def to_dict(self):
        return {
            "id_card_state": self.__id_card_state,
            "name_card_state": self.__name_card_state,
            "state_card_state": self.__state_card_state
        }