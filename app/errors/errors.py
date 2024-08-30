from marshmallow import ValidationError

class NotFoundError(Exception):
    pass


class NameError(Exception):
    pass


class FollowError(Exception):
    pass


class BlockError(Exception):
    pass


class BanError(Exception):
    pass


class NotInError(Exception):
    pass


class ModeratorError(Exception):
    pass


class OwnershipError(Exception):
    pass


class SubscriptionError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class BookmarkError(Exception):
    pass


class VoteError(Exception):
    pass