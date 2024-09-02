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
from app.schemas.comment import comment_schema
from app.schemas.comment import comment_update_schema
from app.schemas.comment import comments_schema
from app.schemas.user import users_schema

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

    return comment_schema.dump(new_comment), HTTPStatus.CREATED


@comment_routes.get('/<string:id>')
@jwt_required(optional=True)
def read_comment(id):
    comment = Comment.get_by_id(id)
    
    CommentManager.read(current_user, comment)
    
    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.get('/')
@jwt_required(optional=True)
def read_comments():
    comments = CommentManager.read_all()

    return comments_schema.dump(comments), HTTPStatus.OK


@comment_routes.patch('/<string:id>')
@jwt_required()
def update_comment(id):
    comment = Comment.get_by_id(id)

    json_data = request.get_json()

    data = comment_update_schema.load(json_data)

    comment = CommentManager.update(current_user, comment, data)

    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.delete('/<string:id>')
@jwt_required()
def delete_comment(id):
    comment = Comment.get_by_id(id)

    CommentManager.delete(current_user, comment)

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

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/vote/down')
@jwt_required()
def downvote_comment(id):
    comment = Comment.get_by_id(id)

    CommentVoteManager.create(current_user, comment, direction=-1)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/vote/cancel')
@jwt_required()
def cancel_vote_on_comment(id):
    comment = Comment.get_by_id(id)

    CommentVoteManager.delete(current_user, comment)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.get('/<int:id>/upvoters')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
def read_comment_upvoters(args, id):
    comment = Comment.get_by_id(id)
    
    downvoted_upvoters = CommentVoteManager.read_upvoters_by_comment(comment, args)

    return user_pagination_response_schema.dump(downvoted_upvoters), HTTPStatus.OK


@comment_routes.get('/<int:id>/downvoters')
@jwt_required(optional=True)
def read_comment_downvoters(id):
    comment = Comment.get_by_id(id)
    
    downvoters = CommentVoteManager.read_downvoters_by_comment(comment)

    return users_schema.dump(downvoters), HTTPStatus.OK
