from src.database.stored_proc_repository import StoredProcRepository


class DocumentTypeRepository(StoredProcRepository):
    sp_entity = "Document_Type"      # usa sp_Insert_Document_Type, sp_GetAll_Document_Type, ...
    pk = "id_doc_type"
    insert_params = ["name_doc_type", "acronym_doc_type"]
    update_params = ["name_doc_type", "acronym_doc_type"]
