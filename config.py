from decouple import config

class Config:
    """Base application configuration class."""
    SECRET_KEY = config('SECRET_KEY', default='dev_secret_key')
    DEBUG = config('DEBUG', default=False, cast=bool)
    PORT = config('PORT', default=5000, cast=int)


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False


# Dictionary mapping environment names to configuration objects
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}