from src.utils.validators import Validators

class RolPermissionModel:

    def __init__(self, id_rol_fk, id_permission_fk):
        self.set_id_rol_fk(id_rol_fk)
        self.set_id_permission_fk(id_permission_fk)

    def get_id_rol_fk(self): return self.__id_rol_fk
    def get_id_permission_fk(self): return self.__id_permission_fk

    @Validators.integer(min_value=1, required=True)
    def set_id_rol_fk(self, value): self.__id_rol_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_permission_fk(self, value): self.__id_permission_fk = value

    def to_dict(self):
        return {
            "id_rol_fk": self.__id_rol_fk,
            "id_permission_fk": self.__id_permission_fk
        }