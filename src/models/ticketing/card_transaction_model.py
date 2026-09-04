from src.utils.validators import Validators

class CardTransactionModel:

    def __init__(self, id_card_fk, id_transaction_type_fk, id_station_fk, amount_transaction, balance_before, balance_after,
                 id_card_transaction=None, transaction_date_hour=None, state_transaction=True):
        self.set_id_card_transaction(id_card_transaction)
        self.set_id_card_fk(id_card_fk)
        self.set_id_transaction_type_fk(id_transaction_type_fk)
        self.set_id_station_fk(id_station_fk)
        self.set_amount_transaction(amount_transaction)
        self.set_balance_before(balance_before)
        self.set_balance_after(balance_after)
        self.set_transaction_date_hour(transaction_date_hour)
        self.set_state_transaction(state_transaction)

    def get_id_card_transaction(self): return self.__id_card_transaction
    def get_id_card_fk(self): return self.__id_card_fk
    def get_id_transaction_type_fk(self): return self.__id_transaction_type_fk
    def get_id_station_fk(self): return self.__id_station_fk
    def get_amount_transaction(self): return self.__amount_transaction
    def get_balance_before(self): return self.__balance_before
    def get_balance_after(self): return self.__balance_after
    def get_transaction_date_hour(self): return self.__transaction_date_hour
    def get_state_transaction(self): return self.__state_transaction

    @Validators.integer(min_value=1, required=False)
    def set_id_card_transaction(self, value): self.__id_card_transaction = value

    @Validators.integer(min_value=1, required=True)
    def set_id_card_fk(self, value): self.__id_card_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_transaction_type_fk(self, value): self.__id_transaction_type_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_station_fk(self, value): self.__id_station_fk = value

    @Validators.decimal(required=True)
    def set_amount_transaction(self, value): self.__amount_transaction = value

    @Validators.decimal(required=True)
    def set_balance_before(self, value): self.__balance_before = value

    @Validators.decimal(required=True)
    def set_balance_after(self, value): self.__balance_after = value

    @Validators.datetime(required=False)
    def set_transaction_date_hour(self, value): self.__transaction_date_hour = value

    @Validators.boolean(required=True)
    def set_state_transaction(self, value): self.__state_transaction = value

    def to_dict(self):
        return {
            "id_card_transaction": self.__id_card_transaction,
            "id_card_fk": self.__id_card_fk,
            "id_transaction_type_fk": self.__id_transaction_type_fk,
            "id_station_fk": self.__id_station_fk,
            "amount_transaction": float(self.__amount_transaction) if self.__amount_transaction is not None else None,
            "balance_before": float(self.__balance_before) if self.__balance_before is not None else None,
            "balance_after": float(self.__balance_after) if self.__balance_after is not None else None,
            "transaction_date_hour": self.__transaction_date_hour.isoformat() if self.__transaction_date_hour else None,
            "state_transaction": self.__state_transaction
        }