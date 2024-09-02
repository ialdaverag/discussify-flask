# Marshmallow
from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate

# Schemas
from app.schemas.user import UserSchema
from app.schemas.pagination import PaginationSchema


class CommunityPaginationRequestSchema(Schema):
    class Meta:
        ordered = True

    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=10)


class CommunityStatsSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    posts_count = fields.Integer()
    comments_count = fields.Integer()
    subscribers_count = fields.Integer()
    moderators_count = fields.Integer()
    banned_count = fields.Integer()


class CommunitySchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=20, error='Name must be between 3 and 20 characters.'),
            validate.Regexp(
                r'^[a-zA-Z0-9_]*$', 
                error='Name must consist of letters, numbers, and underscores only.')
        ]
    )
    about = fields.Str(
        validate=validate.Length(max=1000, error='Maximum 1000 characters.')
    )
    owned_by = fields.Boolean()
    subscriber = fields.Boolean()
    moderator = fields.Boolean()
    ban = fields.Boolean()
    owner = fields.Nested(UserSchema, attribute='owner')
    stats = fields.Nested(CommunityStatsSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CommunityPaginationResponseSchema(PaginationSchema):
    class Meta:
        ordered = True

    communities = fields.Nested(CommunitySchema, attribute="items", many=True)


community_pagination_request_schema = CommunityPaginationRequestSchema()
community_pagination_response_schema = CommunityPaginationResponseSchema()
community_schema = CommunitySchema()
communities_schema = CommunitySchema(many=True)
