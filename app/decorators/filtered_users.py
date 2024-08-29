# Functools
from functools import wraps

# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Models
from app.models.user import Block
from app.models.community import Community


def filtered_users(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        users = func(*args, **kwargs)

        if not current_user:
            return users

        community = args[0] if args and isinstance(args[0], Community) else None

        if community and current_user:
            if current_user.is_moderator_of(community):
                return users

        blocked_users = set(Block.get_blocked(current_user))
        blocking_users = set(Block.get_blockers(current_user))

        if not blocked_users and not blocking_users:
            return users

        filtered_users = [
            user for user in users 
            if user not in blocked_users and user not in blocking_users
        ]
        return filtered_users

    return wrapper