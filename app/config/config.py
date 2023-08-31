import os

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///discussify.db'