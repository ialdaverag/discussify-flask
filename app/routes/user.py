from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from app.extensions.database import db

from app.models.user import User
from app.models.post import PostVote
from app.models.comment import CommentVote

from app.schemas.user import user_schema
from app.schemas.user import users_schema
from app.schemas.user import me_schema
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
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    current_user.follow(user_to_follow)
    
    return {'message': 'You are now following the user'}, HTTPStatus.NO_CONTENT


@user_routes.post('/<string:username>/unfollow')
@jwt_required()
def unfollow_user(username):
    user_to_unfollow = User.get_by_username(username=username)

    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)
    
    current_user.unfollow(user_to_unfollow)
    
    return {'message': 'You are no longer following this user'}, HTTPStatus.NO_CONTENT


@user_routes.get('/<string:username>/following')
@jwt_required(optional=True)
def read_following(username):
    user = User.get_by_username(username)
    
    return users_schema.dump(user.followed)


@user_routes.get('/<string:username>/followers')
@jwt_required(optional=True)
def read_followers(username):
    user = User.get_by_username(username)
    
    return users_schema.dump(user.followers)


@user_routes.get('/<string:username>/subscriptions')
@jwt_required(optional=True)
def read_subscriptions(username):
    user = User.get_by_username(username)

    return communities_schema.dump(user.subscriptions)


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
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    return me_schema.dump(current_user)


@user_routes.get('/posts/bookmarked')
@jwt_required()
def read_user_bookmarks():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    return posts_schema.dump(current_user.bookmarks)


@user_routes.get('/posts/upvoted')
@jwt_required()
def read_user_upvoted_posts():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    upvotes = PostVote.query.filter_by(user_id=current_user.id, direction=1).all()

    posts = [upvote.post for upvote in upvotes]

    return posts_schema.dump(posts), HTTPStatus.OK


@user_routes.get('/posts/downvoted')
@jwt_required()
def read_user_downvoted_posts():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    downvotes = PostVote.query.filter_by(user_id=current_user.id, direction=-1).all()

    posts = [downvote.post for downvote in downvotes]

    return posts_schema.dump(posts), HTTPStatus.OK


@user_routes.get('/comments/upvoted')
@jwt_required()
def read_user_upvoted_comments():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    upvotes = CommentVote.query.filter_by(user_id=current_user.id, direction=1).all()

    comments = [upvote.comment for upvote in upvotes]

    return comments_schema.dump(comments), HTTPStatus.OK


@user_routes.get('/comments/downvoted')
@jwt_required()
def read_user_downvoted_comments():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    downvotes = CommentVote.query.filter_by(user_id=current_user.id, direction=-1).all()

    comments = [downvote.comment for downvote in downvotes]

    return comments_schema.dump(comments), HTTPStatus.OK


@user_routes.get('/comments/bookmarked')
@jwt_required()
def read_user_bookmarked_comments():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    return comments_schema.dump(current_user.comment_bookmarks)