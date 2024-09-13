import os
import datetime

from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Flask-JWT-Extended
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'

    # Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = True