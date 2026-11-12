"""
Unit of Work: agrupa varias operaciones de distintos repositorios en UNA
sola transaccion. Si cualquier paso falla, se deshace todo (rollback).

Uso:
    with UnitOfWork() as conn:
        person_repo.create(person_data, conn=conn)
        user_repo.create(user_data, conn=conn)
    # Al salir sin errores -> commit. Con error -> rollback y se relanza.
"""

from src.database.database import Database


class UnitOfWork:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = Database.get_db_connection()
        if self.conn is None:
            raise ConnectionError("No se pudo establecer conexion con la base de datos.")
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            self.conn.close()
        return False  # no se "traga" la excepcion: sigue hacia el manejador HTTP
