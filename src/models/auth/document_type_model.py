from src.utils.validators import Validators

class DocumentTypeModel:

    def __init__(self, id_doc_type=None, name_doc_type="", acronym_doc_type="", state_doc_type=True):
        self.set_id_doc_type(id_doc_type)
        self.set_name_doc_type(name_doc_type)
        self.set_acronym_doc_type(acronym_doc_type)
        self.set_state_doc_type(state_doc_type)

    def get_id_doc_type(self):
        return self.__id_doc_type

    def get_name_doc_type(self):
        return self.__name_doc_type

    def get_acronym_doc_type(self):
        return self.__acronym_doc_type

    def get_state_doc_type(self):
        return self.__state_doc_type

    @Validators.integer(min_value=1, required=False)
    def set_id_doc_type(self, value):
        self.__id_doc_type = value

    @Validators.string(max_length=50, required=True)
    def set_name_doc_type(self, value):
        self.__name_doc_type = value

    @Validators.string(max_length=10, required=True)
    def set_acronym_doc_type(self, value):
        self.__acronym_doc_type = value

    @Validators.boolean(required=True)
    def set_state_doc_type(self, value):
        self.__state_doc_type = value

    def to_dict(self):
        return {
            "id_doc_type": self.__id_doc_type,
            "name_doc_type": self.__name_doc_type,
            "acronym_doc_type": self.__acronym_doc_type,
            "state_doc_type": self.__state_doc_type
        }