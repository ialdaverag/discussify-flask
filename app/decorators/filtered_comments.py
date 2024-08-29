# Functools
from functools import wraps

# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Models
from app.models.user import Block


def filtered_comments(func):
    from app.models.post import Post

    @wraps(func)
    def wrapper(*args, **kwargs):
        comments = func(*args, **kwargs)

        if not current_user:
            return comments

        post = args[0] if args and isinstance(args[0], Post) else None
        community = post.community if post else None
        
        if community and current_user.is_moderator_of(community):
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
