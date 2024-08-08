from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import current_user

from marshmallow import ValidationError

from app.extensions.database import db

from app.models.community import Community
from app.models.user import User

from app.schemas.community import community_schema
from app.schemas.community import communities_schema
from app.schemas.user import users_schema
from app.schemas.post import posts_schema

community_routes = Blueprint('community_routes', __name__)


@community_routes.post('/')
@jwt_required()
def create_community():
    json_data = request.get_json()

    try:
        data = community_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST

    community = current_user.create_community(**data)

    return community_schema.dump(community), HTTPStatus.CREATED


@community_routes.get('/<string:name>')
@jwt_required(optional=True)
def read_community(name):
    community = Community.get_by_name(name)

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.get('/')
@jwt_required(optional=True)
def read_communities():
    communities = Community.get_all()

    return communities_schema.dump(communities), HTTPStatus.OK


@community_routes.patch('/<string:name>')
@jwt_required()
def update_community(name):
    community = Community.get_by_name(name=name)

    json_data = request.get_json()

    try:
        data = community_schema.load(json_data, partial=('name',))
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    new_name = data.get('name')
    new_about = data.get('about')
    
    current_user.update_community(community, name=new_name, about=new_about)

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.delete('/<string:name>')
@jwt_required()
def delete_community(name):
    community = Community.get_by_name(name=name)

    current_user.delete_community(community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/subscribe')
@jwt_required()
def subscribe(name):
    community = Community.get_by_name(name)

    current_user.subscribe_to(community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.get('/<string:name>/subscribers')
@jwt_required(optional=True)
def read_subscribers(name):
    community = Community.get_by_name(name)

    only_subscribers = set(community.subscribers) - set(community.moderators) - set(community.banned)

    return users_schema.dump(only_subscribers), HTTPStatus.OK


@community_routes.post('/<string:name>/unsubscribe')
@jwt_required()
def unsubscribe(name):
    community = Community.get_by_name(name)

    current_user.unsubscribe_to(community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/mod/<string:username>')
@jwt_required()
def mod(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    current_user.appoint_moderator(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.get('/<string:name>/moderators')
@jwt_required(optional=True)
def read_moderators(name):
    community = Community.get_by_name(name)

    return users_schema.dump(community.moderators), HTTPStatus.OK


@community_routes.post('/<string:name>/unmod/<string:username>')
@jwt_required()
def unmod(name, username):
    community = Community.get_by_name(name)

    user = User.get_by_username(username)

    current_user.dismiss_moderator(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/ban/<string:username>')
@jwt_required()
def ban(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    current_user.ban_from(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.get('/<string:name>/banned')
@jwt_required(optional=True)
def read_banned(name):
    community = Community.get_by_name(name)

    return users_schema.dump(community.banned), HTTPStatus.OK


@community_routes.post('/<string:name>/unban/<string:username>')
@jwt_required()
def unban(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    current_user.unban_from(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/transfer/<string:username>')
@jwt_required()
def transfer(name, username):
    community = Community.get_by_name(name=name)
    
    user = User.get_by_username(username=username)
    
    current_user.transfer_community(community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.get('/<string:name>/posts')
@jwt_required(optional=True)
def read_community_posts(name):
    community = Community.get_by_name(name)
    
    return posts_schema.dump(community.posts), HTTPStatus.OK