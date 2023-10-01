from flask import Flask
from flask_migrate import Migrate

from app.config.development import DevelopmentConfig

from app.extensions.database import db
from app.extensions.jwt import jwt
from app.extensions.email import mail

from app.routes.auth import black_list
from app.routes.auth import auth_routes
from app.routes.user import user_routes
from app.routes.community import community_routes
from app.routes.post import post_routes
from app.routes.comment import comment_routes


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        return jti in black_list


def register_blueprints(app):
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(community_routes, url_prefix='/community')
    app.register_blueprint(post_routes, url_prefix='/post')
    app.register_blueprint(comment_routes, url_prefix='/comment')