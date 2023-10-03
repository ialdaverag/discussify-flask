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
from app.schemas.community import communities_schema
from app.schemas.post import posts_schema
from app.schemas.comment import comments_schema

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/<string:username>', methods=['GET'])
@jwt_required(optional=True)
def read_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    return user_schema.dump(user), HTTPStatus.OK


@user_routes.route('/', methods=['GET'])
@jwt_required(optional=True)
def read_users():
    users = User.query.all()

    return users_schema.dump(users), HTTPStatus.OK


@user_routes.route('/<string:username>/available', methods=['GET'])
@jwt_required()
def is_username_available(username):
    user = User.query.filter_by(username=username).first()

    if user:
        return {'message': False}, HTTPStatus.OK

    return {'message': True}, HTTPStatus.OK


@user_routes.route('/<string:username>/follow', methods=['POST'])
@jwt_required()
def follow_user(username):
    user_to_follow = User.query.filter_by(username=username).first()

    if not user_to_follow:
        return {'message': 'User to follow not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if user_to_follow == current_user:
        return {'message': 'You cannot follow yourself'}, HTTPStatus.BAD_REQUEST
    
    if user_to_follow in current_user.followed:
            return {'message': 'You are already following this user'}, HTTPStatus.BAD_REQUEST
    
    current_user.followed.append(user_to_follow)
    db.session.commit()
    
    return {'message': 'You are now following the user'}, HTTPStatus.CREATED


@user_routes.route('/<string:username>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(username):
    user_to_unfollow = User.query.filter_by(username=username).first()

    if not user_to_unfollow:
        return {'message': 'User to unfollow not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if user_to_unfollow == current_user:
        return {'message': 'You cannot unfollow yourself'}, HTTPStatus.BAD_REQUEST
    
    if user_to_unfollow not in current_user.followed:
            return {'message': 'You are not following this user'}, HTTPStatus.BAD_REQUEST
    
    current_user.followed.remove(user_to_unfollow)
    db.session.commit()
    
    return {'message': 'You are no longer following this user'}, HTTPStatus.CREATED


@user_routes.route('/<string:username>/following', methods=['GET'])
@jwt_required(optional=True)
def read_following(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    return users_schema.dump(user.followed)


@user_routes.route('/<string:username>/followers', methods=['GET'])
@jwt_required(optional=True)
def read_followers(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    return users_schema.dump(user.followers)


@user_routes.route('/<string:username>/subscriptions', methods=['GET'])
@jwt_required(optional=True)
def read_subscriptions(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

    return communities_schema.dump(user.subscriptions)


@user_routes.route('/<string:username>/posts', methods=['GET'])
@jwt_required(optional=True)
def read_user_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    return posts_schema.dump(user.posts)


@user_routes.route('/posts/bookmarked', methods=['GET'])
@jwt_required()
def read_user_bookmarks():
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    return posts_schema.dump(current_user.bookmarks)


@user_routes.route('/posts/upvoted', methods=['GET'])
@jwt_required()
def read_user_upvoted_posts():
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    upvotes = PostVote.query.filter_by(user_id=current_user.id, direction=1).all()

    posts = [upvote.post for upvote in upvotes]

    return posts_schema.dump(posts), HTTPStatus.OK


@user_routes.route('/posts/downvoted', methods=['GET'])
@jwt_required()
def read_user_downvoted_posts():
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    downvotes = PostVote.query.filter_by(user_id=current_user.id, direction=-1).all()

    posts = [downvote.post for downvote in downvotes]

    return posts_schema.dump(posts), HTTPStatus.OK


@user_routes.route('/<string:username>/comments', methods=['GET'])
@jwt_required(optional=True)
def read_user_comments(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
    
    return comments_schema.dump(user.comments)


@user_routes.route('/comments/upvoted', methods=['GET'])
@jwt_required()
def read_user_upvoted_comments():
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    upvotes = CommentVote.query.filter_by(user_id=current_user.id, direction=1).all()

    comments = [upvote.comment for upvote in upvotes]

    return comments_schema.dump(comments), HTTPStatus.OK


@user_routes.route('/comments/downvoted', methods=['GET'])
@jwt_required()
def read_user_downvoted_comments():
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    downvotes = CommentVote.query.filter_by(user_id=current_user.id, direction=-1).all()

    comments = [downvote.comment for downvote in downvotes]

    return comments_schema.dump(comments), HTTPStatus.OK


@user_routes.route('/comments/bookmarked', methods=['GET'])
@jwt_required()
def read_user_bookmarked_comments():
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    return comments_schema.dump(current_user.comment_bookmarks)