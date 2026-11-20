"""Estaciones de una ruta (tabla route_station, llave compuesta ruta+estacion)."""

from src.database.stored_proc_repository import StoredProcRepository


class RouteStationRepository(StoredProcRepository):
    sp_entity = "Route_Station"
    insert_params = ["id_route_fk", "id_station_fk", "order_route_station"]
    update_params = ["id_station_fk", "order_route_station"]  # no se usa el update generico

    def find_by_route(self, id_route, conn=None):
        # sp_GetAll_Route_Station ya viene ordenado por ruta y orden
        return [r for r in self.find_all(conn=conn) if r["id_route_fk"] == id_route]

    def find_pair(self, id_route, id_station, conn=None):
        name = "cur_route_station_by_id"
        with self._session(conn) as c:
            rows = self._fetch_cursor(
                c, "CALL sp_GetById_Route_Station(%s, %s, %s)", (id_route, id_station, name), name
            )
            return rows[0] if rows else None

    def update_order(self, id_route, id_station, order, conn=None):
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute("CALL sp_Update_Route_Station(%s, %s, %s)", (id_route, id_station, order))
            return self.find_pair(id_route, id_station, conn=c)

    def set_active(self, id_route, id_station, active, conn=None):
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute("CALL sp_UpdateState_Route_Station(%s, %s, %s)", (id_route, id_station, active))
        return True

    def remove(self, id_route, id_station, conn=None):
        # Borrado logico: la fila queda con state_route_station = FALSE.
        return self.set_active(id_route, id_station, False, conn=conn)
