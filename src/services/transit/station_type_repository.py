from src.database.stored_proc_repository import StoredProcRepository


class StationTypeRepository(StoredProcRepository):
    sp_entity = "Station_Type"
    pk = "id_station_type"
    insert_params = ["name_station_type"]
    update_params = ["name_station_type"]
