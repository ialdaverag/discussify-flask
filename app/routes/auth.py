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
from app.models.user import User

from app.utils.password import check_password
from app.utils.email import send_email
from app.utils.token import generate_verification_token
from app.utils.token import confirm_verification_token

auth_routes = Blueprint('auth_routes', __name__)

black_list = set()


@auth_routes.route('/signup', methods=['POST'])
def signup():
    json_data = request.get_json()

    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    user = User.is_username_available(data['username'])

    if not user:
        return {'message': 'Username already used'}, HTTPStatus.BAD_REQUEST
    
    email = User.is_email_available(data['email'])

    if not email:
        return {'message': 'Email already used'}, HTTPStatus.BAD_REQUEST
    
    user = User(**data)

    '''
    token = generate_verification_token(user.email, salt='activate')
    subject = 'Please confirm your registration'
    link = url_for('auth_routes.confirm_email', token=token, _external=True)

    send_email(
        to=user.email, 
        subject=subject, 
        template=render_template('email/confirmation.html', link=link)
    )
    '''

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), HTTPStatus.CREATED


@auth_routes.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()

    if 'username' not in json_data:
        return {'message': 'Username required'}, HTTPStatus.BAD_REQUEST

    if 'password' not in json_data:
        return {'message': 'Password required'}, HTTPStatus.BAD_REQUEST
    
    username = json_data['username']

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'Incorrect username'}, HTTPStatus.UNAUTHORIZED
    
    password = json_data['password']
    
    if not check_password(password, user.password):
        return {'message': 'Incorrect password'}, HTTPStatus.UNAUTHORIZED
    
    '''
    if user.is_verified is False:
            return {'message': 'The user account is not activated yet'}, HTTPStatus.FORBIDDEN
    '''
    
    access_token = create_access_token(identity=user.id) 
    refresh_token = create_refresh_token(identity=user.id)  

    return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


@auth_routes.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    black_list.add(jti)

    return {'message': 'Successfully logged out'}, HTTPStatus.OK


@auth_routes.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def get_new_access_token():
    print('pidiendo nuevo access token')
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