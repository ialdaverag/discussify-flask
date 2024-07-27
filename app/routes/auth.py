from http import HTTPStatus

from werkzeug.http import dump_cookie

from flask import Blueprint
from flask import request
from flask import render_template
from flask import url_for
from flask import make_response
from flask import jsonify
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user

from marshmallow import ValidationError

from app.extensions.database import db

from app.schemas.user import user_schema
from app.schemas.user import login_schema

from app.models.user import User

from app.utils.password import hash_password
from app.utils.password import check_password
from app.utils.email import send_email
from app.utils.token import generate_verification_token
from app.utils.token import confirm_verification_token

auth_routes = Blueprint('auth_routes', __name__)

black_list = set()


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    json_data = request.get_json()

    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not User.is_username_available(username):
        return {'message': 'Username already taken.'}, HTTPStatus.BAD_REQUEST

    if not User.is_email_available(email):
        return {'message': 'Email already taken.'}, HTTPStatus.BAD_REQUEST
    
    user = User(username=username, email=email, password=hash_password(password))

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), HTTPStatus.CREATED


from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies

@auth_routes.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()

    try:
        data = login_schema.load(json_data)
    except Exception as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST

    username = data.get('username')
    password = data.get('password')

    user = User.get_by_username(username)
    
    if not check_password(password, user.password):
        return {'message': 'Incorrect password.'}, HTTPStatus.UNAUTHORIZED
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id) 

    response = make_response(jsonify({'access_token': access_token}), HTTPStatus.OK)

    set_refresh_cookies(response, refresh_token)

    return response


from flask_jwt_extended import unset_jwt_cookies

@auth_routes.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    black_list.add(jti)

    response = make_response({'message': 'Successfully logged out'}, HTTPStatus.OK)

    # Remove JWT cookies
    unset_jwt_cookies(response)

    return response


@auth_routes.route('/refresh', methods=['POST'])
@jwt_required(refresh=True, locations=['cookies'])
def get_new_access_token():
    current_user = get_jwt_identity()

    token = create_access_token(identity=current_user)

    return {'access_token': token}, HTTPStatus.OK


@auth_routes.route('/email/confirm/<string:token>', methods=['GET'])
def confirm_email(token):
    email = confirm_verification_token(token, salt="activate")

    if email is False:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    if user.is_verified is True:
        return {'message': 'The user account is already activated'}, HTTPStatus.BAD_REQUEST
    
    user.is_verified = True
    
    db.session.commit()

    return {'message': 'Email confirmed'}, HTTPStatus.OK