from src.database.stored_proc_repository import StoredProcRepository


class RolRepository(StoredProcRepository):
    sp_entity = "Rol"                # sp_*_Rol (stored_procedures_final.sql)
    pk = "id_rol"
    insert_params = ["name_rol", "description_rol"]
    update_params = ["name_rol", "description_rol"]

    def find_by_name(self, name, conn=None):
        """Busca un rol ACTIVO por nombre, sin distinguir mayusculas."""
        target = (name or "").strip().lower()
        for row in self.find_all(conn=conn):
            if (row.get("name_rol") or "").strip().lower() == target:
                return row
        return None
