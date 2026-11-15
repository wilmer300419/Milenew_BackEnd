"""Excepciones de dominio que las rutas mapean a codigos HTTP."""


class NotFoundError(Exception):
    """El recurso solicitado no existe (-> 404)."""


class ConflictError(Exception):
    """Conflicto de datos, p. ej. un valor unico duplicado (-> 409)."""


class NotConfiguredError(Exception):
    """Falta un dato de configuracion en la DB, p. ej. el rol 'Pasajero' (-> 503)."""


class ForbiddenError(Exception):
    """El usuario esta autenticado pero no puede hacer esto (-> 403)."""
