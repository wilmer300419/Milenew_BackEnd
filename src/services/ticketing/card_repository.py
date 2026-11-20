from src.database.stored_proc_repository import StoredProcRepository


class CardRepository(StoredProcRepository):
    sp_entity = "Card"
    pk = "id_card"
    insert_params = ["id_passenger_fk", "id_card_type_fk", "id_card_state_fk", "balance_card"]
    update_params = insert_params

    def set_card_state(self, id_card, id_card_state, conn=None):
        # OJO: en la BD sp_UpdateState_Card recibe el ID del estado (no un booleano).
        self.change_state(id_card, id_card_state, conn=conn)
        return self.find_by_id(id_card, conn=conn)


class CardTypeRepository(StoredProcRepository):
    sp_entity = "Card_Type"
    pk = "id_card_type"
    insert_params = ["name_card_type"]
    update_params = ["name_card_type"]


class CardStateRepository(StoredProcRepository):
    sp_entity = "Card_State"
    pk = "id_card_state"
    insert_params = ["name_card_state"]
    update_params = ["name_card_state"]


class TransactionTypeRepository(StoredProcRepository):
    sp_entity = "Transaction_Type"
    pk = "id_transaction_type"
    insert_params = ["name_transaction_type"]
    update_params = ["name_transaction_type"]


class CardTransactionRepository(StoredProcRepository):
    sp_entity = "Card_Transaction"
    pk = "id_card_transaction"
    insert_params = ["id_card_fk", "id_transaction_type_fk", "id_station_fk", "amount_transaction"]

    def find_by_card(self, id_card, conn=None):
        return [r for r in self.find_all(conn=conn) if r["id_card_fk"] == id_card]
