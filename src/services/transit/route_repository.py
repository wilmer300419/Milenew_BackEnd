from src.database.stored_proc_repository import StoredProcRepository


class RouteRepository(StoredProcRepository):
    sp_entity = "Route"
    pk = "id_route"
    insert_params = ["code_route", "description_route"]
    update_params = ["code_route", "description_route"]
