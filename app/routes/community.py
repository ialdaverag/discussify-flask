from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from extensions.database import db

from models.community import Community
from models.user import User

from schemas.community import community_schema
from schemas.community import communities_schema

community_routes = Blueprint('community_routes', __name__)


@community_routes.route('/', methods=['POST'])
@jwt_required()
def create_community():
    json_data = request.get_json()

    try:
        data = community_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    community = Community.query.filter_by(name=data['name']).first()

    if community:
        return {'message': 'Name already used'}, HTTPStatus.BAD_REQUEST
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    community = Community(**data, user_id=current_user.id)
    community.subscribers.append(current_user)

    db.session.add(community)
    db.session.commit()

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


@community_routes.route('/<string:name>/subscribe', methods=['POST'])
@jwt_required()
def subscribe(name):
    community = Community.query.filter_by(name=name).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user in community.subscribers:
        return {'message': 'User is already subscribed to this community'}, HTTPStatus.BAD_REQUEST

    community.subscribers.append(current_user)
    db.session.commit()

    return {}, HTTPStatus.CREATED