"""
Tarjetas y movimientos de saldo.

Permisos:
    - Listar todas, crear, editar y bloquear (PATCH state): solo administradores.
    - Ver UNA tarjeta y sus movimientos: el dueno (pasajero) o un administrador.
    - Registrar movimiento: el dueno solo puede RECARGAR (monto > 0);
      los cobros (monto < 0) los registra un administrador.
"""

from flask import request, jsonify, g

from src.routes.crud_blueprint import crud_blueprint
from src.security.auth_middleware import token_required
from src.security.permissions import admin_required, is_admin
from src.services.ticketing.card_service import (
    CardService, CardTypeService, CardStateService, TransactionTypeService,
)
from src.utils import payload as P
from src.utils.errors import ForbiddenError

service = CardService()
# Sin DELETE: una tarjeta se bloquea cambiando su estado (PATCH /<id>/state).
# GET /<id> se define abajo porque necesita control de dueno.
card_bp = crud_blueprint("card", "/api/cards", service, "Tarjeta",
                         allow_delete=False, list_access="admin", get_access=None)


@card_bp.get("/<int:id_card>")
@token_required
def get_card(id_card):
    return jsonify(service.check_access(id_card, g.current_user)), 200


@card_bp.patch("/<int:id_card>/state")
@token_required
@admin_required
def set_card_state(id_card):
    return jsonify(service.set_state(id_card, request.get_json(silent=True))), 200


@card_bp.get("/<int:id_card>/transactions")
@token_required
def list_card_transactions(id_card):
    service.check_access(id_card, g.current_user)
    return jsonify(service.list_transactions(id_card)), 200


@card_bp.post("/<int:id_card>/transactions")
@token_required
def add_card_transaction(id_card):
    """Monto positivo = recarga, negativo = cobro de pasaje."""
    data = request.get_json(silent=True) or {}
    service.check_access(id_card, g.current_user)
    if not is_admin() and P.number(data, "amount_transaction") <= 0:
        raise ForbiddenError("Solo puedes recargar tu tarjeta (monto positivo); los cobros los registra el sistema.")
    return jsonify(service.add_transaction(id_card, data)), 201


card_type_bp = crud_blueprint("card_type", "/api/card-types", CardTypeService(), "Tipo de tarjeta")
card_state_bp = crud_blueprint("card_state", "/api/card-states", CardStateService(), "Estado de tarjeta")
transaction_type_bp = crud_blueprint("transaction_type", "/api/transaction-types",
                                     TransactionTypeService(), "Tipo de transaccion")
