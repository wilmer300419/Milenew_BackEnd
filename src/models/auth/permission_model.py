from src.utils.validators import Validators

class PermissionModel:

    def __init__(self, id_permission=None, name_permission="", description_permission=None, state_permission=True):
        self.set_id_permission(id_permission)
        self.set_name_permission(name_permission)
        self.set_description_permission(description_permission)
        self.set_state_permission(state_permission)

    def get_id_permission(self): return self.__id_permission
    def get_name_permission(self): return self.__name_permission
    def get_description_permission(self): return self.__description_permission
    def get_state_permission(self): return self.__state_permission

    @Validators.integer(min_value=1, required=False)
    def set_id_permission(self, value): self.__id_permission = value

    @Validators.string(max_length=50, required=True)
    def set_name_permission(self, value): self.__name_permission = value

    @Validators.string(max_length=200, required=False)
    def set_description_permission(self, value): self.__description_permission = value

    @Validators.boolean(required=True)
    def set_state_permission(self, value): self.__state_permission = value

    def to_dict(self):
        return {
            "id_permission": self.__id_permission,
            "name_permission": self.__name_permission,
            "description_permission": self.__description_permission,
            "state_permission": self.__state_permission
        }