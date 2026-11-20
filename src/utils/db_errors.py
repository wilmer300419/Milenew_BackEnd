"""
Traduce errores de PostgreSQL (psycopg2) a las excepciones de dominio del
proyecto, que index.py ya convierte en respuestas JSON con su codigo HTTP.

    UniqueViolation      -> ConflictError (409)
    ForeignKeyViolation  -> ValueError    (400)  "alguna referencia no existe"
    CheckViolation       -> ValueError    (400)
    RaiseException (RAISE EXCEPTION dentro de un SP):
        mensaje con "not found" -> NotFoundError (404)
        cualquier otro          -> ValueError    (400)  ej. "Insufficient balance"
"""

from functools import wraps

import psycopg2

from src.utils.errors import NotFoundError, ConflictError


def translate_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except psycopg2.errors.UniqueViolation:
            raise ConflictError("Ya existe un registro con ese valor unico.")
        except psycopg2.errors.ForeignKeyViolation:
            raise ValueError("Alguna referencia (llave foranea) no existe o esta en uso.")
        except psycopg2.errors.CheckViolation:
            raise ValueError("Los datos no cumplen una restriccion de la base de datos.")
        except psycopg2.errors.RaiseException as e:
            msg = (e.diag.message_primary or str(e)).strip()
            if "not found" in msg.lower():
                raise NotFoundError(msg)
            raise ValueError(msg)
    return wrapper
