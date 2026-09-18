from flask import Blueprint, request, jsonify
from src.services.auth.document_type_service import DocumentTypeService

document_type_bp = Blueprint("document_type", __name__, url_prefix="/api/document-types")
service = DocumentTypeService()


@document_type_bp.get("")
def list_document_types():
    return jsonify(service.list_all()), 200


@document_type_bp.get("/<int:id_doc_type>")
def get_document_type(id_doc_type):
    return jsonify(service.get(id_doc_type)), 200


@document_type_bp.post("")
def create_document_type():
    data = request.get_json(silent=True) or {}
    return jsonify(service.create(data)), 201


@document_type_bp.put("/<int:id_doc_type>")
def update_document_type(id_doc_type):
    data = request.get_json(silent=True) or {}
    return jsonify(service.update(id_doc_type, data)), 200


@document_type_bp.delete("/<int:id_doc_type>")
def delete_document_type(id_doc_type):
    service.delete(id_doc_type)
    return jsonify({"message": f"Tipo de documento {id_doc_type} eliminado."}), 200
