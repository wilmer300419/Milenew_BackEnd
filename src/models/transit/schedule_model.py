from src.utils.validators import Validators

class ScheduleModel:

    def __init__(self, id_day_type_fk, start_time, end_time, id_schedule=None, state_schedule=True):
        self.set_id_schedule(id_schedule)
        self.set_id_day_type_fk(id_day_type_fk)
        self.set_start_time(start_time)
        self.set_end_time(end_time)
        self.set_state_schedule(state_schedule)

    def get_id_schedule(self): return self.__id_schedule
    def get_id_day_type_fk(self): return self.__id_day_type_fk
    def get_start_time(self): return self.__start_time
    def get_end_time(self): return self.__end_time
    def get_state_schedule(self): return self.__state_schedule

    @Validators.integer(min_value=1, required=False)
    def set_id_schedule(self, value): self.__id_schedule = value

    @Validators.integer(min_value=1, required=True)
    def set_id_day_type_fk(self, value): self.__id_day_type_fk = value

    @Validators.time(required=True)
    def set_start_time(self, value): self.__start_time = value

    @Validators.time(required=True)
    def set_end_time(self, value): self.__end_time = value

    @Validators.boolean(required=True)
    def set_state_schedule(self, value): self.__state_schedule = value

    def to_dict(self):
        return {
            "id_schedule": self.__id_schedule,
            "id_day_type_fk": self.__id_day_type_fk,
            "start_time": self.__start_time.isoformat() if self.__start_time else None,
            "end_time": self.__end_time.isoformat() if self.__end_time else None,
            "state_schedule": self.__state_schedule
        }