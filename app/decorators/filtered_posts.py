# Functools
from functools import wraps

# Inspect
import inspect

# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Models
from app.models.user import Block


def filtered_posts(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        posts = func(*args, **kwargs)

        if not current_user:
            return posts
        
        signature = inspect.signature(func)

        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        community = None

        if 'community' in bound_arguments.arguments:
            community = bound_arguments.arguments['community']
            
        if community and current_user.is_moderator_of(community):
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