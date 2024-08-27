from functools import wraps
from flask_jwt_extended import current_user
from app.models.user import Block

def filtered_posts(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        posts = func(*args, **kwargs)

        if not current_user:
            return posts

        blocked_users = set(Block.get_blocked(current_user))
        blocking_users = set(Block.get_blockers(current_user))

        if not blocked_users and not blocking_users:
            return posts

        filtered_posts = [
            post for post in posts 
            if post.owner not in blocked_users and post.owner not in blocking_users
        ]
        return filtered_posts

    return wrapper