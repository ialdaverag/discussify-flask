# config
from .config import Config


class TestingConfig(Config):
    # Flask
    TESTING = True

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///discussify.db'