from functools import wraps
from flask_jwt_extended import current_user
from app.models.user import Block

def filtered_users(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        users = func(*args, **kwargs)

        if not current_user:
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