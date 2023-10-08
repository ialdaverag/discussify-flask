from .config import Config


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///discussify.db'