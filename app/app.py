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

from app.errors.user import UserNotFoundError
from app.errors.user import UserSelfFollowError
from app.errors.user import UserAlreadyFollowedError
from app.errors.user import UserSelfUnfollowError
from app.errors.user import UserNotFollowedError
from app.errors.community import CommunityNotFoundError
from app.errors.community import CommunityNameAlreadyUsedError
from app.errors.community import CommunityNotBelongsToUserError

from app.handlers.errors import handler_user_not_found
from app.handlers.errors import handler_user_self_follow
from app.handlers.errors import handler_user_already_followed
from app.handlers.errors import handler_user_self_unfollow
from app.handlers.errors import handler_user_not_followed
from app.handlers.errors import handler_community_not_found
from app.handlers.errors import handler_community_name_already_exists
from app.handlers.errors import handler_community_not_belongs_to_user


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)
    register_handlers(app)

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


def register_handlers(app):
    app.register_error_handler(UserNotFoundError, handler_user_not_found)
    app.register_error_handler(UserSelfFollowError, handler_user_self_follow)
    app.register_error_handler(UserAlreadyFollowedError, handler_user_already_followed)
    app.register_error_handler(UserSelfUnfollowError, handler_user_self_unfollow)
    app.register_error_handler(UserNotFollowedError, handler_user_not_followed)
    app.register_error_handler(CommunityNotFoundError, handler_community_not_found)
    app.register_error_handler(CommunityNameAlreadyUsedError, handler_community_name_already_exists)
    app.register_error_handler(CommunityNotBelongsToUserError, handler_community_not_belongs_to_user)