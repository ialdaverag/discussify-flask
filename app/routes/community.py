from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from app.extensions.database import db

from app.models.community import Community
from app.models.user import User

from app.schemas.community import community_schema
from app.schemas.community import communities_schema
from app.schemas.user import users_schema
from app.schemas.post import posts_schema

community_routes = Blueprint('community_routes', __name__)


@community_routes.route('/', methods=['POST'])
@jwt_required()
def create_community():
    json_data = request.get_json()

    try:
        data = community_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    community = current_user.create_community(**data)

    return community_schema.dump(community), HTTPStatus.CREATED


@community_routes.route('/<string:name>', methods=['GET'])
@jwt_required(optional=True)
def read_community(name):
    community = Community.get_by_name(name)

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.route('/', methods=['GET'])
@jwt_required(optional=True)
def read_communities():
    communities = Community.get_all()

    return communities_schema.dump(communities), HTTPStatus.OK


@community_routes.route('/<string:name>', methods=['PATCH'])
@jwt_required()
def update_community(name):
    community = Community.get_by_name(name=name)
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    json_data = request.get_json()

    try:
        data = community_schema.load(json_data, partial=('name',))
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    new_name = data.get('name')
    new_about = data.get('about')
    
    current_user.update_community(community, name=new_name, about=new_about)

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.route('/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_community(name):
    community = Community.get_by_name(name=name)

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    current_user.delete_community(community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/subscribe', methods=['POST'])
@jwt_required()
def subscribe(name):
    community = Community.get_by_name(name)
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    current_user.subscribe_to(community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/subscribers', methods=['GET'])
@jwt_required(optional=True)
def read_subscribers(name):
    community = Community.get_by_name(name)

    return users_schema.dump(community.subscribers), HTTPStatus.OK


@community_routes.route('/<string:name>/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe(name):
    community = Community.get_by_name(name)

    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    current_user.unsubscribe_to(community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/mod/<string:username>', methods=['POST'])
@jwt_required()
def mod(name, username):
    community = Community.get_by_name(name)

    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)
    
    user = User.get_by_username(username)
    
    current_user.appoint_moderator(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/moderators', methods=['GET'])
@jwt_required(optional=True)
def read_moderators(name):
    community = Community.get_by_name(name)

    return users_schema.dump(community.moderators), HTTPStatus.OK


@community_routes.route('/<string:name>/unmod/<string:username>', methods=['POST'])
@jwt_required()
def unmod(name, username):
    community = Community.get_by_name(name)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    user = User.get_by_username(username)

    current_user.dismiss_moderator(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/ban/<string:username>', methods=['POST'])
@jwt_required()
def ban(name, username):
    community = Community.get_by_name(name)
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)
    
    user = User.get_by_username(username)
    
    current_user.ban_from(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/banned', methods=['GET'])
@jwt_required()
def read_banned(name):
    community = Community.get_by_name(name)

    return users_schema.dump(community.banned), HTTPStatus.OK


@community_routes.route('/<string:name>/unban/<string:username>', methods=['POST'])
@jwt_required()
def unban(name, username):
    community = Community.get_by_name(name)
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)
    
    user = User.get_by_username(username)
    
    current_user.unban_from(user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/transfer/<string:username>', methods=['POST'])
@jwt_required()
def transfer(name, username):
    community = Community.get_by_name(name=name)
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    user = User.get_by_username(username=username)
    
    current_user.transfer_community(community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/posts', methods=['GET'])
@jwt_required(optional=True)
def read_community_posts(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    return posts_schema.dump(community.posts), HTTPStatus.OK