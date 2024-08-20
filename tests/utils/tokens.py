# Flask-JWT-Extended
from flask_jwt_extended import create_access_token

def get_access_token(user):
    return create_access_token(identity=user.id)