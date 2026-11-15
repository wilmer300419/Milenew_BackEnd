from src.models.ticketing import CardModel
from src.services.crud_service import CrudService
from src.services.ticketing.card_repository import (
    CardRepository, CardTypeRepository, CardStateRepository,
    TransactionTypeRepository, CardTransactionRepository,
)
from src.services.ticketing.passenger_repository import PassengerRepository
from src.security.permissions import is_admin
from src.utils import payload as P
from src.utils.db_errors import translate_db_errors
from src.utils.errors import ForbiddenError


class CardService(CrudService):
    """
    Reglas:
      - Una tarjeta nueva siempre inicia con saldo 0.
      - El saldo NO se edita por PUT: solo cambia con transacciones
        (recarga = monto positivo, cobro = monto negativo).
      - No hay DELETE: una tarjeta se bloquea/desactiva cambiando su estado.
    """
    label = "la tarjeta"

    def __init__(self):
        self.repo = CardRepository()
        self.transactions = CardTransactionRepository()
        self.passengers = PassengerRepository()

    def validate(self, data, current=None):
        for key in ("id_passenger_fk", "id_card_type_fk", "id_card_state_fk"):
            P.integer(data, key)
        card = CardModel(
            id_passenger_fk=data.get("id_passenger_fk"),
            id_card_type_fk=data.get("id_card_type_fk"),
            id_card_state_fk=data.get("id_card_state_fk"),
            balance_card=current["balance_card"] if current else 0,
        )
        d = card.to_dict()
        return {k: d[k] for k in self.repo.insert_params}

    def check_access(self, id_card, user):
        """
        Admin: cualquier tarjeta. Resto: solo las tarjetas de SU pasajero.
        404 si la tarjeta no existe, 403 si existe pero no es suya.
        """
        card = self.get(id_card)
        if is_admin(user):
            return card
        passenger = self.passengers.find_by_user(int(user["sub"]))
        if passenger is None or card.get("id_passenger_fk") != passenger["id_passenger"]:
            raise ForbiddenError("Esta tarjeta no pertenece a tu cuenta.")
        return card

    @translate_db_errors
    def set_state(self, id_card, data):
        self.get(id_card)
        id_state = P.integer(data or {}, "id_card_state_fk")
        return self.repo.set_card_state(id_card, id_state)

    # ---------------- movimientos de saldo ----------------
    def list_transactions(self, id_card):
        self.get(id_card)
        return self.transactions.find_by_card(id_card)

    @translate_db_errors
    def add_transaction(self, id_card, data):
        self.get(id_card)  # 404 si no existe
        data = data or {}
        amount = P.number(data, "amount_transaction")
        if amount == 0:
            raise ValueError("amount_transaction no puede ser 0.")
        payload = {
            "id_card_fk": id_card,
            "id_transaction_type_fk": P.integer(data, "id_transaction_type_fk"),
            "id_station_fk": P.integer(data, "id_station_fk"),
            "amount_transaction": amount,
        }
        # El SP bloquea la fila, valida saldo suficiente y actualiza el saldo atomicamente.
        self.transactions.create(payload)
        rows = self.transactions.find_by_card(id_card)
        return {
            "transaction": rows[0] if rows else None,   # GetAll viene ordenado: la mas reciente primero
            "card": self.get(id_card),
        }


class CardTypeService(CrudService):
    label = "el tipo de tarjeta"

    def __init__(self):
        self.repo = CardTypeRepository()

    def validate(self, data, current=None):
        return {"name_card_type": P.text(data, "name_card_type", 50)}


class CardStateService(CrudService):
    label = "el estado de tarjeta"

    def __init__(self):
        self.repo = CardStateRepository()

    def validate(self, data, current=None):
        return {"name_card_state": P.text(data, "name_card_state", 50)}


class TransactionTypeService(CrudService):
    label = "el tipo de transaccion"

    def __init__(self):
        self.repo = TransactionTypeRepository()

    def validate(self, data, current=None):
        return {"name_transaction_type": P.text(data, "name_transaction_type", 50)}
