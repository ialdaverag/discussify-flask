class UserNotFoundError(Exception):
    pass


class UserSelfFollowError(Exception):
    pass


class UserAlreadyFollowedError(Exception):
    pass


class UserSelfUnfollowError(Exception):
    pass


class UserNotFollowedError(Exception):
    pass


class UserBannedError(Exception):
    pass


class UserAlreadySubscribedError(Exception):
    pass