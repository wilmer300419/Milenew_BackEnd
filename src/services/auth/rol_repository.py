from src.database.base_repository import BaseRepository


class RolRepository(BaseRepository):
    table = "rol"
    pk = "id_rol"
    columns = ["name_rol", "description_rol", "state_rol"]
