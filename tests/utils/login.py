from flask_jwt_extended import create_access_token

def login(user):
    return create_access_token(identity=user.id)