"""
Servicio generico para relaciones N:M simples (padre -> lista de hijos):
    list(padre)            -> hijos asociados (404 si el padre no existe)
    add(padre, data)       -> asocia un hijo (409 si ya estaba, 400 si el hijo no existe)
    remove(padre, hijo)    -> quita la asociacion (404 si no estaba)
"""

from src.utils import payload as P
from src.utils.db_errors import translate_db_errors
from src.utils.errors import ConflictError, NotFoundError


class LinkService:
    def __init__(self, repo, parent_service, child_label):
        self.repo = repo                    # LinkRepository
        self.parent = parent_service        # servicio con .get(id) -> 404 si no existe
        self.child_label = child_label      # texto para los mensajes, ej. "el horario"

    def list(self, parent_id):
        self.parent.get(parent_id)
        return self.repo.find_by_parent(parent_id)

    @translate_db_errors
    def add(self, parent_id, data):
        self.parent.get(parent_id)
        child_id = P.integer(data or {}, self.repo.child_col)
        if self.repo.find_pair(parent_id, child_id):
            raise ConflictError(f"{self.child_label.capitalize()} {child_id} ya esta asociado.")
        self.repo.add(parent_id, child_id)
        return self.repo.find_pair(parent_id, child_id)

    @translate_db_errors
    def remove(self, parent_id, child_id):
        self.parent.get(parent_id)
        if not self.repo.find_pair(parent_id, child_id):
            raise NotFoundError(f"{self.child_label.capitalize()} {child_id} no esta asociado.")
        return self.repo.remove(parent_id, child_id)
