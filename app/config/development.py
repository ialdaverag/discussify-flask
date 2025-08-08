# OS
import os

# config
from .config import Config


class DevelopmentConfig(Config):
    # Flask
    DEBUG = True

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')