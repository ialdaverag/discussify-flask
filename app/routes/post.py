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


@post_routes.route('/', methods=['POST'])
@jwt_required()
def create_post():
    json_data = request.get_json()

    try:
        data = post_schema.load(json_data)
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    community_id = data['community_id']
    community = Community.get_by_id(community_id)
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    title = data.get('title')
    content = data.get('content')

    post = current_user.create_post(title, content, community)

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


@post_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_post(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    json_data = request.get_json()

    try:
        data = post_schema.load(json_data, partial=('title', 'content', 'community_id'))
    except ValidationError as err:
        return {'errors': err.messages}, HTTPStatus.BAD_REQUEST
    
    title = data.get('title')
    content = data.get('content')

    print(title)
    print(content)
    
    post = current_user.update_post(post, title, content)

    return post_schema.dump(post), HTTPStatus.OK


@post_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    if current_user.id != post.user_id:
        return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
    
    db.session.delete(post)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


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


@post_routes.route('/<int:id>/vote/up', methods=['POST'])
@jwt_required()
def upvote(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    community_id = post.community_id
    community = Community.query.get(community_id)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user not in community.subscribers:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST

    vote = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if vote:
        if vote.direction == -1 or vote.direction == 0:
            vote.direction = 1

            db.session.commit()

            return {'message': 'Vote changed'}, HTTPStatus.NO_CONTENT

        return {'message': 'You have already upvoted this publication'}, HTTPStatus.BAD_REQUEST
    
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


@post_routes.route('/<int:id>/vote/down', methods=['POST'])
@jwt_required()
def downvote(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    community_id = post.community_id
    community = Community.query.get(community_id)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user not in community.subscribers:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST

    vote = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if vote:
        if vote.direction == 1 or vote.direction == 0:
            vote.direction = -1

            print(vote.direction)

            db.session.commit()

            return {'message': 'Vote changed'}, HTTPStatus.NO_CONTENT
        
        return {'message': 'You have already upvoted this publication'}, HTTPStatus.BAD_REQUEST
    
    vote = PostVote(user_id=current_user.id, post_id=post.id, direction=-1)

    db.session.add(vote)
    db.session.commit()

    return {}, HTTPStatus.NO_CONTENT


@post_routes.route('/<int:id>/downvoters', methods=['GET'])
@jwt_required(optional=True)
def read_downvoters(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    downvotes = PostVote.query.filter_by(post_id=id, direction=-1).all()

    downvoters = [vote.user for vote in downvotes]

    return users_schema.dump(downvoters), HTTPStatus.OK


@post_routes.route('/<int:id>/vote/cancel', methods=['POST'])
@jwt_required()
def cancel(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)

    community_id = post.community_id
    community = Community.query.get(community_id)

    if current_user in community.banned:
        return {'message': 'You are banned from this community'}, HTTPStatus.BAD_REQUEST

    if current_user not in community.subscribers:
        return {'message': 'You are not subscribed to this community'}, HTTPStatus.BAD_REQUEST

    vote = PostVote.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if vote:
        if vote.direction == 0:
            return {'message': 'Vote already canceled'}, HTTPStatus.BAD_REQUEST

        vote.direction = 0

        db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    return {'message': 'You have not voted this post'}, HTTPStatus.BAD_REQUEST


@post_routes.route('/<int:id>/comments', methods=['GET'])
@jwt_required(optional=True)
def read_post_comments(id):
    post = Post.query.get(id)

    if not post:
        return {'message': 'Post not found'}, HTTPStatus.NOT_FOUND
    
    return comments_schema.dump(post.comments)