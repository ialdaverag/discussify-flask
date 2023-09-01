from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

from marshmallow import ValidationError

from extensions.database import db

from schemas.user import user_schema
from models.user import User

from utils.password import check_password

auth_routes = Blueprint('author_routes', __name__)

black_list = set()


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


@auth_routes.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    
    username = json_data['username']
    password = json_data['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'Incorrect username'}, HTTPStatus.UNAUTHORIZED
    
    if not check_password(password, user.password):
        return {'message': 'Incorrect password'}, HTTPStatus.UNAUTHORIZED
    
    access_token = create_access_token(identity=user.id)
    
    return {'access_token': access_token}, HTTPStatus.OK


@auth_routes.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    black_list.add(jti)

    return {'message': 'Successfully logged out'}, HTTPStatus.OK
