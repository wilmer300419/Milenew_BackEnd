"""Validaciones pequenas para cuerpos JSON (lanzan ValueError -> HTTP 400)."""

from datetime import date, time
from decimal import Decimal, InvalidOperation


def text(data, key, max_len, required=True):
    value = data.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            raise ValueError(f"El campo '{key}' es obligatorio.")
        return None
    if not isinstance(value, str):
        raise ValueError(f"El campo '{key}' debe ser texto.")
    value = value.strip()
    if len(value) > max_len:
        raise ValueError(f"El campo '{key}' no puede superar {max_len} caracteres.")
    return value


def integer(data, key, min_value=1, required=True):
    value = data.get(key)
    if value is None or value == "":
        if required:
            raise ValueError(f"El campo '{key}' es obligatorio.")
        return None
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError(f"El campo '{key}' debe ser un entero.")
    try:
        value = int(value)
    except ValueError:
        raise ValueError(f"El campo '{key}' debe ser un entero.")
    if value < min_value:
        raise ValueError(f"El campo '{key}' debe ser mayor o igual a {min_value}.")
    return value


def number(data, key, required=True):
    value = data.get(key)
    if value is None or value == "":
        if required:
            raise ValueError(f"El campo '{key}' es obligatorio.")
        return None
    if isinstance(value, bool):
        raise ValueError(f"El campo '{key}' debe ser numerico.")
    try:
        return Decimal(str(value))
    except InvalidOperation:
        raise ValueError(f"El campo '{key}' debe ser numerico.")


def iso_date(value, key, required=True):
    if value in (None, ""):
        if required:
            raise ValueError(f"El campo '{key}' es obligatorio (AAAA-MM-DD).")
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f"El campo '{key}' debe tener el formato AAAA-MM-DD.")


def iso_time(value, key, required=True):
    if value in (None, ""):
        if required:
            raise ValueError(f"El campo '{key}' es obligatorio (HH:MM o HH:MM:SS).")
        return None
    if isinstance(value, time):
        return value
    try:
        return time.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f"El campo '{key}' debe tener el formato HH:MM o HH:MM:SS.")
