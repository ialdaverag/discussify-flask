from flask import Flask
from flask_migrate import Migrate

from config.config import Config

from extensions.database import db
from extensions.jwt import jwt

from routes.auth import black_list
from routes.auth import auth_routes
from routes.user import user_routes
from routes.community import community_routes


def create_app():
    app = Flask(__name__)

    config_app(app)
    register_extensions(app)
    register_blueprints(app)

    return app


def config_app(app):
    app.config.from_object(Config)


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        return jti in black_list


def register_blueprints(app):
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(community_routes, url_prefix='/community')