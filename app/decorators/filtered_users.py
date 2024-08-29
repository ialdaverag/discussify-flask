# Functools
from functools import wraps

# Inspect
import inspect

# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Models
# from app.models.user import Block
# from app.models.community import Community


def filtered_users(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app.models.user import Block 

        users = func(*args, **kwargs)

        if not current_user:
            return users

        signature = inspect.signature(func)
        
        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        community = None

        if 'community' in bound_arguments.arguments:
            community = bound_arguments.arguments['community']

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