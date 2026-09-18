from src.models.auth import RolModel
from src.services.auth.rol_repository import RolRepository
from src.utils.errors import NotFoundError


class RolService:
    def __init__(self):
        self.repo = RolRepository()

    def list_all(self):
        return self.repo.find_all()

    def get(self, id_rol):
        row = self.repo.find_by_id(id_rol)
        if row is None:
            raise NotFoundError(f"No existe el rol con id {id_rol}.")
        return row

    def create(self, data):
        # Validacion via el modelo de dominio (lanza ValueError si es invalido)
        rol = RolModel(
            name_rol=data.get("name_rol"),
            description_rol=data.get("description_rol"),
            state_rol=data.get("state_rol", True),
        )
        return self.repo.create(rol.to_dict())

    def update(self, id_rol, data):
        current = self.get(id_rol)  # 404 si no existe
        merged = {**current, **data}
        rol = RolModel(
            id_rol=id_rol,
            name_rol=merged.get("name_rol"),
            description_rol=merged.get("description_rol"),
            state_rol=merged.get("state_rol", True),
        )
        return self.repo.update(id_rol, rol.to_dict())

    def delete(self, id_rol):
        self.get(id_rol)  # 404 si no existe
        return self.repo.delete(id_rol)
