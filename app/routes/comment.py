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

# Extensions
from app.extensions.cache import cache

# Schemas
from app.schemas.user import user_pagination_request_schema
from app.schemas.user import user_pagination_response_schema
from app.schemas.comment import comment_schema
from app.schemas.comment import comment_update_schema
from app.schemas.comment import comment_pagination_request_schema
from app.schemas.comment import comment_pagination_response_schema

# Models
from app.models.post import Post
from app.models.comment import Comment

# Managers
from app.managers.comment import CommentManager
from app.managers.comment import CommentBookmarkManager
from app.managers.comment import CommentVoteManager


comment_routes = Blueprint('comment_routes', __name__)


@comment_routes.post('/')
@jwt_required()
def create_comment():
    json_data = request.get_json()
    
    data = comment_schema.load(json_data)

    post_id = data.get('post_id')

    post = Post.get_by_id(post_id)

    comment_id = data.get('comment_id')

    comment_to_reply = None

    if comment_id is not None:
        comment_to_reply = Comment.get_by_id(comment_id)

    new_comment = CommentManager.create(current_user, post, data, comment_to_reply)

    # Clear relevant caches after creating a comment
    cache.delete_memoized('read_comments')  # Clear comments list cache
    cache.delete_memoized('read_post_comments', post_id)  # Clear post comments cache

    return comment_schema.dump(new_comment), HTTPStatus.CREATED


@comment_routes.get('/<string:id>')
@jwt_required(optional=True)
@cache.cached(timeout=300, key_prefix='comment_%s')  # Cache for 5 minutes
def read_comment(id):
    comment = Comment.get_by_id(id)
    
    CommentManager.read(current_user, comment)
    
    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.get('/')
@use_args(comment_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=240, query_string=True)  # Cache for 4 minutes
def read_comments(args):
    paginated_comments = CommentManager.read_all(args)

    return comment_pagination_response_schema.dump(paginated_comments), HTTPStatus.OK


@comment_routes.patch('/<string:id>')
@jwt_required()
def update_comment(id):
    comment = Comment.get_by_id(id)

    json_data = request.get_json()

    data = comment_update_schema.load(json_data)

    comment = CommentManager.update(current_user, comment, data)

    # Clear relevant caches after updating a comment
    cache.delete_memoized('read_comment', id)  # Clear individual comment cache
    cache.delete_memoized('read_comments')  # Clear comments list cache

    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.delete('/<string:id>')
@jwt_required()
def delete_comment(id):
    comment = Comment.get_by_id(id)

    CommentManager.delete(current_user, comment)

    # Clear relevant caches after deleting a comment
    cache.delete_memoized('read_comment', id)  # Clear individual comment cache
    cache.delete_memoized('read_comments')  # Clear comments list cache

    return {}, HTTPStatus.NO_CONTENT
    

@comment_routes.post('/<int:id>/bookmark')
@jwt_required()
def bookmark_comment(id):
    comment = Comment.get_by_id(id)
    
    CommentBookmarkManager.create(current_user, comment)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/unbookmark')
@jwt_required()
def unbookmark_comment(id):
    comment = Comment.get_by_id(id)

    CommentBookmarkManager.delete(current_user, comment)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/vote/up')
@jwt_required()
def upvote_comment(id):
    comment = Comment.get_by_id(id)

    CommentVoteManager.create(current_user, comment, direction=1)

    # Clear vote-related caches
    cache.delete_memoized('read_comment_upvoters', id)
    cache.delete_memoized('read_comment_downvoters', id)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/vote/down')
@jwt_required()
def downvote_comment(id):
    comment = Comment.get_by_id(id)

    CommentVoteManager.create(current_user, comment, direction=-1)

    # Clear vote-related caches
    cache.delete_memoized('read_comment_upvoters', id)
    cache.delete_memoized('read_comment_downvoters', id)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/vote/cancel')
@jwt_required()
def cancel_vote_on_comment(id):
    comment = Comment.get_by_id(id)

    CommentVoteManager.delete(current_user, comment)

    # Clear vote-related caches
    cache.delete_memoized('read_comment_upvoters', id)
    cache.delete_memoized('read_comment_downvoters', id)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.get('/<int:id>/upvoters')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=300, query_string=True)  # Cache for 5 minutes
def read_comment_upvoters(args, id):
    comment = Comment.get_by_id(id)
    
    paginated_upvoters = CommentVoteManager.read_upvoters_by_comment(comment, args)

    return user_pagination_response_schema.dump(paginated_upvoters), HTTPStatus.OK


@comment_routes.get('/<int:id>/downvoters')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=300, query_string=True)  # Cache for 5 minutes
def read_comment_downvoters(args, id):
    comment = Comment.get_by_id(id)

    paginated_downvoters = CommentVoteManager.read_downvoters_by_comment(comment, args)

    return user_pagination_response_schema.dump(paginated_downvoters), HTTPStatus.OK
