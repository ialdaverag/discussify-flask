from functools import wraps
from flask_jwt_extended import current_user
from app.models.user import Block

def filtered_comments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        comments = func(*args, **kwargs)

        if not current_user:
            return comments

        blocked_users = set(Block.get_blocked(current_user))
        blocking_users = set(Block.get_blockers(current_user))

        if not blocked_users and not blocking_users:
            return comments

        filtered_comments = [
            comment for comment in comments 
            if comment.owner not in blocked_users and comment.owner not in blocking_users
        ]
        return filtered_comments

    return wrapper