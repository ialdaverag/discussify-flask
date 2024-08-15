from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import current_user

from marshmallow import ValidationError

from app.schemas.comment import comment_schema
from app.schemas.comment import comment_update_schema
from app.schemas.comment import comments_schema
from app.schemas.user import users_schema

from app.models.post import Post
from app.models.user import User
from app.models.community import Community
from app.models.comment import Comment
from app.models.comment import CommentVote

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

    post_id = data['post_id']
    post = Post.get_by_id(post_id)

    comment_id = data.get('comment_id')

    comment_to_reply = None

    if comment_id is not None:
        comment_to_reply = Comment.get_by_id(comment_id)

    content = data.get('content')

    new_comment = current_user.create_comment(content, post, comment_to_reply)

    return comment_schema.dump(new_comment), HTTPStatus.CREATED


@comment_routes.get('/<string:id>')
@jwt_required(optional=True)
def read_comment(id):
    comment = Comment.get_by_id(id)
    
    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.get('/')
@jwt_required(optional=True)
def read_comments():
    comments = Comment.get_all()

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
    
    content = data.get('content')

    comment = current_user.update_comment(content, comment)

    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.delete('/<string:id>')
@jwt_required()
def delete_comment(id):
    comment = Comment.get_by_id(id)

    current_user.delete_comment(comment)

    return {}, HTTPStatus.NO_CONTENT
    

@comment_routes.post('/<int:id>/bookmark')
@jwt_required()
def bookmark_comment(id):
    comment = Comment.get_by_id(id)
    
    current_user.bookmark_comment(comment)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/unbookmark')
@jwt_required()
def unbookmark_comment(id):
    comment = Comment.get_by_id(id)

    current_user.unbookmark_comment(comment)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/vote/up')
@jwt_required()
def upvote_comment(id):
    comment = Comment.get_by_id(id)

    current_user.upvote_comment(comment)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.post('/<int:id>/vote/down')
@jwt_required()
def downvote_comment(id):
    comment = Comment.get_by_id(id)

    current_user.downvote_comment(comment)

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.get('/<int:id>/upvoters')
@jwt_required(optional=True)
def read_comment_upvoters(id):
    comment = Comment.get_by_id(id)
    
    upvoters = CommentVote.get_upvoters_by_comment(comment)

    return users_schema.dump(upvoters), HTTPStatus.OK


@comment_routes.get('/<int:id>/downvoters')
@jwt_required(optional=True)
def read_comment_downvoters(id):
    comment = Comment.get_by_id(id)
    
    downvoters = CommentVote.get_downvoters_by_comment(comment)

    return users_schema.dump(downvoters), HTTPStatus.OK


@comment_routes.post('/<int:id>/vote/cancel')
@jwt_required()
def cancel_vote_on_comment(id):
    comment = Comment.get_by_id(id)

    current_user.cancel_comment_vote(comment)

    return {}, HTTPStatus.NO_CONTENT