from http import HTTPStatus


def handler_user_not_found(error):
    return {'message': 'User not found'}, HTTPStatus.NOT_FOUND


def handler_user_self_follow(error):
    return {'message': 'You cannot follow yourself'}, HTTPStatus.BAD_REQUEST


def handler_user_already_followed(error):
    return {'message': 'You are already following this user'}, HTTPStatus.BAD_REQUEST


def handler_user_self_unfollow(error):
    return {'message': 'You cannot unfollow yourself'}, HTTPStatus.BAD_REQUEST


def handler_user_not_followed(error):
    return {'message': 'You are not following this user'}, HTTPStatus.BAD_REQUEST


def handler_community_name_already_exists(error):
    return {'message': 'Name already used'}, HTTPStatus.BAD_REQUEST
