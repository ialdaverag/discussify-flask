# HTTP
from http import HTTPStatus

# Flask
from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

# Marshmallow
from marshmallow import ValidationError

# Models
from app.models.community import Community
from app.models.user import User

# Managers
from app.managers.community import CommunityManager
from app.managers.community import SubscriptionManager
from app.managers.community import ModerationManager
from app.managers.community import BanManager
from app.managers.community import TransferManager
from app.managers.post import PostManager

# Schemas
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

    community = CommunityManager.create(current_user, data)

    return community_schema.dump(community), HTTPStatus.CREATED


@community_routes.get('/<string:name>')
@jwt_required(optional=True)
def read_community(name):
    community = Community.get_by_name(name)
    
    CommunityManager.read(name)

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.get('/')
@jwt_required(optional=True)
def read_communities():
    communities = CommunityManager.read_all()

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
    
    community = CommunityManager.update(current_user, community, data)

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.delete('/<string:name>')
@jwt_required()
def delete_community(name):
    community = Community.get_by_name(name=name)

    CommunityManager.delete(current_user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/subscribe')
@jwt_required()
def subscribe(name):
    community = Community.get_by_name(name)

    SubscriptionManager.create(current_user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/unsubscribe')
@jwt_required()
def unsubscribe(name):
    community = Community.get_by_name(name)

    SubscriptionManager.delete(current_user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/mod/<string:username>')
@jwt_required()
def mod(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    ModerationManager.create(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/unmod/<string:username>')
@jwt_required()
def unmod(name, username):
    community = Community.get_by_name(name)

    user = User.get_by_username(username)

    ModerationManager.delete(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/ban/<string:username>')
@jwt_required()
def ban(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    BanManager.create(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/unban/<string:username>')
@jwt_required()
def unban(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    BanManager.delete(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/transfer/<string:username>')
@jwt_required()
def transfer(name, username):
    community = Community.get_by_name(name=name)
    
    user = User.get_by_username(username=username)
    
    TransferManager.create(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.get('/<string:name>/subscribers')
@jwt_required(optional=True)
def read_subscribers(name):
    community = Community.get_by_name(name)

    subscribers = SubscriptionManager.read_subscribers_by_community(community)

    return users_schema.dump(subscribers), HTTPStatus.OK


@community_routes.get('/<string:name>/moderators')
@jwt_required(optional=True)
def read_moderators(name):
    community = Community.get_by_name(name)

    moderators = ModerationManager.read_moderators_by_community(community)

    return users_schema.dump(moderators), HTTPStatus.OK


@community_routes.get('/<string:name>/banned')
@jwt_required(optional=True)
def read_banned(name):
    community = Community.get_by_name(name)

    banned = BanManager.read_bans_by_community(community)

    return users_schema.dump(banned), HTTPStatus.OK


@community_routes.get('/<string:name>/posts')
@jwt_required(optional=True)
def read_community_posts(name):
    community = Community.get_by_name(name)

    posts = PostManager.read_all_by_community(community)
    
    return posts_schema.dump(posts), HTTPStatus.OK