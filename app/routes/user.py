# HTTP
from http import HTTPStatus

# Flask
from flask import Blueprint

# Flask JWT Extended
from flask_jwt_extended import (
    jwt_required, 
    current_user
)

# Models
from app.models.user import User
from app.models.user import Follow
from app.models.community import CommunitySubscriber
from app.models.post import PostVote
from app.models.post import PostBookmark
from app.models.comment import CommentVote
from app.models.comment import CommentBookmark

# Schemas
from app.schemas.user import (
    user_schema, 
    users_schema, 
    me_schema
)

# Schemas
from app.schemas.community import communities_schema
from app.schemas.post import posts_schema
from app.schemas.comment import comments_schema

user_routes = Blueprint('user_routes', __name__)


@user_routes.get('/<string:username>')
@jwt_required(optional=True)
def read_user(username):
    user = User.get_by_username(username)

    return user_schema.dump(user), HTTPStatus.OK


@user_routes.get('/')
@jwt_required(optional=True)
def read_users():
    users = User.get_all()

    return users_schema.dump(users), HTTPStatus.OK


@user_routes.post('/<string:username>/follow')
@jwt_required()
def follow_user(username):
    user_to_follow = User.get_by_username(username=username)

    current_user.follow(user_to_follow)
    
    return {'message': 'You are now following the user'}, HTTPStatus.NO_CONTENT


@user_routes.post('/<string:username>/unfollow')
@jwt_required()
def unfollow_user(username):
    user_to_unfollow = User.get_by_username(username=username)
    
    current_user.unfollow(user_to_unfollow)
    
    return {'message': 'You are no longer following this user'}, HTTPStatus.NO_CONTENT


@user_routes.get('/<string:username>/following')
@jwt_required(optional=True)
def read_following(username):
    user = User.get_by_username(username)

    following = Follow.get_followed(user)
    
    return users_schema.dump(following)


@user_routes.get('/<string:username>/followers')
@jwt_required(optional=True)
def read_followers(username):
    user = User.get_by_username(username)

    followers = Follow.get_followers(user)
    
    return users_schema.dump(followers)


@user_routes.get('/<string:username>/subscriptions')
@jwt_required(optional=True)
def read_subscriptions(username):
    user = User.get_by_username(username)

    subscriptions = CommunitySubscriber.get_subscriptions_by_user(user)

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
def read_user_bookmarks():
    bookmarks = PostBookmark.get_bookmarks_by_user(current_user)

    return posts_schema.dump(bookmarks), HTTPStatus.OK


@user_routes.get('/posts/upvoted')
@jwt_required()
def read_user_upvoted_posts():
    upvotes = PostVote.get_upvoted_posts_by_user(current_user)

    return posts_schema.dump(upvotes), HTTPStatus.OK


@user_routes.get('/posts/downvoted')
@jwt_required()
def read_user_downvoted_posts():
    downvotes = PostVote.get_downvoted_posts_by_user(current_user)

    return posts_schema.dump(downvotes), HTTPStatus.OK


@user_routes.get('/comments/upvoted')
@jwt_required()
def read_user_upvoted_comments():
    upvotes = CommentVote.get_upvoted_comments_by_user(current_user)

    return comments_schema.dump(upvotes), HTTPStatus.OK


@user_routes.get('/comments/downvoted')
@jwt_required()
def read_user_downvoted_comments():
    downvotes = CommentVote.get_downvoted_comments_by_user(current_user)

    return comments_schema.dump(downvotes), HTTPStatus.OK


@user_routes.get('/comments/bookmarked')
@jwt_required()
def read_user_bookmarked_comments():
    bookmarks = CommentBookmark.get_bookmarks_by_user(current_user)
    
    return comments_schema.dump(bookmarks), HTTPStatus.OK