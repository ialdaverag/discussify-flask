from http import HTTPStatus

from flask import Blueprint
from flask import request


from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from app.schemas.post import post_schema
from app.schemas.post import posts_schema
from app.schemas.user import users_schema
from app.schemas.comment import comments_schema

from app.extensions.database import db

from app.models.community import Community
from app.models.user import User
from app.models.post import Post
from app.models.post import PostVote

post_routes = Blueprint('post_routes', __name__)


@post_routes.post('/')
@jwt_required()
def create_post():
    json_data = request.get_json()

    try:
        data = post_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    community_id = data['community_id']
    community = Community.get_by_id(community_id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    title = data.get('title')
    content = data.get('content')

    post = current_user.create_post(title, content, community)

    return post_schema.dump(post), HTTPStatus.CREATED


@post_routes.get('/<int:id>')
@jwt_required(optional=True)
def read_post(id):
    post = Post.get_by_id(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND

    return post_schema.dump(post), HTTPStatus.OK


@post_routes.get('/')
@jwt_required(optional=True)
def read_posts():
    posts = Post.query.all()

    return posts_schema.dump(posts), HTTPStatus.OK


@post_routes.patch('/<int:id>')
@jwt_required()
def update_post(id):
    post = Post.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    json_data = request.get_json()

    try:
        data = post_schema.load(json_data, partial=('title', 'content', 'community_id'))
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    title = data.get('title')
    content = data.get('content')
    
    post = current_user.update_post(post, title, content)

    return post_schema.dump(post), HTTPStatus.OK


@post_routes.delete('/<int:id>')
@jwt_required()
def delete_post(id):
    post = Post.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    current_user.delete_post(post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/bookmark')
@jwt_required()
def bookmark(id):
    post = Post.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    current_user.bookmark_post(post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/unbookmark')
@jwt_required()
def unbookmark(id):
    post = Post.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    current_user.unbookmark_post(post)
    
    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/vote/up')
@jwt_required()
def upvote(id):
    post = Post.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    current_user.upvote_post(post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.get('/<int:id>/upvoters')
@jwt_required(optional=True)
def read_upvoters(id):
    post = Post.get_by_id(id)
    
    upvotes = PostVote.query.filter_by(post_id=post.id, direction=1).all()

    upvoters = [vote.user for vote in upvotes]

    return users_schema.dump(upvoters), HTTPStatus.OK


@post_routes.post('/<int:id>/vote/down')
@jwt_required()
def downvote(id):
    post = Post.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    current_user.downvote_post(post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.get('/<int:id>/downvoters')
@jwt_required(optional=True)
def read_downvoters(id):
    post = Post.get_by_id(id)
    
    downvotes = PostVote.query.filter_by(post_id=post.id, direction=-1).all()

    downvoters = [vote.user for vote in downvotes]

    return users_schema.dump(downvoters), HTTPStatus.OK


@post_routes.post('/<int:id>/vote/cancel')
@jwt_required()
def cancel(id):
    post = Post.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    current_user.cancel_post_vote(post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.get('/<int:id>/comments')
@jwt_required(optional=True)
def read_post_comments(id):
    post = Post.get_by_id(id)
    
    return comments_schema.dump(post.read_root_comments())