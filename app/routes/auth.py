# HTTP
from http import HTTPStatus

# Flask
from flask import Blueprint
from flask import request
from flask import make_response
from flask import jsonify
from flask import url_for
from flask import render_template

# Flask JWT Extended
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies

# Marshmallow
from marshmallow import ValidationError

# Extensions
from app.extensions.database import db

# Schemas
from app.schemas.user import user_schema
from app.schemas.user import login_schema

# Models
from app.models.user import User

# Managers
from app.managers.user import UserManager

# Utils
from app.utils.password import check_password
from app.utils.email import send_email
from app.utils.token import generate_verification_token
from app.utils.token import confirm_verification_token

auth_routes = Blueprint('auth_routes', __name__)

black_list = set()


@auth_routes.post('/signup')
def sign_up():
    json_data = request.get_json()

    data = user_schema.load(json_data)

    user = UserManager.create(data)

    token = generate_verification_token(user.email, salt='activate')
    subject = 'Please confirm your registration'
    link = url_for('auth_routes.confirm_email', token=token, _external=True)

    send_email(
        to=user.email, 
        subject=subject, 
        template=render_template('email/confirmation.html', link=link)
    )

    return user_schema.dump(user), HTTPStatus.CREATED


@auth_routes.post('/login')
def log_in():
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


@auth_routes.post('/logout')
@jwt_required()
def log_out():
    jti = get_jwt()["jti"]
    black_list.add(jti)

    response = make_response({'message': 'Successfully logged out.'}, HTTPStatus.OK)

    unset_jwt_cookies(response)

    return response


@auth_routes.post('/refresh')
@jwt_required(refresh=True, locations=['cookies'])
def get_new_access_token():
    current_user = get_jwt_identity()

    token = create_access_token(identity=current_user)

    return {'access_token': token}, HTTPStatus.OK


@auth_routes.get('/email/confirm/<string:token>')
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