# HTTP
from http import HTTPStatus

# Flask
from flask import Blueprint

# Flask JWT Extended
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

# Models
from app.models.user import User

# Managers
from app.schemas.user import user_schema
from app.schemas.user import users_schema
from app.schemas.user import me_schema

# Managers
from app.managers.user import UserManager
from app.managers.user import FollowManager
from app.managers.community import SubscriptionManager
from app.managers.post import PostBookmarkManager
from app.managers.post import PostVoteManager
from app.managers.comment import CommentBookmarkManager
from app.managers.comment import CommentVoteManager

# Schemas
from app.schemas.community import communities_schema
from app.schemas.post import posts_schema
from app.schemas.comment import comments_schema

user_routes = Blueprint('user_routes', __name__)


@user_routes.get('/<string:username>')
@jwt_required(optional=True)
def read_user(username):
    user = UserManager.read(username)

    return user_schema.dump(user), HTTPStatus.OK


@user_routes.get('/')
@jwt_required(optional=True)
def read_users():
    users = UserManager.read_all()

    return users_schema.dump(users), HTTPStatus.OK


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


@user_routes.get('/<string:username>/following')
@jwt_required(optional=True)
def read_following(username):
    user = User.get_by_username(username)

    following = FollowManager.read_followed(user)
    
    return users_schema.dump(following)


@user_routes.get('/<string:username>/followers')
@jwt_required(optional=True)
def read_followers(username):
    user = User.get_by_username(username)

    followers = FollowManager.read_followers(user)
    
    return users_schema.dump(followers)


@user_routes.get('/<string:username>/subscriptions')
@jwt_required(optional=True)
def read_subscriptions(username):
    user = User.get_by_username(username)

    subscriptions = SubscriptionManager.read_subscriptions_by_user(user)

    return communities_schema.dump(subscriptions)


@user_routes.get('/<string:username>/posts')
@jwt_required(optional=True)
def read_user_posts(username):
    user = User.get_by_username(username)
    
    return posts_schema.dump(user.posts)


@user_routes.get('/<string:username>/comments')
@jwt_required(optional=True)
def read_user_comments(username):
    user = User.get_by_username(username)
    
    return comments_schema.dump(user.comments)


@user_routes.get('/me')
@jwt_required()
def me():
    return me_schema.dump(current_user)


@user_routes.get('/posts/bookmarked')
@jwt_required()
def read_user_bookmarked_posts():
    bookmarks = PostBookmarkManager.read_bookmarked_posts_by_user(current_user)

    return posts_schema.dump(bookmarks), HTTPStatus.OK


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
