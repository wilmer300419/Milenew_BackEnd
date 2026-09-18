from src.database.base_repository import BaseRepository


class AppUserRepository(BaseRepository):
    table = "app_user"
    pk = "id_user"
    columns = ["id_person_fk", "id_rol_fk", "username", "password", "state_user"]

    def find_by_username(self, username):
        return self.find_one_by("username", username)
