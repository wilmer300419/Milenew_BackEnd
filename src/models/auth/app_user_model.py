from src.utils.validators import Validators

class AppUserModel:

    def __init__(self, id_person_fk, id_rol_fk, username, password, id_user=None, state_user=True):
        self.set_id_user(id_user)
        self.set_id_person_fk(id_person_fk)
        self.set_id_rol_fk(id_rol_fk)
        self.set_username(username)
        self.set_password(password)
        self.set_state_user(state_user)

    def get_id_user(self): return self.__id_user
    def get_id_person_fk(self): return self.__id_person_fk
    def get_id_rol_fk(self): return self.__id_rol_fk
    def get_username(self): return self.__username
    def get_password(self): return self.__password
    def get_state_user(self): return self.__state_user

    @Validators.integer(min_value=1, required=False)
    def set_id_user(self, value): self.__id_user = value

    @Validators.integer(min_value=1, required=True)
    def set_id_person_fk(self, value): self.__id_person_fk = value

    @Validators.integer(min_value=1, required=True)
    def set_id_rol_fk(self, value): self.__id_rol_fk = value

    @Validators.string(max_length=50, required=True)
    def set_username(self, value): self.__username = value

    @Validators.string(max_length=255, required=True)
    def set_password(self, value): self.__password = value

    @Validators.boolean(required=True)
    def set_state_user(self, value): self.__state_user = value

    def to_dict(self):
        return {
            "id_user": self.__id_user,
            "id_person_fk": self.__id_person_fk,
            "id_rol_fk": self.__id_rol_fk,
            "username": self.__username,
            "state_user": self.__state_user
        }