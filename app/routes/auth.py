from http import HTTPStatus

from flask import Blueprint
from flask import request

from marshmallow import ValidationError

from extensions.database import db

from schemas.user import user_schema
from models.user import User

auth_routes = Blueprint('author_routes', __name__)


@auth_routes.route('/signup', methods=['POST'])
def signup():
    json_data = request.get_json()

    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    user = User.query.filter_by(username=data['username']).first()

    if user:
        return {'message': 'Username already used'}, HTTPStatus.BAD_REQUEST
    
    user = User(**data)
    
    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), HTTPStatus.CREATED
