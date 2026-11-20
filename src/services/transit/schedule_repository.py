from src.database.link_repository import LinkRepository
from src.database.stored_proc_repository import StoredProcRepository


class ScheduleRepository(StoredProcRepository):
    sp_entity = "Schedule"            # sp_*_Schedule (stored_procedures_hectordev.sql)
    pk = "id_schedule"
    insert_params = ["start_time", "end_time", "day_type"]
    update_params = ["start_time", "end_time", "day_type"]


class ServiceTypeRepository(StoredProcRepository):
    sp_entity = "Service_Type"
    pk = "id_service_type"
    insert_params = ["name_service_type"]
    update_params = ["name_service_type"]


class RouteScheduleRepository(LinkRepository):
    sp_entity = "Route_Schedule"      # horarios de una ruta (N:M)
    parent_col = "id_route_fk"
    child_col = "id_schedule_fk"


class ServiceTypeRouteRepository(LinkRepository):
    sp_entity = "Service_Type_Route"  # tipos de servicio de una ruta (N:M)
    parent_col = "id_route_fk"
    child_col = "id_service_type_fk"
