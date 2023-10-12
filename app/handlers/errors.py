from http import HTTPStatus


def handler_not_found(error):
    return {'message': str(error)}, HTTPStatus.NOT_FOUND


def handler_name_error(error):
    return {'message': str(error)}, HTTPStatus.BAD_REQUEST


def handler_follow_error(error):
    return {'message': str(error)}, HTTPStatus.BAD_REQUEST


def handler_subscription_error(error):
    return {'message': str(error)}, HTTPStatus.BAD_REQUEST


def handler_moderator_error(error):
    return {'message': str(error)}, HTTPStatus.BAD_REQUEST


def handler_ban_error(error):
    return {'message': str(error)}, HTTPStatus.BAD_REQUEST


def handler_ownership_error(error):
    return {'message': str(error)}, HTTPStatus.FORBIDDEN


def handler_unauthorized_error(error):
    return {'message': str(error)}, HTTPStatus.UNAUTHORIZED