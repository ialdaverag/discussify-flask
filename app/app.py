from flask import Flask
from flask_migrate import Migrate

from app.config.development import DevelopmentConfig

from app.extensions.database import db
from app.extensions.jwt import jwt
from app.extensions.email import mail
from app.extensions.cors import cors
from app.extensions.socketio import socketio

from app.routes.auth import black_list
from app.routes.auth import auth_routes
from app.routes.user import user_routes
from app.routes.community import community_routes
from app.routes.post import post_routes
from app.routes.comment import comment_routes
from app.routes.notification import notification_routes

from app.models.user import User

from app.errors.errors import ValidationError
from app.errors.errors import NotFoundError
from app.errors.errors import NameError
from app.errors.errors import FollowError
from app.errors.errors import BlockError
from app.errors.errors import SubscriptionError
from app.errors.errors import ModeratorError
from app.errors.errors import BanError
from app.errors.errors import NotInError
from app.errors.errors import OwnershipError
from app.errors.errors import UnauthorizedError
from app.errors.errors import BookmarkError
from app.errors.errors import VoteError

from app.handlers.errors import handler_validation_error
from app.handlers.errors import handler_not_found
from app.handlers.errors import handler_name_error
from app.handlers.errors import handler_follow_error
from app.handlers.errors import handler_block_error
from app.handlers.errors import handler_subscription_error
from app.handlers.errors import handler_moderator_error
from app.handlers.errors import handler_ban_error
from app.handlers.errors import handler_not_in_error
from app.handlers.errors import handler_ownership_error
from app.handlers.errors import handler_unauthorized_error
from app.handlers.errors import handler_bookmark_error
from app.handlers.errors import handler_vote_error


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.sort_keys = False

    register_extensions(app)
    register_blueprints(app)
    register_handlers(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(
        app, 
        supports_credentials=True
    )
    socketio.init_app(app, cors_allowed_origins="*")
    

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]

        return User.query.filter_by(id=identity).one_or_none()


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
    app.register_blueprint(notification_routes, url_prefix='/notification')
    
    # Import socket events to register them
    from app.events import socket_events


def register_handlers(app):
    app.register_error_handler(ValidationError, handler_validation_error)
    app.register_error_handler(NotFoundError, handler_not_found)
    app.register_error_handler(NameError, handler_name_error)
    app.register_error_handler(FollowError, handler_follow_error)
    app.register_error_handler(BlockError, handler_block_error)
    app.register_error_handler(SubscriptionError, handler_subscription_error)
    app.register_error_handler(ModeratorError, handler_moderator_error)
    app.register_error_handler(BanError, handler_ban_error)
    app.register_error_handler(OwnershipError, handler_ownership_error)
    app.register_error_handler(UnauthorizedError, handler_unauthorized_error)
    app.register_error_handler(NotInError, handler_not_in_error)
    app.register_error_handler(BookmarkError, handler_bookmark_error)
    app.register_error_handler(VoteError, handler_vote_error)
