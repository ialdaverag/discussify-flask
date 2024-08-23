# HTTP
from http import HTTPStatus

# Flask
from flask import Blueprint
from flask import request

# Flask-JWT-Extended
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

# Marshmallow
from marshmallow import ValidationError

# Schemas
from app.schemas.post import post_schema
from app.schemas.post import posts_schema
from app.schemas.user import users_schema
from app.schemas.comment import comments_schema

# Models
from app.models.community import Community
from app.models.post import Post

# Managers
from app.managers.post import PostManager
from app.managers.post import PostBookmarkManager
from app.managers.post import PostVoteManager

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

    post = PostManager.create(current_user, community, data)

    return post_schema.dump(post), HTTPStatus.CREATED


@post_routes.get('/<int:id>')
@jwt_required(optional=True)
def read_post(id):
    post = Post.get_by_id(id)

    PostManager.read(current_user, post)

    return post_schema.dump(post), HTTPStatus.OK


@post_routes.get('/')
@jwt_required(optional=True)
def read_posts():
    posts = PostManager.read_all()

    return posts_schema.dump(posts), HTTPStatus.OK


@post_routes.patch('/<int:id>')
@jwt_required()
def update_post(id):
    post = Post.get_by_id(id)

    json_data = request.get_json()

    try:
        data = post_schema.load(json_data, partial=('title', 'content', 'community_id'))
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    post = PostManager.update(current_user, post, data)

    return post_schema.dump(post), HTTPStatus.OK


@post_routes.delete('/<int:id>')
@jwt_required()
def delete_post(id):
    post = Post.get_by_id(id)

    PostManager.delete(current_user, post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/bookmark')
@jwt_required()
def bookmark(id):
    post = Post.get_by_id(id)

    PostBookmarkManager.create(current_user, post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/unbookmark')
@jwt_required()
def unbookmark(id):
    post = Post.get_by_id(id)

    PostBookmarkManager.delete(current_user, post)
    
    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/vote/up')
@jwt_required()
def upvote(id):
    post = Post.get_by_id(id)

    PostVoteManager.create(current_user, post, direction=1)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/vote/down')
@jwt_required()
def downvote(id):
    post = Post.get_by_id(id)

    PostVoteManager.create(current_user, post, direction=-1)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.post('/<int:id>/vote/cancel')
@jwt_required()
def cancel(id):
    post = Post.get_by_id(id)

    PostVoteManager.delete(current_user, post)

    return {}, HTTPStatus.NO_CONTENT


@post_routes.get('/<int:id>/upvoters')
@jwt_required(optional=True)
def read_upvoters(id):
    post = Post.get_by_id(id)
    
    upvoters = PostVoteManager.read_upvoters_by_post(post)

    return users_schema.dump(upvoters), HTTPStatus.OK


@post_routes.get('/<int:id>/downvoters')
@jwt_required(optional=True)
def read_downvoters(id):
    post = Post.get_by_id(id)
    
    downvoters = PostVoteManager.read_downvoters_by_post(post)

    return users_schema.dump(downvoters), HTTPStatus.OK


@post_routes.get('/<int:id>/comments')
@jwt_required(optional=True)
def read_post_comments(id):
    post = Post.get_by_id(id)
    
    return comments_schema.dump(post.read_root_comments())