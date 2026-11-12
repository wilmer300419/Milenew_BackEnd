from src.database.stored_proc_repository import StoredProcRepository


class PersonRepository(StoredProcRepository):
    sp_entity = "Person"             # usa sp_Insert_Person, sp_GetAll_Person, ...
    pk = "id_person"
    insert_params = [
        "id_doc_type_fk", "num_doc_person", "first_name_person", "second_name_person",
        "first_last_name_person", "second_last_name_person", "phone_number_person",
        "birthdate_person", "email_person",
    ]
    update_params = insert_params

    def find_by_num_doc(self, num_doc, conn=None):
        # num_doc_person es UNIQUE en la DB, sirve para recuperar el id recien creado.
        return self.find_one_by("num_doc_person", num_doc, conn=conn)
