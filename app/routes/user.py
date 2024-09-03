# HTTP
from http import HTTPStatus

# Flask
from flask import Blueprint

# Flask JWT Extended
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

# Webargs
from webargs.flaskparser import use_args

# Models
from app.models.user import User

# Managers
from app.managers.user import UserManager
from app.managers.user import FollowManager
from app.managers.user import BlockManager
from app.managers.community import SubscriptionManager
from app.managers.post import PostManager
from app.managers.post import PostBookmarkManager
from app.managers.post import PostVoteManager
from app.managers.comment import CommentManager
from app.managers.comment import CommentBookmarkManager
from app.managers.comment import CommentVoteManager

# Schemas
from app.schemas.user import user_schema
from app.schemas.user import me_schema
from app.schemas.user import user_pagination_request_schema
from app.schemas.user import user_pagination_response_schema
from app.schemas.community import community_pagination_request_schema
from app.schemas.community import community_pagination_response_schema
from app.schemas.post import post_pagination_request_schema
from app.schemas.post import post_pagination_response_schema
from app.schemas.post import posts_schema
from app.schemas.comment import comments_schema

user_routes = Blueprint('user_routes', __name__)


@user_routes.get('/<string:username>')
@jwt_required(optional=True)
def read_user(username):
    user = User.get_by_username(username=username)

    UserManager.read(current_user, user)

    return user_schema.dump(user), HTTPStatus.OK


@user_routes.get('/')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_users(args):
    paginated_users = UserManager.read_all(current_user, args)

    return user_pagination_response_schema.dump(paginated_users), HTTPStatus.OK


@user_routes.post('/<string:username>/follow')
@jwt_required()
def follow_user(username):
    user_to_follow = User.get_by_username(username=username)

    FollowManager.create(current_user, user_to_follow)
    
    return {'message': 'You are now following the user'}, HTTPStatus.NO_CONTENT


@user_routes.post('/<string:username>/unfollow')
@jwt_required()
def unfollow_user(username):
    user_to_unfollow = User.get_by_username(username=username)
    
    FollowManager.delete(current_user, user_to_unfollow)
    
    return {'message': 'You are no longer following this user'}, HTTPStatus.NO_CONTENT


@user_routes.post('/<string:username>/block')
@jwt_required()
def block_user(username):
    user_to_block = User.get_by_username(username=username)
    
    BlockManager.create(current_user, user_to_block)
    
    return {'message': 'You are now blocking the user'}, HTTPStatus.NO_CONTENT


@user_routes.post('/<string:username>/unblock')
@jwt_required()
def unblock_user(username):
    user_to_unblock = User.get_by_username(username=username)
    
    BlockManager.delete(current_user, user_to_unblock)
    
    return {'message': 'You are no longer blocking this user'}, HTTPStatus.NO_CONTENT


@user_routes.get('/<string:username>/following')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_following(args, username):
    user = User.get_by_username(username)

    paginated_following = FollowManager.read_followed(user, args)
    
    return user_pagination_response_schema.dump(paginated_following), HTTPStatus.OK


@user_routes.get('/<string:username>/followers')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_followers(args, username):
    user = User.get_by_username(username)

    paginated_followers = FollowManager.read_followers(user, args)
    
    return user_pagination_response_schema.dump(paginated_followers), HTTPStatus.OK


@user_routes.get('/blocked')
@use_args(user_pagination_request_schema, location='query')
@jwt_required()
def read_blocked(args):
    paginated_blocked = BlockManager.read_blocked(current_user, args)
    
    return user_pagination_response_schema.dump(paginated_blocked), HTTPStatus.OK


@user_routes.get('/<string:username>/subscriptions')
@use_args(community_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_subscriptions(args, username):
    user = User.get_by_username(username)

    paginated_subscriptions = SubscriptionManager.read_subscriptions_by_user(user, args)

    return community_pagination_response_schema.dump(paginated_subscriptions),   HTTPStatus.OK


@user_routes.get('/<string:username>/posts')
@use_args(post_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_user_posts(args, username):
    user = User.get_by_username(username)

    paginated_posts = PostManager.read_all_by_user(user, args)
    
    return post_pagination_response_schema.dump(paginated_posts), HTTPStatus.OK


@user_routes.get('/<string:username>/comments')
@jwt_required(optional=True)
def read_user_comments(username):
    user = User.get_by_username(username)

    comments = CommentManager.read_all_by_user(user)
    
    return comments_schema.dump(comments)


@user_routes.get('/me')
@jwt_required()
def me():
    return me_schema.dump(current_user)


@user_routes.get('/posts/bookmarked')
@use_args(post_pagination_request_schema, location='query')
@jwt_required()
def read_user_bookmarked_posts(args):
    paginated_bookmarks = PostBookmarkManager.read_bookmarked_posts_by_user(current_user, args)

    return post_pagination_response_schema.dump(paginated_bookmarks), HTTPStatus.OK


@user_routes.get('/posts/upvoted')
@jwt_required()
def read_user_upvoted_posts():
    upvotes = PostVoteManager.read_upvoted_posts_by_user(current_user)

    return posts_schema.dump(upvotes), HTTPStatus.OK


@user_routes.get('/posts/downvoted')
@jwt_required()
def read_user_downvoted_posts():
    downvotes = PostVoteManager.read_downvoted_posts_by_user(current_user)

    return posts_schema.dump(downvotes), HTTPStatus.OK


@user_routes.get('/comments/bookmarked')
@jwt_required()
def read_user_bookmarked_comments():
    bookmarks = CommentBookmarkManager.read_bookmarked_comments_by_user(current_user)
    
    return comments_schema.dump(bookmarks), HTTPStatus.OK


@user_routes.get('/comments/upvoted')
@jwt_required()
def read_user_upvoted_comments():
    upvotes = CommentVoteManager.read_upvoted_comments_by_user(current_user)

    return comments_schema.dump(upvotes), HTTPStatus.OK


@user_routes.get('/comments/downvoted')
@jwt_required()
def read_user_downvoted_comments():
    downvotes = CommentVoteManager.read_downvoted_comments_by_user(current_user)

    return comments_schema.dump(downvotes), HTTPStatus.OK
