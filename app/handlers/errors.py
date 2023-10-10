from http import HTTPStatus

from app.errors.user import UserNotFoundError


def handler_user_not_found(error):
    return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

def handler_user_self_follow(error):
    return {'message': 'You cannot follow yourself'}, HTTPStatus.BAD_REQUEST

def handler_user_already_followed(error):
    return {'message': 'You are already following this user'}, HTTPStatus.BAD_REQUEST
