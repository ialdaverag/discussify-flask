from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate

from app.schemas.user import UserSchema


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
            validate.Length(min=3, max=20, error='name must be between 3 and 20 characters'),
            validate.Regexp(
                r'^[a-zA-Z0-9_]*$', 
                error='name must consist of letters, numbers, and underscores only')
        ]
    )
    about = fields.Str(
        validate=validate.Length(max=1000, error='maximum 1000 characters')
    )
    subscriber = fields.Boolean()
    moderator = fields.Boolean()
    ban = fields.Boolean()
    owner = fields.Nested(UserSchema, attribute='owner')
    stats = fields.Nested(CommunityStatsSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


community_schema = CommunitySchema()
communities_schema = CommunitySchema(many=True)