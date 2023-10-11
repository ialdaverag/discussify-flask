class CommunityNotFoundError(Exception):
    pass


class CommunityNameAlreadyUsedError(Exception):
    pass


class CommunityBelongsToUserError(Exception):
    pass


class CommunityNotBelongsToUserError(Exception):
    pass