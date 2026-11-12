"""
Emision y verificacion de tokens JWT (stateless).

El token se firma con SECRET_KEY (del .env) y lleva dentro el id del usuario,
su username y su rol. El front lo guarda tras el login y lo envia en cada
peticion protegida como:  Authorization: Bearer <token>
"""

import datetime
import jwt
from decouple import config

SECRET = config("SECRET_KEY", default="dev_secret_key")
ALGORITHM = "HS256"
EXPIRES_MINUTES = config("TOKEN_EXPIRES_MIN", default=120, cast=int)


def generate_token(user):
    """Crea un JWT a partir de un usuario (dict con id_user, username, id_rol_fk)."""
    now = datetime.datetime.utcnow()
    payload = {
        "sub": str(user.get("id_user")),   # PyJWT exige que 'sub' sea string
        "username": user.get("username"),
        "id_rol": user.get("id_rol_fk"),
        "iat": now,
        "exp": now + datetime.timedelta(minutes=EXPIRES_MINUTES),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def decode_token(token):
    """Devuelve el contenido del token o lanza jwt.* si es invalido/expirado."""
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
