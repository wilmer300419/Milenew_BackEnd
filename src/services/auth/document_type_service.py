"""
Catalogo de tipos de documento. Usa el CRUD generico (CrudService), que tras el
INSERT recupera la fila creada (sp_Insert_Document_Type no devuelve el id),
mezcla datos en el PUT y hace soft-delete via sp_UpdateState_Document_Type.
"""

from src.models.auth import DocumentTypeModel
from src.services.crud_service import CrudService
from src.services.auth.document_type_repository import DocumentTypeRepository


class DocumentTypeService(CrudService):
    label = "el tipo de documento"

    def __init__(self):
        self.repo = DocumentTypeRepository()

    def validate(self, data, current=None):
        doc = DocumentTypeModel(
            name_doc_type=data.get("name_doc_type"),
            acronym_doc_type=data.get("acronym_doc_type"),
        )
        d = doc.to_dict()
        return {k: d[k] for k in self.repo.insert_params}
