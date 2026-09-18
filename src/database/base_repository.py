"""
Capa base de acceso a datos (patron Repository).

Cada repositorio concreto define:
    table   -> nombre de la tabla
    pk      -> columna llave primaria
    columns -> columnas insertables/actualizables (sin la PK)

Los nombres de tabla/columna vienen del propio codigo (no del usuario),
por eso se interpolan; los VALORES siempre van parametrizados (%s) para
evitar inyeccion SQL. Usa RealDictCursor, asi que las filas vuelven como
diccionarios listos para JSON.
"""

from src.database.database import Database


class BaseRepository:
    table = None
    pk = None
    columns = []

    def _connect(self):
        conn = Database.get_db_connection()
        if conn is None:
            raise ConnectionError("No se pudo establecer conexion con la base de datos.")
        return conn

    def find_all(self):
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.table} ORDER BY {self.pk}")
                return cur.fetchall()
        finally:
            conn.close()

    def find_by_id(self, id_value):
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.table} WHERE {self.pk} = %s", (id_value,))
                return cur.fetchone()
        finally:
            conn.close()

    def find_one_by(self, column, value):
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.table} WHERE {column} = %s", (value,))
                return cur.fetchone()
        finally:
            conn.close()

    def create(self, data):
        cols = [c for c in self.columns if c in data]
        placeholders = ", ".join(["%s"] * len(cols))
        col_sql = ", ".join(cols)
        values = [data[c] for c in cols]
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {self.table} ({col_sql}) VALUES ({placeholders}) RETURNING *",
                    values,
                )
                row = cur.fetchone()
                conn.commit()
                return row
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update(self, id_value, data):
        cols = [c for c in self.columns if c in data]
        if not cols:
            return self.find_by_id(id_value)
        set_sql = ", ".join(f"{c} = %s" for c in cols)
        values = [data[c] for c in cols] + [id_value]
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE {self.table} SET {set_sql} WHERE {self.pk} = %s RETURNING *",
                    values,
                )
                row = cur.fetchone()
                conn.commit()
                return row
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def delete(self, id_value):
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {self.table} WHERE {self.pk} = %s", (id_value,))
                deleted = cur.rowcount
                conn.commit()
                return deleted > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
