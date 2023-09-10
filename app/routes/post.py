from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from schemas.post import post_schema
from schemas.post import posts_schema
from schemas.user import users_schema

from extensions.database import db

from models.community import Community
from models.user import User
from models.post import Post
from models.post import PostVote

post_routes = Blueprint('post_routes', __name__)


@post_routes.route('/', methods=['POST'])
@jwt_required()
def create_post():
    json_data = request.get_json()

    try:
        data = post_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    community_id = data['community_id']
    community = Community.query.filter_by(id=community_id).first()

    if not community:
        return {'message': 'Community not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user not in community.subscriptors:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST

    post = Post(**data, user_id=current_user.id)

    db.session.add(post)
    db.session.commit()

    return post_schema.dump(post), HTTPStatus.CREATED


@post_routes.route('/<int:id>', methods=['GET'])
@jwt_required(optional=True)
def read_post(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND

    return post_schema.dump(post), HTTPStatus.OK


@post_routes.route('/', methods=['GET'])
@jwt_required(optional=True)
def read_posts():
    posts = Post.query.all()

    return posts_schema.dump(posts), HTTPStatus.OK


@post_routes.route('/<int:id>/bookmark', methods=['POST'])
@jwt_required()
def bookmark(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if post in current_user.bookmarks:
        return {'message': 'Post already bookmarked'}, HTTPStatus.BAD_REQUEST
    
    current_user.bookmarks.append(post)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@post_routes.route('/<int:id>/unbookmark', methods=['POST'])
@jwt_required()
def unbookmark(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if post not in current_user.bookmarks:
        return {'message': 'Post not bookmarked'}, HTTPStatus.BAD_REQUEST
    
    current_user.bookmarks.remove(post)
    db.session.commit()
    
    return {}, HTTPStatus.NO_CONTENT


@post_routes.route('/<int:id>/upvote', methods=['POST'])
@jwt_required()
def upvote(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    vote = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if vote:
        return {'message': 'You have already upvoted this publication'}, HTTPStatus.NOT_FOUND
    
    vote = PostVote(user_id=current_user.id, post_id=post.id, direction=1)

    db.session.add(vote)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@post_routes.route('/<int:id>/upvoters', methods=['GET'])
@jwt_required(optional=True)
def read_upvoters(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    upvotes = PostVote.query.filter_by(post_id=id, direction=1).all()

    upvoters = [vote.user for vote in upvotes]

    return users_schema.dump(upvoters), HTTPStatus.OK