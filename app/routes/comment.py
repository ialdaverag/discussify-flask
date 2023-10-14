from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from marshmallow import ValidationError

from app.schemas.comment import comment_schema
from app.schemas.comment import comments_schema
from app.schemas.user import users_schema

from app.models.post import Post
from app.models.user import User
from app.models.community import Community
from app.models.comment import Comment
from app.models.comment import CommentVote

from app.extensions.database import db

comment_routes = Blueprint('comment_routes', __name__)


@comment_routes.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    json_data = request.get_json()

    try:
        data = comment_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST

    post_id = data['post_id']
    post = Post.get_by_id(post_id)

    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    comment_id = data.get('comment_id')

    comment_to_reply = None

    if comment_id is not None:
        comment_to_reply = Comment.get_by_id(comment_id)

    content = data.get('content')

    new_comment = current_user.create_comment(content, post, comment_to_reply)

    return comment_schema.dump(new_comment), HTTPStatus.CREATED


@comment_routes.route('/<string:id>', methods=['GET'])
@jwt_required(optional=True)
def read_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.route('/', methods=['GET'])
@jwt_required(optional=True)
def read_comments():
    comments = Comment.query.all()

    return comments_schema.dump(comments), HTTPStatus.OK


@comment_routes.route('/<string:id>', methods=['PATCH'])
@jwt_required()
def update_comment(id):
    comment = Comment.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    json_data = request.get_json()

    try:
        data = comment_schema.load(json_data, partial=('content', 'post_id'))
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    content = data.get('content')

    comment = current_user.update_comment(content, comment)

    return comment_schema.dump(comment), HTTPStatus.OK


@comment_routes.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    comment = Comment.get_by_id(id)
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    current_user.delete_comment(comment)

    return {}, HTTPStatus.NO_CONTENT
    

@comment_routes.route('/<int:id>/bookmark', methods=['POST'])
@jwt_required()
def bookmark_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if comment in current_user.comment_bookmarks:
        return {'message': 'Comment already bookmarked'}, HTTPStatus.BAD_REQUEST
    
    current_user.comment_bookmarks.append(comment)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.route('/<int:id>/unbookmark', methods=['POST'])
@jwt_required()
def unbookmark_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if comment not in current_user.comment_bookmarks:
        return {'message': 'Comment not bookmarked'}, HTTPStatus.BAD_REQUEST
    
    current_user.comment_bookmarks.remove(comment)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.route('/<int:id>/vote/up', methods=['POST'])
@jwt_required()
def upvote_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    post_id = comment.post_id
    post = Post.query.get(post_id)

    community_id = post.community_id
    community = Community.query.get(community_id)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user not in community.subscribers:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST
    
    vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()

    if vote:
        if vote.direction == -1 or vote.direction == 0:
            vote.direction = 1

            db.session.commit()

            return {'message': 'Vote changed'}, HTTPStatus.NO_CONTENT

        return {'message': 'You have already upvoted this comment'}, HTTPStatus.BAD_REQUEST
    
    vote = CommentVote(user_id=current_user.id, comment_id=comment.id, direction=1)

    db.session.add(vote)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.route('/<int:id>/upvoters', methods=['GET'])
@jwt_required(optional=True)
def read_comment_upvoters(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    upvotes = CommentVote.query.filter_by(comment_id=id, direction=1).all()

    upvoters = [vote.user for vote in upvotes]

    return users_schema.dump(upvoters), HTTPStatus.OK


@comment_routes.route('/<int:id>/vote/down', methods=['POST'])
@jwt_required()
def downvote_comment(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    post_id = comment.post_id
    post = Post.query.get(post_id)

    community_id = post.community_id
    community = Community.query.get(community_id)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user not in community.subscribers:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST
    
    vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()

    if vote:
        if vote.direction == 1 or vote.direction == 0:
            vote.direction = -1

            db.session.commit()

            return {'message': 'Vote changed'}, HTTPStatus.NO_CONTENT

        return {'message': 'You have already downvoted this comment'}, HTTPStatus.BAD_REQUEST
    
    vote = CommentVote(user_id=current_user.id, comment_id=comment.id, direction=1)

    db.session.add(vote)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@comment_routes.route('/<int:id>/downvoters', methods=['GET'])
@jwt_required(optional=True)
def read_comment_downvoters(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    downvotes = CommentVote.query.filter_by(comment_id=id, direction=-1).all()

    downvoters = [vote.user for vote in downvotes]

    return users_schema.dump(downvoters), HTTPStatus.OK


@comment_routes.route('/<int:id>/vote/cancel', methods=['POST'])
@jwt_required()
def cancel_comment_vote(id):
    comment = Comment.query.get(id)

    if not comment:
        return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    post_id = comment.post_id
    post = Post.query.get(post_id)

    community_id = post.community_id
    community = Community.query.get(community_id)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user not in community.subscribers:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST
    
    vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()

    if vote:
        if vote.direction == 0:
            return {'message': 'Vote already canceled'}, HTTPStatus.BAD_REQUEST

        vote.direction = 0

        db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    return {'message': 'You have not voted this comment'}, HTTPStatus.BAD_REQUEST