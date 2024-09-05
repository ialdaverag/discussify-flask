from functools import wraps
import inspect
from flask_jwt_extended import current_user


def filtered_users(func):
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


def filtered_posts(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app.models.user import Block
        from app.models.post import Post

        posts_query = func(*args, **kwargs)

        if not current_user:
            return posts_query

        signature = inspect.signature(func)

        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        community = None

        if 'community' in bound_arguments.arguments:
            community = bound_arguments.arguments['community']

        if community and current_user.is_moderator_of(community):
            return posts_query

        blocked_users = Block.get_blocked(current_user)
        blocking_users = Block.get_blockers(current_user)

        if not blocked_users and not blocking_users:
            return posts_query

        blocked_user_ids = [user.id for user in blocked_users]
        blocking_user_ids = [user.id for user in blocking_users]

        filtered_posts_query = posts_query.filter(
            ~Post.user_id.in_(blocked_user_ids) &
            ~Post.user_id.in_(blocking_user_ids)
        )

        return filtered_posts_query

    return wrapper



def filtered_comments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from app.models.user import Block
        from app.models.comment import Comment

        comments_query = func(*args, **kwargs)

        if not current_user:
            return comments_query

        signature = inspect.signature(func)

        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        post = None

        if 'post' in bound_arguments.arguments:
            post = bound_arguments.arguments['post']
        
        community = post.community if post else None

        if community and current_user.is_moderator_of(community):
            return comments_query

        blocked_users = Block.get_blocked(current_user)
        blocking_users = Block.get_blockers(current_user)

        if not blocked_users and not blocking_users:
            return comments_query

        blocked_user_ids = [user.id for user in blocked_users]
        blocking_user_ids = [user.id for user in blocking_users]

        filtered_comments_query = comments_query.filter(
            ~Comment.user_id.in_(blocked_user_ids) &
            ~Comment.user_id.in_(blocking_user_ids)
        )

        return filtered_comments_query

    return wrapper
