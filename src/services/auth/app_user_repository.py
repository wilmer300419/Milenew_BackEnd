from src.database.stored_proc_repository import StoredProcRepository


class AppUserRepository(StoredProcRepository):
    sp_entity = "User"               # usa sp_Insert_User, sp_GetAll_User, ...
    pk = "id_user"
    insert_params = ["id_person_fk", "id_rol_fk", "username", "password"]
    update_params = ["id_person_fk", "id_rol_fk", "username", "password"]

    def find_by_username(self, username, conn=None):
        # La DB no expone un sp_GetByUsername: se filtra del GetAll (solo activos).
        # username es UNIQUE, asi que tambien sirve para recuperar el id recien creado.
        return self.find_one_by("username", username, conn=conn)
