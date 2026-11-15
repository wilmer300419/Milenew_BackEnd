from src.database.stored_proc_repository import StoredProcRepository


class BusRepository(StoredProcRepository):
    sp_entity = "Bus"
    pk = "id_bus"
    insert_params = ["id_bus_type_fk", "code_bus", "plate_bus"]
    update_params = insert_params


class BusTypeRepository(StoredProcRepository):
    sp_entity = "Bus_Type"
    pk = "id_bus_type"
    insert_params = ["name_bus_type", "capacity_bus_type"]
    update_params = insert_params
