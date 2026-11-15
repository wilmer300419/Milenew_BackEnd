from src.database.link_repository import LinkRepository
from src.database.stored_proc_repository import StoredProcRepository


class PermissionRepository(StoredProcRepository):
    sp_entity = "Permission"          # sp_*_Permission (stored_procedures_final.sql)
    pk = "id_permission"
    insert_params = ["name_permission", "description_permission"]
    update_params = ["name_permission", "description_permission"]


class RolPermissionRepository(LinkRepository):
    sp_entity = "Rol_Permission"      # permisos de un rol (N:M)
    parent_col = "id_rol_fk"
    child_col = "id_permission_fk"
