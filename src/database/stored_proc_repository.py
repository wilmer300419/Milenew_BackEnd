"""
Capa de acceso a datos basada en STORED PROCEDURES (convencion del proyecto).

La base de datos expone, por entidad:
    sp_Insert_<Entidad>(params...)            -> inserta (no devuelve id)
    sp_Update_<Entidad>(id, params...)        -> actualiza (RAISE si no existe)
    sp_GetAll_<Entidad>(INOUT refcursor)      -> lista los ACTIVOS (REFCURSOR)
    sp_GetById_<Entidad>(id, INOUT refcursor) -> uno por id (REFCURSOR)
    sp_UpdateState_<Entidad>(id, boolean)     -> soft-delete / reactivar

Cada repositorio concreto declara:
    sp_entity     -> nombre de la entidad tal cual en el SP (ej. "Document_Type")
    pk            -> columna llave primaria
    insert_params -> columnas en el ORDEN que las pide sp_Insert
    update_params -> columnas en el ORDEN que las pide sp_Update (despues del id)

Transacciones:
    Todos los metodos aceptan `conn` opcional.
    - Sin conn: abren su propia conexion, hacen commit/rollback y la cierran.
    - Con conn: usan esa conexion y NO hacen commit; quien la abrio (UnitOfWork)
      decide commit o rollback. Asi varias operaciones quedan en UNA transaccion.
"""

from contextlib import contextmanager

from src.database.database import Database


class StoredProcRepository:
    sp_entity = None
    pk = None
    insert_params = []
    update_params = []

    # ------------------------------------------------------------------ #
    # Conexion / transaccion
    # ------------------------------------------------------------------ #
    def _connect(self):
        conn = Database.get_db_connection()
        if conn is None:
            raise ConnectionError("No se pudo establecer conexion con la base de datos.")
        return conn

    @contextmanager
    def _session(self, conn=None):
        if conn is not None:
            # Transaccion externa: la controla el UnitOfWork.
            yield conn
            return
        own = self._connect()
        try:
            yield own
            own.commit()
        except Exception:
            own.rollback()
            raise
        finally:
            own.close()

    @staticmethod
    def _fetch_cursor(conn, call_sql, params, cursor_name):
        """Ejecuta un CALL que abre un REFCURSOR, lee sus filas y lo cierra."""
        with conn.cursor() as cur:
            cur.execute(call_sql, params)
            cur.execute(f'FETCH ALL FROM "{cursor_name}"')
            rows = cur.fetchall()
            # Cerrarlo permite volver a usar el mismo nombre en la misma transaccion.
            cur.execute(f'CLOSE "{cursor_name}"')
            return rows

    # ------------------------------------------------------------------ #
    # Lectura
    # ------------------------------------------------------------------ #
    def find_all(self, conn=None):
        name = f"cur_{self.sp_entity.lower()}"
        with self._session(conn) as c:
            return self._fetch_cursor(c, f"CALL sp_GetAll_{self.sp_entity}(%s)", (name,), name)

    def find_by_id(self, id_value, conn=None):
        name = f"cur_{self.sp_entity.lower()}_by_id"
        with self._session(conn) as c:
            rows = self._fetch_cursor(
                c, f"CALL sp_GetById_{self.sp_entity}(%s, %s)", (id_value, name), name
            )
            return rows[0] if rows else None

    def find_one_by(self, column, value, conn=None):
        """Busca un registro ACTIVO por una columna (no hay SPs de busqueda por campo)."""
        for row in self.find_all(conn=conn):
            if row.get(column) == value:
                return row
        return None

    # ------------------------------------------------------------------ #
    # Escritura
    # ------------------------------------------------------------------ #
    def create(self, data, conn=None):
        values = [data.get(p) for p in self.insert_params]
        placeholders = ", ".join(["%s"] * len(values))
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute(f"CALL sp_Insert_{self.sp_entity}({placeholders})", values)
        # El SP no retorna el id generado; devolvemos el eco de lo insertado.
        return {p: data.get(p) for p in self.insert_params}

    def update(self, id_value, data, conn=None):
        values = [id_value] + [data.get(p) for p in self.update_params]
        placeholders = ", ".join(["%s"] * len(values))
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute(f"CALL sp_Update_{self.sp_entity}({placeholders})", values)
            return self.find_by_id(id_value, conn=c)

    def change_state(self, id_value, state, conn=None):
        with self._session(conn) as c:
            with c.cursor() as cur:
                cur.execute(f"CALL sp_UpdateState_{self.sp_entity}(%s, %s)", (id_value, state))
        return True

    def delete(self, id_value, conn=None):
        """Borrado logico (soft-delete): state = FALSE via sp_UpdateState."""
        return self.change_state(id_value, False, conn=conn)
