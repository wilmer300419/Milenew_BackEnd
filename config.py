from decouple import config

# Clave minima recomendada para firmar los tokens (HS256): 32 caracteres.
MIN_SECRET_KEY_LENGTH = 32
DEV_SECRET_KEY = "dev_secret_key_solo_para_desarrollo"

# Entorno de ejecucion, se elige en el .env:  APP_ENV=development | production
APP_ENV = config("APP_ENV", default="development").strip().lower()


class Config:
    """Base application configuration class."""
    SECRET_KEY = config("SECRET_KEY", default=DEV_SECRET_KEY)
    DEBUG = config("DEBUG", default=False, cast=bool)
    PORT = config("PORT", default=5000, cast=int)


class DevelopmentConfig(Config):
    """Desarrollo local: DEBUG encendido (recarga automatica y depurador)."""
    DEBUG = True


class ProductionConfig(Config):
    """Produccion: DEBUG SIEMPRE apagado (el depurador de Flask permite ejecutar codigo)."""
    DEBUG = False


# Dictionary mapping environment names to configuration objects
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def validate_secret_key(app_config):
    """
    En produccion exige una SECRET_KEY propia y larga; en desarrollo solo avisa.
    Generar una:  python -c "import secrets; print(secrets.token_hex(32))"
    """
    key = app_config.get("SECRET_KEY") or ""
    weak = key == DEV_SECRET_KEY or len(key) < MIN_SECRET_KEY_LENGTH
    if not weak:
        return
    message = (
        f"SECRET_KEY insegura (minimo {MIN_SECRET_KEY_LENGTH} caracteres y distinta de la de desarrollo). "
        'Genera una con: python -c "import secrets; print(secrets.token_hex(32))" y ponla en el .env.'
    )
    if not app_config.get("DEBUG"):
        raise RuntimeError(message)
    print(f"Aviso: {message}")
