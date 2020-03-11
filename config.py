from os import environ


class Config(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        environ.get('FLASK_DATABASE_USER', 'flask'),
        environ.get('FLASK_DATABASE_PASSWORD', 'flask'),
        environ.get('FLASK_DATABASE_HOST', 'db'),
        environ.get('FLASK_DATABASE_PORT', 5432),
        environ.get('FLASK_DATABASE_NAME', 'flask')
    )


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
