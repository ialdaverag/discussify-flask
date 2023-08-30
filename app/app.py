from flask import Flask

from config.config import Config


def create_app():
    app = Flask(__name__)

    config_app(app)

    return app


def config_app(app):
    app.config.from_object(Config)