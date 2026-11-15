from src.database.stored_proc_repository import StoredProcRepository


class StationRepository(StoredProcRepository):
    sp_entity = "Station"
    pk = "id_station"
    insert_params = ["id_station_type_fk", "name_station", "address_station",
                     "latitude_station", "longitude_station"]
    update_params = insert_params
