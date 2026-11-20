"""
Tablas de union N:M sin estado (llave compuesta padre + hijo), por ejemplo
route_schedule, service_type_route y rol_permission. Sus SPs son:

    sp_Insert_<X>(padre, hijo)
    sp_GetAll_<X>(refcursor)
    sp_GetById_<X>(padre, hijo, refcursor)
    sp_Delete_<X>(padre, hijo)          <- borrado fisico (no tienen columna de estado)
"""

from src.database.stored_proc_repository import StoredProcRepository


class LinkRepository(StoredProcRepository):
    parent_col = None   # ej. "id_route_fk"
    child_col = None    # ej. "id_schedule_fk"

    @property
    def insert_params(self):
        return [self.parent_col, self.child_col]

    def find_by_parent(self, parent_id, conn=None):
        return [r for r in self.find_all(conn=conn) if r.get(self.parent_col) == parent_id]

    def find_pair(self, parent_id, child_id, conn=None):
        name = f"cur_{self.sp_entity.lower()}_pair"
        with self._session(conn) as c:
            rows = self._fetch_cursor(
                c, f"CALL sp_GetById_{self.sp_entity}(%s, %s, %s)", (parent_id, child_id, name), name
            )
            return rows[0] if rows else None

    def add(self, parent_id, child_id, conn=None):
        return self.create({self.parent_col: parent_id, self.child_col: child_id}, conn=conn)

    def remove(self, parent_id, child_id, conn=None):
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute(f"CALL sp_Delete_{self.sp_entity}(%s, %s)", (parent_id, child_id))
        return True
