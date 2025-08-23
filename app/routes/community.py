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

# Models
from app.models.community import Community
from app.models.user import User

# Managers
from app.managers.community import CommunityManager
from app.managers.community import SubscriptionManager
from app.managers.community import ModerationManager
from app.managers.community import BanManager
from app.managers.community import TransferManager
from app.managers.post import PostManager

# Schemas
from app.schemas.community import community_pagination_request_schema
from app.schemas.community import community_pagination_response_schema
from app.schemas.user import user_pagination_request_schema
from app.schemas.user import user_pagination_response_schema
from app.schemas.community import community_schema
from app.schemas.post import post_pagination_request_schema
from app.schemas.post import post_pagination_response_schema

community_routes = Blueprint('community_routes', __name__)


@community_routes.post('/')
@jwt_required()
def create_community():
    json_data = request.get_json()

    data = community_schema.load(json_data)

    community = CommunityManager.create(current_user, data)

    # Clear communities list cache after creating a community
    cache.delete_memoized('read_communities')

    return community_schema.dump(community), HTTPStatus.CREATED


@community_routes.get('/<string:name>')
@jwt_required(optional=True)
@cache.cached(timeout=600, key_prefix='community_%s')  # Cache for 10 minutes
def read_community(name):
    community = Community.get_by_name(name)
    
    CommunityManager.read(name)

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.get('/')
@use_args(community_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=600, query_string=True)  # Cache for 10 minutes
def read_communities(args):
    paginated_communities = CommunityManager.read_all(args)

    return community_pagination_response_schema.dump(paginated_communities), HTTPStatus.OK


@community_routes.patch('/<string:name>')
@jwt_required()
def update_community(name):
    community = Community.get_by_name(name=name)

    json_data = request.get_json()

    data = community_schema.load(json_data, partial=('name',))
    
    community = CommunityManager.update(current_user, community, data)

    # Clear relevant caches after updating a community
    cache.delete_memoized('read_community', name)
    cache.delete_memoized('read_communities')

    return community_schema.dump(community), HTTPStatus.OK


@community_routes.delete('/<string:name>')
@jwt_required()
def delete_community(name):
    community = Community.get_by_name(name=name)

    CommunityManager.delete(current_user, community)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/subscribe')
@jwt_required()
def subscribe(name):
    community = Community.get_by_name(name)

    SubscriptionManager.create(current_user, community)

    # Clear subscribers cache after subscription
    cache.delete_memoized('read_subscribers', name)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/unsubscribe')
@jwt_required()
def unsubscribe(name):
    community = Community.get_by_name(name)

    SubscriptionManager.delete(current_user, community)

    # Clear subscribers cache after unsubscription
    cache.delete_memoized('read_subscribers', name)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/mod/<string:username>')
@jwt_required()
def mod(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    ModerationManager.create(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/unmod/<string:username>')
@jwt_required()
def unmod(name, username):
    community = Community.get_by_name(name)

    user = User.get_by_username(username)

    ModerationManager.delete(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/ban/<string:username>')
@jwt_required()
def ban(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    BanManager.create(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/unban/<string:username>')
@jwt_required()
def unban(name, username):
    community = Community.get_by_name(name)
    
    user = User.get_by_username(username)
    
    BanManager.delete(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.post('/<string:name>/transfer/<string:username>')
@jwt_required()
def transfer(name, username):
    community = Community.get_by_name(name=name)
    
    user = User.get_by_username(username=username)
    
    TransferManager.create(current_user, community, user)

    return {}, HTTPStatus.NO_CONTENT


@community_routes.get('/<string:name>/subscribers')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=300, query_string=True)  # Cache for 5 minutes
def read_subscribers(args, name):
    community = Community.get_by_name(name)

    paginated_subscribers = SubscriptionManager.read_subscribers_by_community(community, args)

    return user_pagination_response_schema.dump(paginated_subscribers), HTTPStatus.OK


@community_routes.get('/<string:name>/moderators')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=900, query_string=True)  # Cache for 15 minutes (changes less frequently)
def read_moderators(args, name):
    community = Community.get_by_name(name)

    paginated_moderators = ModerationManager.read_moderators_by_community(community, args)

    return user_pagination_response_schema.dump(paginated_moderators), HTTPStatus.OK


@community_routes.get('/<string:name>/banned')
@use_args(user_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=600, query_string=True)  # Cache for 10 minutes
def read_banned(args, name):
    community = Community.get_by_name(name)

    paginated_banned = BanManager.read_bans_by_community(community, args)

    return user_pagination_response_schema.dump(paginated_banned), HTTPStatus.OK


@community_routes.get('/<string:name>/posts')
@use_args(post_pagination_request_schema, location='query')
@jwt_required(optional=True)
@cache.cached(timeout=180, query_string=True)  # Cache for 3 minutes (more dynamic content)
def read_community_posts(args, name):
    community = Community.get_by_name(name)

    paginated_posts = PostManager.read_all_by_community(community, args)
    
    return post_pagination_response_schema.dump(paginated_posts), HTTPStatus.OK