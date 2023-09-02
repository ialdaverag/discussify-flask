from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from extensions.database import db

from schemas.community import community_schema
from models.community import Community

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
    
    community = Community(**data)
    community.user_id = current_user

    db.session.add(community)
    db.session.commit()

    return community_schema.dump(community), HTTPStatus.CREATED