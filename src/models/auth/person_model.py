from src.utils.validators import Validators

class PersonModel:

    def __init__(self, id_doc_type_fk, num_doc_person, first_name_person, first_last_name_person,
                 id_person=None, second_name_person=None, second_last_name_person=None,
                 phone_number_person=None, birthdate_person=None, email_person=None, state_person=True):
        self.set_id_person(id_person)
        self.set_id_doc_type_fk(id_doc_type_fk)
        self.set_num_doc_person(num_doc_person)
        self.set_first_name_person(first_name_person)
        self.set_second_name_person(second_name_person)
        self.set_first_last_name_person(first_last_name_person)
        self.set_second_last_name_person(second_last_name_person)
        self.set_phone_number_person(phone_number_person)
        self.set_birthdate_person(birthdate_person)
        self.set_email_person(email_person)
        self.set_state_person(state_person)

    def get_id_person(self): return self.__id_person
    def get_id_doc_type_fk(self): return self.__id_doc_type_fk
    def get_num_doc_person(self): return self.__num_doc_person
    def get_first_name_person(self): return self.__first_name_person
    def get_second_name_person(self): return self.__second_name_person
    def get_first_last_name_person(self): return self.__first_last_name_person
    def get_second_last_name_person(self): return self.__second_last_name_person
    def get_phone_number_person(self): return self.__phone_number_person
    def get_birthdate_person(self): return self.__birthdate_person
    def get_email_person(self): return self.__email_person
    def get_state_person(self): return self.__state_person

    @Validators.integer(min_value=1, required=False)
    def set_id_person(self, value): self.__id_person = value

    @Validators.integer(min_value=1, required=True)
    def set_id_doc_type_fk(self, value): self.__id_doc_type_fk = value

    @Validators.string(max_length=20, required=True)
    def set_num_doc_person(self, value): self.__num_doc_person = value

    @Validators.string(max_length=50, required=True)
    def set_first_name_person(self, value): self.__first_name_person = value

    @Validators.string(max_length=50, required=False)
    def set_second_name_person(self, value): self.__second_name_person = value

    @Validators.string(max_length=50, required=True)
    def set_first_last_name_person(self, value): self.__first_last_name_person = value

    @Validators.string(max_length=50, required=False)
    def set_second_last_name_person(self, value): self.__second_last_name_person = value

    @Validators.string(max_length=20, required=False)
    def set_phone_number_person(self, value): self.__phone_number_person = value

    @Validators.date(required=False)
    def set_birthdate_person(self, value): self.__birthdate_person = value

    @Validators.string(max_length=150, required=False)
    def set_email_person(self, value): self.__email_person = value

    @Validators.boolean(required=True)
    def set_state_person(self, value): self.__state_person = value

    def to_dict(self):
        return {
            "id_person": self.__id_person,
            "id_doc_type_fk": self.__id_doc_type_fk,
            "num_doc_person": self.__num_doc_person,
            "first_name_person": self.__first_name_person,
            "second_name_person": self.__second_name_person,
            "first_last_name_person": self.__first_last_name_person,
            "second_last_name_person": self.__second_last_name_person,
            "phone_number_person": self.__phone_number_person,
            "birthdate_person": self.__birthdate_person.isoformat() if self.__birthdate_person else None,
            "email_person": self.__email_person,
            "state_person": self.__state_person
        }