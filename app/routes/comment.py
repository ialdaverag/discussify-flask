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

# Extensions
from app.extensions.database import db

comment_routes = Blueprint('comment_routes', __name__)


@comment_routes.post('/')
@jwt_required()
def create_comment():
    json_data = request.get_json()

    try:
        data = comment_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST

    # Get the post_id from the data
    post_id = data.get('post_id')

    # Get the post by the post_id
    post = Post.get_by_id(post_id)

    # Get the comment_id from the data
    comment_id = data.get('comment_id')

    # Initialize the comment_to_reply to None
    comment_to_reply = None

    if comment_id is not None:
        comment_to_reply = Comment.get_by_id(comment_id)

    new_comment = CommentManager.create(current_user, post, data, comment_to_reply)

    return comment_schema.dump(new_comment), HTTPStatus.CREATED


@comment_routes.get('/<string:id>')
@jwt_required(optional=True)
def read_comment(id):
    comment = Comment.get_by_id(id)
    
    CommentManager.read(id)
    
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

    try:
        data = comment_update_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST

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
@jwt_required(optional=True)
def read_comment_upvoters(id):
    comment = Comment.get_by_id(id)
    
    upvoters = CommentVoteManager.read_upvoters_by_comment(comment)

    return users_schema.dump(upvoters), HTTPStatus.OK


@comment_routes.get('/<int:id>/downvoters')
@jwt_required(optional=True)
def read_comment_downvoters(id):
    comment = Comment.get_by_id(id)
    
    downvoters = CommentVoteManager.read_downvoters_by_comment(comment)

    return users_schema.dump(downvoters), HTTPStatus.OK
