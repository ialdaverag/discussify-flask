import os

import datetime

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = True