from src.database.stored_proc_repository import StoredProcRepository


class PassengerRepository(StoredProcRepository):
    sp_entity = "Passenger"          # usa sp_Insert_Passenger, sp_GetAll_Passenger, ...
    pk = "id_passenger"
    insert_params = ["id_user_fk"]
    update_params = ["id_user_fk"]

    def find_by_user(self, id_user, conn=None):
        return self.find_one_by("id_user_fk", id_user, conn=conn)
