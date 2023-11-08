import os

import datetime

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=1)
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'
    JWT_COOKIE_CSRF_PROTECT = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = True

    CORS_SUPPORTS_CREDENTIALS = True