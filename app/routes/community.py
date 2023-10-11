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
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    return community_schema.dump(community), HTTPStatus.OK


@community_routes.route('/', methods=['GET'])
@jwt_required(optional=True)
def read_communities():
    communities = Community.query.all()

    return communities_schema.dump(communities), HTTPStatus.OK


@community_routes.route('/<string:name>', methods=['PATCH'])
@jwt_required()
def update_community(name):
    community = Community.get_by_name(name=name)
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user.id != community.user_id:
        return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
    
    json_data = request.get_json()

    try:
        data = community_schema.load(json_data, partial=('name',))
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    new_name = data.get('name')

    if new_name is not None:
        existing_community = Community.query.filter_by(name=new_name).first()
        
        if existing_community and existing_community != community:
            return {'message': 'Name already used'}, HTTPStatus.BAD_REQUEST
        
        community.name = new_name

    community.about = data.get('about') or community.about

    db.session.commit()
    
    return community_schema.dump(community), HTTPStatus.OK


@community_routes.route('/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_community(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user.id != community.user_id:
        return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
    
    db.session.delete(community)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/subscribe', methods=['POST'])
@jwt_required()
def subscribe(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user in community.subscribers:
        return {'message': 'You are already subscribed to this community'}, HTTPStatus.BAD_REQUEST

    community.subscribers.append(current_user)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/subscribers', methods=['GET'])
@jwt_required(optional=True)
def read_subscribers(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND

    return users_schema.dump(community.subscribers), HTTPStatus.OK


@community_routes.route('/<string:name>/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()

    if current_user == community.user_id:
        return {'message': 'You are the owner of this community and cannot unsubscribe'}, HTTPStatus.BAD_REQUEST
    
    current_user = User.query.get(current_user)

    if current_user not in community.subscribers:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST
    
    if current_user in community.moderators:
        community.moderators.remove(current_user)
    
    community.subscribers.remove(current_user)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/mod/<string:username>', methods=['POST'])
@jwt_required()
def mod(name, username):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user not in community.moderators:
        return {'message': 'You are not a moderator of this community'}, HTTPStatus.UNAUTHORIZED
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    # What if target user is banned?
    if user in community.banned:
        return {'message': 'User is banned from this community'}, HTTPStatus.BAD_REQUEST
    
    if user not in community.subscribers:
        return {'message': 'User is not subscribed to this community'}, HTTPStatus.BAD_REQUEST

    if user in community.moderators:
        return {'message': 'User is already a moderator of this community'}, HTTPStatus.BAD_REQUEST
    
    community.moderators.append(user)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/moderators', methods=['GET'])
@jwt_required(optional=True)
def read_moderators(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND

    return users_schema.dump(community.moderators), HTTPStatus.OK


@community_routes.route('/<string:name>/unmod/<string:username>', methods=['POST'])
@jwt_required()
def unmod(name, username):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()

    if current_user == community.user_id:
        return {'message': 'You are the owner of this community and cannot unmod'}, HTTPStatus.BAD_REQUEST
    
    current_user = User.query.get(current_user)

    if current_user not in community.moderators:
        return {'message': 'You are not a moderator of this community'}, HTTPStatus.UNAUTHORIZED
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    if user.id == community.user_id:
        return {'message': 'User is the owner of this community'}, HTTPStatus.BAD_REQUEST
    
    if user not in community.moderators:
        return {'message': 'User is not a moderator of this community'}, HTTPStatus.BAD_REQUEST
    
    community.moderators.remove(user)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/ban/<string:username>', methods=['POST'])
@jwt_required()
def ban(name, username):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user not in community.moderators:
        return {'message': 'You are not a moderator of this community'}, HTTPStatus.UNAUTHORIZED
    
    user = User.query.filter_by(username=username).first()

    if current_user is user:
        return {'message': 'User cannot ban themselves'}, HTTPStatus.BAD_REQUEST
    
    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    if user in community.banned:
        return {'message': 'User is already banned from this community'}, HTTPStatus.BAD_REQUEST
    
    if user.id == community.user_id:
        return {'message': 'User is the owner of this community'}, HTTPStatus.BAD_REQUEST
    
    if user not in community.subscribers:
        return {'message': 'User is not subscribed to this community'}, HTTPStatus.BAD_REQUEST
    
    if user in community.moderators:
        community.moderators.remove(user)
    
    community.append_subscriber(user)
    community.append_moderator(user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/banned', methods=['GET'])
@jwt_required(optional=True)
def read_banned(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND

    return users_schema.dump(community.banned), HTTPStatus.OK


@community_routes.route('/<string:name>/unban/<string:username>', methods=['POST'])
@jwt_required()
def unban(name, username):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user not in community.moderators:
        return {'message': 'You are not a moderator of this community'}, HTTPStatus.UNAUTHORIZED
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    if user not in community.banned:
        return {'message': 'User is not banned from this community.'}, HTTPStatus.BAD_REQUEST
    
    community.banned.remove(user)
    community.subscribers.append(user)

    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/transfer/<string:username>', methods=['POST'])
@jwt_required()
def transfer(name, username):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    
    if current_user != community.user_id:
        return {'message': 'You are not the owner of this community'}, HTTPStatus.BAD_REQUEST
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    if user not in community.subscribers:
        return {'message': 'User is not subscribed to this community'}, HTTPStatus.BAD_REQUEST
    
    if user not in community.moderators:
        community.moderators.append(user)
    
    community.user_id = user.id
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@community_routes.route('/<string:name>/posts', methods=['GET'])
@jwt_required(optional=True)
def read_community_posts(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    return posts_schema.dump(community.posts), HTTPStatus.OK