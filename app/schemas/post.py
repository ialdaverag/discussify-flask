from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate

from app.schemas.user import UserSchema
from app.schemas.community import CommunitySchema


class PostSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    title = fields.Str(
        required=True, 
        validate=validate.Length(
            min=3, 
            max=70, 
            error='title must be between 8 and 40 characters'
        )
    )
    content = fields.Str(
        required=True, 
        validate=validate.Length(
            min=1, 
            error='content must contain at least 1 character'
        )
    )
    community_id = fields.Integer(
        required=True, 
        load_only=True
    )
    owner = fields.Nested(
        UserSchema, 
        dump_only=True
    )
    community = fields.Nested(
        CommunitySchema, 
        dump_only=True
    )
    bookmarked = fields.Boolean(dump_only=True)
    upvoted = fields.Boolean(dump_only=True)
    downvoted = fields.Boolean(dump_only=True)
    comments_count = fields.Integer(dump_only=True)
    bookmarks_count = fields.Integer(dump_only=True)
    upvotes_count = fields.Integer(dump_only=True)
    downvotes_count = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)