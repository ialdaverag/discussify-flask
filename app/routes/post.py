# HTTP
from http import HTTPStatus

# Flask
from flask import Blueprint
from flask import request

# Flask-JWT-Extended
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

# Webargs
from webargs.flaskparser import use_args

# Schemas
from app.schemas.user import user_pagination_request_schema
from app.schemas.user import user_pagination_response_schema
from app.schemas.post import post_pagination_request_schema
from app.schemas.post import post_pagination_response_schema
from app.schemas.post import post_schema
from app.schemas.post import posts_schema
from app.schemas.comment import comment_pagination_request_schema
from app.schemas.comment import comment_pagination_response_schema

# Models
from app.models.community import Community
from app.models.post import Post

# Managers
from app.managers.post import PostManager
from app.managers.post import PostBookmarkManager
from app.managers.post import PostVoteManager
from app.managers.comment import CommentManager

post_routes = Blueprint('post_routes', __name__)


@post_routes.post('/')
@jwt_required()
def create_post():
    json_data = request.get_json()

    data = post_schema.load(json_data)
    
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
@use_args(post_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_users(args):
    paginated_posts = PostManager.read_all(args)

    return post_pagination_response_schema.dump(paginated_posts), HTTPStatus.OK

@post_routes.patch('/<int:id>')
@jwt_required()
def update_post(id):
    post = Post.get_by_id(id)

    json_data = request.get_json()

    data = post_schema.load(json_data, partial=('title', 'content', 'community_id'))
    
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
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_upvoters(args, id):
    post = Post.get_by_id(id)
    
    paginated_upvoters = PostVoteManager.read_upvoters_by_post(post, args)

    return user_pagination_response_schema.dump(paginated_upvoters), HTTPStatus.OK


@post_routes.get('/<int:id>/downvoters')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_downvoters(args, id):
    post = Post.get_by_id(id)
    
    paginated_downvoters = PostVoteManager.read_downvoters_by_post(post, args)

    return user_pagination_response_schema.dump(paginated_downvoters), HTTPStatus.OK


@post_routes.get('/<int:id>/comments')
@use_args(comment_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_post_comments(args, id):
    post = Post.get_by_id(id)

    paginated_comments = CommentManager.read_all_root_comments_by_post(post, args)
    
    return comment_pagination_response_schema.dump(paginated_comments), HTTPStatus.OK