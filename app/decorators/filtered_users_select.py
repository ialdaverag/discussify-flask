from flask_jwt_extended import current_user
from functools import wraps
import inspect
from sqlalchemy.sql import select

def filtered_users_select(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app.models.user import Block, User

        users_query = func(*args, **kwargs)

        if not current_user:
            return users_query

        signature = inspect.signature(func)

        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        community = None

        if 'community' in bound_arguments.arguments:
            community = bound_arguments.arguments['community']

        if community and current_user:
            if current_user.is_moderator_of(community):
                return users_query

        blocked_users = set(Block.get_blocked(current_user))
        blocking_users = set(Block.get_blockers(current_user))

        if not blocked_users and not blocking_users:
            return users_query

        blocked_user_ids = [user.id for user in blocked_users]
        blocking_user_ids = [user.id for user in blocking_users]

        filtered_users_query = users_query.where(
            ~User.id.in_(blocked_user_ids) &
            ~User.id.in_(blocking_user_ids)
        )

        return filtered_users_query

    return wrapper