from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required

from models.user import User
from schemas.user import user_schema
from schemas.user import users_schema
from schemas.community import communities_schema
from schemas.post import posts_schema

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/<string:username>', methods=['GET'])
@jwt_required(optional=True)
def read_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    return user_schema.dump(user), HTTPStatus.OK


@user_routes.route('/', methods=['GET'])
@jwt_required(optional=True)
def read_users():
    users = User.query.all()

    return users_schema.dump(users), HTTPStatus.OK


@user_routes.route('/<string:username>/subscriptions', methods=['GET'])
@jwt_required(optional=True)
def read_subscriptions(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    return communities_schema.dump(user.subscriptions)


@user_routes.route('/<string:username>/posts', methods=['GET'])
@jwt_required(optional=True)
def read_user_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    return posts_schema.dump(user.posts)