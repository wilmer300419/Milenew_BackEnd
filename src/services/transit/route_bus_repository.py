"""Buses asignados a una ruta por fecha (tabla route_bus, llave ruta+bus+fecha)."""

from src.database.stored_proc_repository import StoredProcRepository


class RouteBusRepository(StoredProcRepository):
    sp_entity = "Route_Bus"
    insert_params = ["id_route_fk", "id_bus_fk", "service_date", "start_time", "end_time"]

    def find_by_route(self, id_route, conn=None):
        return [r for r in self.find_all(conn=conn) if r["id_route_fk"] == id_route]

    def find_assignment(self, id_route, id_bus, service_date, conn=None):
        name = "cur_route_bus_by_id"
        with self._session(conn) as c:
            rows = self._fetch_cursor(
                c, "CALL sp_GetById_Route_Bus(%s, %s, %s, %s)",
                (id_route, id_bus, service_date, name), name
            )
            return rows[0] if rows else None

    def update_assignment(self, id_route, id_bus, service_date, start_time, end_time, conn=None):
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute("CALL sp_Update_Route_Bus(%s, %s, %s, %s, %s)",
                            (id_route, id_bus, service_date, start_time, end_time))
            return self.find_assignment(id_route, id_bus, service_date, conn=c)

    def remove(self, id_route, id_bus, service_date, conn=None):
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute("CALL sp_Delete_Route_Bus(%s, %s, %s)", (id_route, id_bus, service_date))
        return True
