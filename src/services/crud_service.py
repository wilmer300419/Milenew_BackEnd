"""
Servicio CRUD generico sobre un StoredProcRepository.

Cada servicio concreto define:
    repo, label (para mensajes), pk
    validate(data, current=None) -> dict con los campos listos para el SP
        (lanza ValueError si algo es invalido; `current` es la fila actual en PUT)
"""

from decimal import Decimal

from src.utils.db_errors import translate_db_errors
from src.utils.errors import NotFoundError


class CrudService:
    repo = None
    label = "registro"

    def validate(self, data, current=None):
        raise NotImplementedError

    def list_all(self):
        return self.repo.find_all()

    def get(self, id_value):
        row = self.repo.find_by_id(id_value)
        if row is None:
            raise NotFoundError(f"No existe {self.label} con id {id_value}.")
        return row

    @translate_db_errors
    def create(self, data):
        payload = self.validate(data or {})
        echo = self.repo.create(payload)
        return self._find_created(payload) or echo

    @translate_db_errors
    def update(self, id_value, data):
        current = self.get(id_value)
        payload = self.validate({**current, **(data or {})}, current=current)
        return self.repo.update(id_value, payload)

    @translate_db_errors
    def delete(self, id_value):
        # Borrado logico via sp_UpdateState_<Entidad>(id, FALSE)
        self.get(id_value)
        return self.repo.delete(id_value)

    # El SP de insercion no devuelve el id: buscamos la fila recien creada
    # comparando los campos insertados (la mas reciente que coincida).
    def _find_created(self, payload):
        try:
            for row in reversed(self.repo.find_all()):
                if all(_same(row.get(k), payload.get(k)) for k in self.repo.insert_params
                       if payload.get(k) is not None):
                    return row
        except Exception:
            pass
        return None


def _same(a, b):
    """Compara numeros (Decimal vs float) o textos sin que el formato estorbe."""
    try:
        return Decimal(str(a)) == Decimal(str(b))
    except Exception:
        return str(a) == str(b)
