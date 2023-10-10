from http import HTTPStatus

from app.errors.user import UserNotFoundError


def handler_user_not_found(error):
    return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
