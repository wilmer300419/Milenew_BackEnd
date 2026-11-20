"""Conductores/empleados asignados a un bus por fecha (tabla bus_employee, llave bus+empleado+fecha)."""

from src.database.stored_proc_repository import StoredProcRepository


class BusEmployeeRepository(StoredProcRepository):
    sp_entity = "Bus_Employee"
    insert_params = ["id_bus_fk", "id_employee_fk", "service_date", "start_time", "end_time"]
    # La DB no trae sp_Delete ni sp_UpdateState para esta tabla: no se puede quitar una asignacion.

    def find_by_bus(self, id_bus, conn=None):
        return [r for r in self.find_all(conn=conn) if r["id_bus_fk"] == id_bus]

    def find_assignment(self, id_bus, id_employee, service_date, conn=None):
        name = "cur_bus_employee_by_id"
        with self._session(conn) as c:
            rows = self._fetch_cursor(
                c, "CALL sp_GetById_Bus_Employee(%s, %s, %s, %s)",
                (id_bus, id_employee, service_date, name), name
            )
            return rows[0] if rows else None

    def update_assignment(self, id_bus, id_employee, service_date, start_time, end_time, conn=None):
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute("CALL sp_Update_Bus_Employee(%s, %s, %s, %s, %s)",
                            (id_bus, id_employee, service_date, start_time, end_time))
            return self.find_assignment(id_bus, id_employee, service_date, conn=c)
