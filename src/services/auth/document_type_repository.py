from src.database.base_repository import BaseRepository


class DocumentTypeRepository(BaseRepository):
    table = "document_type"
    pk = "id_doc_type"
    columns = ["name_doc_type", "acronym_doc_type", "state_doc_type"]
