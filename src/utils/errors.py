"""Excepciones de dominio que las rutas mapean a codigos HTTP."""


class NotFoundError(Exception):
    """El recurso solicitado no existe (-> 404)."""


class ConflictError(Exception):
    """Conflicto de datos, p. ej. un valor unico duplicado (-> 409)."""
