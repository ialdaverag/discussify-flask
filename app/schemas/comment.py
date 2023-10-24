from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate

from app.schemas.user import UserSchema
from app.schemas.post import PostSchema


class CommentSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    content = fields.Str(
        required=True,
        validate=validate.Length(
            min=1, 
            error='content must contain at least 1 character'
        )
    )
    post_id = fields.Integer(required=True, load_only=True)
    comment_id = fields.Integer(load_only=True)
    owner = fields.Nested(UserSchema, dump_only=True)
    post = fields.Nested(PostSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    replies = fields.List(fields.Nested(lambda: CommentSchema()))


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)