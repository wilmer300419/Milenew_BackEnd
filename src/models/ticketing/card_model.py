from src.utils.validators import Validators

class CardModel:

    def __init__(self, id_passenger_fk, id_card_type_fk, id_card_state_fk, id_card=None, balance_card=0.0):
        self.set_id_card(id_card)
        self.set_id_passenger_fk(id_passenger_fk)
        self.set_id_card_type_fk(id_card_type_fk)
        self.set_id_card_state_fk(id_card_state_fk)
        self.set_balance_card(balance_card)

    def get_id_card(self): return self.__id_card
    def get_id_passenger_fk(self): return self.__id_passenger_fk
    def get_id_card_type_fk(self): return self.__id_card_type_fk
    def get_id_card_state_fk(self): return self.__id_card_state_fk
    def get_balance_card(self): return self.__balance_card

    @Validators.integer(min_value=1, required=False)
    def set_id_card(self, value): self.__id_card = value

    @Validators.integer(min_value=1, required=True)
    def set_id_passenger_fk(self, value): self.__id_passenger_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_card_type_fk(self, value): self.__id_card_type_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_card_state_fk(self, value): self.__id_card_state_fk = value

    @Validators.decimal(min_value=0, required=True)
    def set_balance_card(self, value): self.__balance_card = value

    def to_dict(self):
        return {
            "id_card": self.__id_card,
            "id_passenger_fk": self.__id_passenger_fk,
            "id_card_type_fk": self.__id_card_type_fk,
            "id_card_state_fk": self.__id_card_state_fk,
            "balance_card": float(self.__balance_card) if self.__balance_card is not None else 0.0
        }