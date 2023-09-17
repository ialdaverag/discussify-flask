from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from models.user import User
from models.post import PostVote
from models.comment import CommentVote

from schemas.user import user_schema
from schemas.user import users_schema
from schemas.community import communities_schema
from schemas.post import posts_schema
from schemas.comment import comments_schema

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


@user_routes.route('/bookmarks', methods=['GET'])
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