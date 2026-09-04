from src.utils.validators import Validators

class ScheduleModel:

    def __init__(self, start_time, end_time, day_type, id_schedule=None, state_schedule=True):
        self.set_id_schedule(id_schedule)
        self.set_start_time(start_time)
        self.set_end_time(end_time)
        self.set_day_type(day_type)
        self.set_state_schedule(state_schedule)

    def get_id_schedule(self): return self.__id_schedule
    def get_start_time(self): return self.__start_time
    def get_end_time(self): return self.__end_time
    def get_day_type(self): return self.__day_type
    def get_state_schedule(self): return self.__state_schedule

    @Validators.integer(min_value=1, required=False)
    def set_id_schedule(self, value): self.__id_schedule = value

    @Validators.time(required=True)
    def set_start_time(self, value): self.__start_time = value

    @Validators.time(required=True)
    def set_end_time(self, value): self.__end_time = value

    @Validators.string(max_length=20, required=True)
    def set_day_type(self, value): self.__day_type = value

    @Validators.boolean(required=True)
    def set_state_schedule(self, value): self.__state_schedule = value

    def to_dict(self):
        return {
            "id_schedule": self.__id_schedule,
            "start_time": self.__start_time.isoformat() if self.__start_time else None,
            "end_time": self.__end_time.isoformat() if self.__end_time else None,
            "day_type": self.__day_type,
            "state_schedule": self.__state_schedule
        }