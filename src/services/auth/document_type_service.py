from src.models.auth import DocumentTypeModel
from src.services.auth.document_type_repository import DocumentTypeRepository
from src.utils.errors import NotFoundError


class DocumentTypeService:
    def __init__(self):
        self.repo = DocumentTypeRepository()

    def list_all(self):
        return self.repo.find_all()

    def get(self, id_doc_type):
        row = self.repo.find_by_id(id_doc_type)
        if row is None:
            raise NotFoundError(f"No existe el tipo de documento con id {id_doc_type}.")
        return row

    def create(self, data):
        doc = DocumentTypeModel(
            name_doc_type=data.get("name_doc_type"),
            acronym_doc_type=data.get("acronym_doc_type"),
            state_doc_type=data.get("state_doc_type", True),
        )
        return self.repo.create(doc.to_dict())

    def update(self, id_doc_type, data):
        current = self.get(id_doc_type)
        merged = {**current, **data}
        doc = DocumentTypeModel(
            id_doc_type=id_doc_type,
            name_doc_type=merged.get("name_doc_type"),
            acronym_doc_type=merged.get("acronym_doc_type"),
            state_doc_type=merged.get("state_doc_type", True),
        )
        return self.repo.update(id_doc_type, doc.to_dict())

    def delete(self, id_doc_type):
        self.get(id_doc_type)
        return self.repo.delete(id_doc_type)
